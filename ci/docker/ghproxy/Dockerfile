FROM gcr.io/k8s-prow/ghproxy
VOLUME ["/cache"]
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
