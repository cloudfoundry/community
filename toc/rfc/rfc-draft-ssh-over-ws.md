# Meta
[meta]: #meta
- Name: CF SSH over WebSockets
- Start Date: 2024-04-08
- Author(s): @domdom82
- Status: Draft
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/807


## Summary

This RFC aims at providing an additional way of using CF SSH in an effort to reduce the potential attack surface against SSH.

By tunneling SSH through a WebSocket connection, the SSH client may reuse the same port as regular HTTP traffic, removing the need for port 2222 as well as a separate ingress for platform operators.

## Problem

Cloud Foundry is a shared multi-tenant platform.

If a feature requiring an open port such as CF SSH is used by at least one customer, the port has to be opened on the whole platform. It cannot be enabled for one tenant but disabled for another.

The way CF SSH is configurable today, a specific port must be open and it must be open for the whole platform. The port is easily discoverable by both customers and potential attackers.

In production deployments of Cloud Foundry, it is commonplace for customers to run security scans on their workloads to ensure compliance and reduce attack surfaces.

These scans usually complain that besides port 443 for HTTP traffic, also port 2222 is open for SSH on the internet-facing load balancer. Many customers demand closure of the port as they
view it as a potential attack surface for brute-force attacks against the SSH protocol.

The issue is exacerbated by features like "bring-your-own-domain" where customers provide a CNAME entry alongside a matching x509 certificate that points their own (sub-)domain to an app hosted on the shared Cloud Foundry environment.

If the Cloud Foundry operator chooses to host the HTTP ingress and the SSH ingress on the same load balancer, this can cause potential reputation damage to the customer because to an outsider, it looks like the port 2222 is open on the customer's domain, e.g. `www.big-corp.com:2222` open looks worse than `my-app.cf-app.com:2222` even though both are technically the same.

If the Cloud Foundry operator runs the HTTP ingress and SSH ingress on different load balancers, this may be less of an issue as the customer's domain would be `www.big-corp.com:443` only and be separate from a potential `ssh.cf-app.com:2222`. However, such an ingress would still look very inviting to attackers and would incur additional costs and maintenance.

Security-wise it is easier for an attacker to probe the environment by simply doing a port scan and then testing direct attacks on the SSH proxy:

```
nmap api.cf-app.com

Starting Nmap 7.94 ( https://nmap.org ) at 2024-04-08 10:29 CEST
Nmap scan report for api.cf-app.com (1.2.3.4)
Host is up (0.031s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT     STATE SERVICE
80/tcp   open  http
443/tcp  open  https
2222/tcp open  EtherNetIP-1
```

then proceed with connecting to the port 2222:

```
nc api.cf.cf-app.com 2222

SSH-2.0-diego-ssh-proxy
```

the SSH proxy greets with the SSH-2.0 version, allowing the attacker to try all kinds of SSH-2.0 related probes.

Another facet of the problem is that many customers require explicit allow-listing of external web sites from their on-prem environments.
Port 443 is usually not a problem as many firewalls open it by default, but port 2222 likely is frowned upon and cause for concern.

## Proposal

The proposal aims to make CF SSH less discoverable and reduce complexity and costs to potentially maintain two separate load balancers for HTTP and SSH traffic.

### Note on Security
The proposal does not aim to solve security issues of (CF) SSH per se. Tunneling a protocol through another does not make it inherently more secure. Any weakness of SSH within the CF SSH proxy will still be present even if the RFC is accepted. The main goal is to reduce the number of open ports required. Although, there is one minor security improvement as the SSH traffic will then be also encrypted by TLS within the WebSocket tunnel.


### Architecture Changes

![architecture-changes](rfc-draft-ssh-over-ws/cf-ssh-over-websocket.drawio.png)

There are three scenarios:

#### Scenario A: Legacy SSH
This is the default scenario as of today. All changed components MUST ensure this scenario still works. It SHOULD be tested with legacy CLI versions such as v6 which are no longer updated. This scenario includes regular SSH clients like OpenSSH.

#### Scenario B: Dual SSH / WS
This scenario MAY be enabled by operators. It allows legacy SSH as well as pure WebSocket-based SSH in one environment. The CF CLI MUST understand the legacy flow from scenario A. The CF CLI SHOULD understand the new flow using a WebSocket tunnel. Other components MUST support both scenarios.

#### Scenario C: WS only
This scenario MAY be enabled by operators. It turns of the legacy scenario A and allows operators to close the public port 2222 on the load balancer. The CF CLI MUST understand the new flow using a WebSocket tunnel. Other components MUST support the new flow and MAY support both scenarios.


### Changes per Component (Scenario B and C)

#### CF CLI
- The CLI MUST query the "/" endpoint of Cloud Controller.
- The CLI MUST use at least v3 of CC API for this feature.
- The "v2/info" endpoint is deprecated and not used by CLI v7/8. It MUST NOT return "app_ssh_ws_endpoint" info.
- The "/" endpoint SHOULD return the legacy SSH info, if the legacy SSH feature is enabled:

```
{
  "links": {
	(...)
    "app_ssh": {
      "href": "ssh.cf.cf-app.com:2222",
      "meta": {
        "host_key_fingerprint": "TD1dRQINLi2KxilVLzAI8tXB2h8MP79oyVJnUwshjdc",
        "oauth_client": "ssh-proxy"
      }
	}
  }
}
```
- The "/" endpoint MUST NOT return the legacy SSH info, if the legacy SSH feature is disabled.

- The endpoint MUST return an object for ssh-over-websocket if the feature is enabled:

```
{
  "links": {
	(...)
    "app_ssh_ws": {
      "href": "wss://ssh.cf.cf-app.com",
      "meta": {
        "host_key_fingerprint": "TD1dRQINLi2KxilVLzAI8tXB2h8MP79oyVJnUwshjdc",
        "oauth_client": "ssh-proxy"
      }
	}
  }
}
```

- If both legacy SSH and SSH-over-WebSocket features are enabled, the "/" endpoint MUST return info objects for both features:

```
{
  "links": {
	(...)
    "app_ssh": {
      "href": "ssh.cf.cf-app.com:2222",
      "meta": {
        "host_key_fingerprint": "TD1dRQINLi2KxilVLzAI8tXB2h8MP79oyVJnUwshjdc",
        "oauth_client": "ssh-proxy"
      }
	}

    "app_ssh_ws": {
      "href": "wss://ssh.cf.cf-app.com",
      "meta": {
        "host_key_fingerprint": "TD1dRQINLi2KxilVLzAI8tXB2h8MP79oyVJnUwshjdc",
        "oauth_client": "ssh-proxy"
      }
	}
  }
}
```

- CF CLI MUST prefer the `app_ssh_ws` link over the `app_ssh` link if present.
- CF CLI MAY fall back to `app_ssh` link if `app_ssh_ws` did not connect successfully and both are present.
- When using `app_ssh_ws`, the CF CLI MUST wrap the SSH connection in a WebSocket connection:

```
func (c *secureShell) Connect(opts *options.SSHOptions) error {
	err := c.validateTarget(opts)
	if err != nil {
		return err
	}

	clientConfig := &ssh.ClientConfig{
		User: fmt.Sprintf("cf:%s/%d", c.app.GUID, opts.Index),
		Auth: []ssh.AuthMethod{
			ssh.Password(c.token),
		},
		HostKeyCallback: fingerprintCallback(opts, c.sshEndpointFingerprint),
	}

	// Wrap SSH in WebSocket if possible
	var secureClient SecureClient
	if c.sshWsEndpoint != "" {
		secureClient, err = tunnelSSHThruWebSocket(c.sshWsEndpoint, clientConfig)
	}

	if err != nil {
		// Fall back to SSH over TCP
		secureClient, err = c.secureDialer.Dial("tcp", c.sshEndpoint, clientConfig)
		if err != nil {
			return err
		}
	}

	c.secureClient = secureClient
	c.opts = opts
	return nil
}
```
Code adapted from [cloudfoundry/cli ssh.go](https://github.com/cloudfoundry/cli/blob/main/cf/ssh/ssh.go#L119)

The `sshWsEndpoint` would have to be fetched from the `app_ssh_ws.href` field of the "/" endpoint of CAPI.


A `tunnelSSHThruWebSocket` function could look something like this:
```
func tunnelSSHThruWebSocket(url string, config *ssh.ClientConfig) (SecureClient, error) {
	wsConn, err := websocket.Dial(url, "", url)
	if err != nil {
		return nil, err
	}

	c, chans, reqs, err := ssh.NewClientConn(wsConn, url, config)
	if err != nil {
		return nil, err
	}
	sshClient := ssh.NewClient(c, chans, reqs)
	return &secureClient{client: sshClient}, nil
}
```

- The rest of CF CLI SHOULD be unchanged and work as before.

#### CAPI

- CAPI MUST provide an additional `app_ssh_ws` object in the "/" endpoint, if the feature is enabled:
```
    "app_ssh_ws": {
      "href": "wss://ssh.cf.cf-app.com",
      "meta": {
        "host_key_fingerprint": "TD1dRQINLi2KxilVLzAI8tXB2h8MP79oyVJnUwshjdc",
        "oauth_client": "ssh-proxy"
      }
	}
```
- CAPI MUST provide both `app_ssh` and `app_ssh_ws` objects in the "/" endpoint, if both features are enabled.
- CAPI MUST NOT change the `app_ssh` object in any way to remain backwards compatible.
- The URL presented in the `app_ssh_ws.href`field MUST be `wss://` + the route as announced by route-registrar for SSH proxy (see [CF Deployment](#cf-deployment))

#### SSH Proxy

- Diego SSH Proxy SHOULD provide the option to [launch a separate WebSocket server](https://github.com/cloudfoundry/diego-ssh/blob/main/cmd/ssh-proxy/main.go#L65) besides the regular SSH server
- SSH Proxy SHOULD provide a separate handler for unwrapping WebSocket connections:
```
	sshWsProxy := wsProxy.New(logger, proxySSHServerConfig, metronClient, tlsConfig)
	wsServer := server.NewServer(logger, sshProxyConfig.Address, websocket.Handler(sshWsProxy), time.Duration(sshProxyConfig.IdleConnectionTimeout))
```
Changes in [ssh-proxy/main.go](https://github.com/cloudfoundry/diego-ssh/blob/main/cmd/ssh-proxy/main.go#L65C1-L67C1)

```
func (p *WsProxy) HandleConnection(wsConn *websocket.Conn) {
	logger := p.logger.Session("handle-ws-connection")
	defer wsConn.Close()

    // Here we start a SSH handshake inside the WebSocket tunnel
	serverConn, serverChannels, serverRequests, err := ssh.NewServerConn(wsConn, p.serverConfig)

(...)
```
Changes in [proxy.go](https://github.com/cloudfoundry/diego-ssh/blob/main/proxy/proxy.go#L67)

**Remark:**
(these changes are not meant as verbatim code; they only illustrate areas that would need to change)


- SSH Proxy SHOULD retain the legacy SSH server on port 2222 for backwards compatibiliy
- The code of the legacy SSH feature SHOULD NOT be deleted
- Diego Release SHOULD provide [a spec](https://github.com/cloudfoundry/diego-release/blob/develop/jobs/ssh_proxy/spec#L53) to define a `diego.ssh_proxy.listen_ws_addr` property with a default of `0.0.0.0:443` or `0.0.0.0:9443`
- Diego Release SHOULD provide [a spec](https://github.com/cloudfoundry/diego-release/blob/develop/jobs/ssh_proxy/spec#L59) to disable the `diego.ssh_proxy.listen_addr` property, closing the default port of 2222.

#### CF Deployment

- CF Deployment [deploys SSH Proxy on Scheduler](https://github.com/cloudfoundry/cf-deployment/blob/main/cf-deployment.yml#L1329) but there is no route to it at the moment.
- CF Deployment SHOULD deploy [route-registrar](https://github.com/cloudfoundry/routing-release/tree/develop/jobs/route_registrar) alongside SSH Proxy and configure it to announce a TLS route at Gorouter:
```
  - name: route_registrar
    properties:
      nats:
        tls:
          enabled: true
          client_cert: "((nats_client_cert.certificate))"
          client_key: "((nats_client_cert.private_key))"
      route_registrar:
        routes:
        - name: ssh-ws-proxy
          port: 443     # or 9443 if preferred
          tls_port: 443 # or 9443 if preferred
          registration_interval: 20s
          server_cert_domain_san: ssh.((system_domain))
          uris:
          - ssh.((system_domain))       # e.g. ssh.cf-app.com, announced by CAPI as wss://ssh.cf-app.com
    release: routing
```


### Remaining Compatible with OpenSSH

- Getting the ssh token via `cf ssh-code` MUST remain unchanged as it connects to UAA.
- Regular ssh, scp and sftp commands support a `-o ProxyCommand` option.
- The program run as `ProxyCommand` MUST read from `stdin` and write to `stdout` for ssh to work.
- The CF community MAY offer a simple WebSocket proxy for regular ssh as a [homebrew formula](https://github.com/cloudfoundry/homebrew-tap) or similar option.
- The CF CLI MAY also offer a WebSocket proxy, e.g. as a sub-command like `cf proxy-ssh`
- A simple WebSocket proxy could look like this:
```
func main() {
	url := os.Args[1]

	wsConn, err := websocket.Dial(url, "", url)

	if err != nil {
		panic(err)
	}

	wg := sync.WaitGroup{}
	wg.Add(2)

	go func() {
		_, err := io.Copy(wsConn, os.Stdin)
		if err != nil {
			fmt.Println(err.Error())
		}
		wg.Done()
	}()

	go func() {
		_, err := io.Copy(os.Stdout, wsConn)
		if err != nil {
			fmt.Println(err.Error())
		}
		wg.Done()
	}()

	wg.Wait()
	_ = wsConn.Close()
}
```
Source of `ws-proxy` used below

Which can be used with regular ssh like so:
```
ssh -o ProxyCommand="ws-proxy wss://ssh.cf-app.com" cf:$(cf app app-name --guid)/0@ssh.cf-app.com
```