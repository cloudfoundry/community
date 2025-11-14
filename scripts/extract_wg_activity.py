#!/usr/bin/env python3
"""
Extract raw repository activity data for Cloud Foundry working groups using GitHub GraphQL API.
This script extracts pure activity data without analysis or formatting.
"""

import yaml
import json
import subprocess
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import re
from dateutil import parser as date_parser

def extract_repos_from_charter(charter_file):
    """Extract repository information from a working group charter file."""
    with open(charter_file, 'r') as f:
        content = f.read()
    
    # Try YAML frontmatter first (new format)
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_content = parts[1]
            try:
                metadata = yaml.safe_load(yaml_content)
                # Convert from frontmatter format to old config format
                if 'repositories' in metadata:
                    config = {
                        'name': metadata.get('name', charter_file.split('/')[-1].replace('.md', '')),
                        'areas': [
                            {
                                'name': 'main',
                                'repositories': metadata['repositories']
                            }
                        ]
                    }
                    return config
            except yaml.YAMLError as e:
                print(f"Error parsing YAML frontmatter: {e}")
    
    # Fall back to old YAML block format
    yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
    if not yaml_match:
        print(f"No YAML configuration found in {charter_file}")
        return None
    
    try:
        config = yaml.safe_load(yaml_match.group(1))
        return config
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None

def get_repo_activity_graphql(repo, since_date):
    """Get raw repository activity using GitHub GraphQL API."""
    org, name = repo.split('/')
    since_iso = since_date.isoformat()
    
    activity = {
        'repository': repo,
        'commits': [],
        'pull_requests': [],
        'issues': [],
        'releases': []
    }
    
    print(f"  Fetching activity for {repo} since {since_date.strftime('%Y-%m-%d')}...")
    
    try:
        # GraphQL query for commits
        commits_query = f'''
        {{
          repository(owner: "{org}", name: "{name}") {{
            defaultBranchRef {{
              target {{
                ... on Commit {{
                  history(first: 100, since: "{since_iso}") {{
                    edges {{
                      node {{
                        oid
                        messageHeadline
                        messageBody
                        author {{
                          name
                          email
                          date
                        }}
                        url
                        associatedPullRequests(first: 5) {{
                          edges {{
                            node {{
                              number
                              title
                              url
                            }}
                          }}
                        }}
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        '''
        
        result = subprocess.run(['gh', 'api', 'graphql', '--cache', '1h', '-f', f'query={commits_query}'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('data', {}).get('repository', {}).get('defaultBranchRef'):
                commits = data['data']['repository']['defaultBranchRef']['target']['history']['edges']
                for edge in commits:
                    commit = edge['node']
                    associated_prs = [pr_edge['node'] for pr_edge in commit.get('associatedPullRequests', {}).get('edges', [])]
                    activity['commits'].append({
                        'sha': commit['oid'],
                        'message': commit['messageHeadline'],
                        'body': commit.get('messageBody', ''),
                        'author': commit['author']['name'],
                        'email': commit['author'].get('email', ''),
                        'date': commit['author']['date'],
                        'url': commit['url'],
                        'associated_prs': associated_prs
                    })
        
        # GraphQL query for pull requests
        prs_query = f'''
        {{
          repository(owner: "{org}", name: "{name}") {{
            pullRequests(first: 100, orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
              edges {{
                node {{
                  number
                  title
                  state
                  createdAt
                  updatedAt
                  closedAt
                  mergedAt
                  author {{
                    login
                  }}
                  url
                  body
                  labels(first: 20) {{
                    edges {{
                      node {{
                        name
                      }}
                    }}
                  }}
                  milestone {{
                    title
                  }}
                  assignees(first: 10) {{
                    edges {{
                      node {{
                        login
                      }}
                    }}
                  }}
                  reviews(first: 20) {{
                    edges {{
                      node {{
                        state
                        author {{
                          login
                        }}
                      }}
                    }}
                  }}
                  comments(first: 20) {{
                    edges {{
                      node {{
                        body
                        author {{
                          login
                        }}
                        createdAt
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        '''
        
        result = subprocess.run(['gh', 'api', 'graphql', '--cache', '1h', '-f', f'query={prs_query}'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('data', {}).get('repository', {}).get('pullRequests'):
                prs = data['data']['repository']['pullRequests']['edges']
                for edge in prs:
                    pr = edge['node']
                    # Filter by date
                    try:
                        created_date = date_parser.parse(pr['createdAt']).replace(tzinfo=None)
                        updated_date = date_parser.parse(pr['updatedAt']).replace(tzinfo=None)
                        
                        if created_date >= since_date or updated_date >= since_date:
                            labels = [label_edge['node']['name'] for label_edge in pr.get('labels', {}).get('edges', [])]
                            assignees = [assignee_edge['node']['login'] for assignee_edge in pr.get('assignees', {}).get('edges', [])]
                            reviews = [{'state': review_edge['node']['state'], 'author': review_edge['node']['author']['login'] if review_edge['node']['author'] else None} 
                                     for review_edge in pr.get('reviews', {}).get('edges', [])]
                            comments = [{'body': comment_edge['node']['body'], 'author': comment_edge['node']['author']['login'] if comment_edge['node']['author'] else None, 'date': comment_edge['node']['createdAt']} 
                                      for comment_edge in pr.get('comments', {}).get('edges', [])]
                            
                            activity['pull_requests'].append({
                                'number': pr['number'],
                                'title': pr['title'],
                                'state': pr['state'],
                                'created_at': pr['createdAt'],
                                'updated_at': pr['updatedAt'],
                                'closed_at': pr.get('closedAt'),
                                'merged_at': pr.get('mergedAt'),
                                'user': pr['author']['login'] if pr['author'] else None,
                                'url': pr['url'],
                                'body': pr['body'],
                                'labels': labels,
                                'milestone': pr.get('milestone', {}).get('title') if pr.get('milestone') else None,
                                'assignees': assignees,
                                'reviews': reviews,
                                'comments': comments
                            })
                    except Exception as e:
                        print(f"    Date parsing error for PR in {repo}: {e}")
        
        # GraphQL query for issues
        issues_query = f'''
        {{
          repository(owner: "{org}", name: "{name}") {{
            issues(first: 100, orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
              edges {{
                node {{
                  number
                  title
                  state
                  createdAt
                  updatedAt
                  closedAt
                  author {{
                    login
                  }}
                  url
                  body
                  labels(first: 20) {{
                    edges {{
                      node {{
                        name
                      }}
                    }}
                  }}
                  milestone {{
                    title
                  }}
                  assignees(first: 10) {{
                    edges {{
                      node {{
                        login
                      }}
                    }}
                  }}
                  comments(first: 20) {{
                    edges {{
                      node {{
                        body
                        author {{
                          login
                        }}
                        createdAt
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        '''
        
        result = subprocess.run(['gh', 'api', 'graphql', '--cache', '1h', '-f', f'query={issues_query}'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('data', {}).get('repository', {}).get('issues'):
                issues = data['data']['repository']['issues']['edges']
                for edge in issues:
                    issue = edge['node']
                    # Filter by date
                    try:
                        created_date = date_parser.parse(issue['createdAt']).replace(tzinfo=None)
                        updated_date = date_parser.parse(issue['updatedAt']).replace(tzinfo=None)
                        
                        if created_date >= since_date or updated_date >= since_date:
                            labels = [label_edge['node']['name'] for label_edge in issue.get('labels', {}).get('edges', [])]
                            assignees = [assignee_edge['node']['login'] for assignee_edge in issue.get('assignees', {}).get('edges', [])]
                            comments = [{'body': comment_edge['node']['body'], 'author': comment_edge['node']['author']['login'] if comment_edge['node']['author'] else None, 'date': comment_edge['node']['createdAt']} 
                                      for comment_edge in issue.get('comments', {}).get('edges', [])]
                            
                            activity['issues'].append({
                                'number': issue['number'],
                                'title': issue['title'],
                                'state': issue['state'],
                                'created_at': issue['createdAt'],
                                'updated_at': issue['updatedAt'],
                                'closed_at': issue.get('closedAt'),
                                'user': issue['author']['login'] if issue['author'] else None,
                                'url': issue['url'],
                                'body': issue['body'],
                                'labels': labels,
                                'milestone': issue.get('milestone', {}).get('title') if issue.get('milestone') else None,
                                'assignees': assignees,
                                'comments': comments
                            })
                    except Exception as e:
                        print(f"    Date parsing error for issue in {repo}: {e}")
        
        # GraphQL query for releases
        releases_query = f'''
        {{
          repository(owner: "{org}", name: "{name}") {{
            releases(first: 50, orderBy: {{field: CREATED_AT, direction: DESC}}) {{
              edges {{
                node {{
                  tagName
                  name
                  createdAt
                  publishedAt
                  author {{
                    login
                  }}
                  url
                  isPrerelease
                  isDraft
                  description
                  releaseAssets(first: 10) {{
                    edges {{
                      node {{
                        name
                        downloadCount
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        '''
        
        result = subprocess.run(['gh', 'api', 'graphql', '--cache', '1h', '-f', f'query={releases_query}'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('data', {}).get('repository', {}).get('releases'):
                releases = data['data']['repository']['releases']['edges']
                for edge in releases:
                    release = edge['node']
                    # Filter by date
                    try:
                        created_date = date_parser.parse(release['createdAt']).replace(tzinfo=None)
                        
                        if created_date >= since_date:
                            assets = [{'name': asset_edge['node']['name'], 'downloads': asset_edge['node']['downloadCount']} 
                                    for asset_edge in release.get('releaseAssets', {}).get('edges', [])]
                            
                            activity['releases'].append({
                                'tag_name': release['tagName'],
                                'name': release['name'],
                                'created_at': release['createdAt'],
                                'published_at': release.get('publishedAt'),
                                'author': release['author']['login'] if release['author'] else None,
                                'url': release['url'],
                                'prerelease': release['isPrerelease'],
                                'draft': release['isDraft'],
                                'description': release['description'],
                                'assets': assets
                            })
                    except Exception as e:
                        print(f"    Date parsing error for release in {repo}: {e}")
        
    except subprocess.TimeoutExpired:
        print(f"    Timeout while fetching data for {repo}")
    except subprocess.CalledProcessError as e:
        print(f"    Error fetching data for {repo}: {e}")
    except json.JSONDecodeError as e:
        print(f"    JSON decode error for {repo}: {e}")
    except Exception as e:
        print(f"    Unexpected error for {repo}: {e}")
    
    # Print activity summary for this repo
    total_activity = len(activity['commits']) + len(activity['pull_requests']) + len(activity['issues']) + len(activity['releases'])
    if total_activity > 0:
        print(f"    Found: {len(activity['commits'])} commits, {len(activity['pull_requests'])} PRs, {len(activity['issues'])} issues, {len(activity['releases'])} releases")
    
    return activity

def get_community_rfcs(since_date):
    """Get RFCs from cloudfoundry/community repo that are relevant to the reporting period."""
    rfcs = []
    
    try:
        print("  Fetching RFCs from cloudfoundry/community repository...")
        
        # Query for PRs and issues in community repo
        prs_query = f'''
        query {{
          repository(owner: "cloudfoundry", name: "community") {{
            pullRequests(first: 50, states: [OPEN, MERGED], orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
              edges {{
                node {{
                  number
                  title
                  state
                  url
                  createdAt
                  updatedAt
                  mergedAt
                  author {{
                    login
                  }}
                  body
                  labels(first: 10) {{
                    edges {{
                      node {{
                        name
                      }}
                    }}
                  }}
                  files(first: 10) {{
                    edges {{
                      node {{
                        path
                      }}
                    }}
                  }}
                }}
              }}
            }}
            issues(first: 50, states: [OPEN, CLOSED], orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
              edges {{
                node {{
                  number
                  title
                  state
                  url
                  createdAt
                  updatedAt
                  closedAt
                  author {{
                    login
                  }}
                  body
                  labels(first: 10) {{
                    edges {{
                      node {{
                        name
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        '''
        
        result = subprocess.run(['gh', 'api', 'graphql', '--cache', '1h', '-f', f'query={prs_query}'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            repo_data = data.get('data', {}).get('repository', {})
            
            # Process PRs
            prs = repo_data.get('pullRequests', {}).get('edges', [])
            for edge in prs:
                pr = edge['node']
                
                # Filter by date
                try:
                    updated_date = date_parser.parse(pr['updatedAt']).replace(tzinfo=None)
                    if updated_date >= since_date:
                        # Get labels and files
                        labels = [l['node']['name'] for l in pr.get('labels', {}).get('edges', [])]
                        files = [f['node']['path'] for f in pr.get('files', {}).get('edges', [])]
                        
                        # Check if it's RFC-related or working group related
                        is_rfc = (any('rfc' in file.lower() for file in files) or 
                                 'rfc' in pr['title'].lower() or
                                 any('rfc' in label.lower() for label in labels) or
                                 any(label.startswith('wg-') for label in labels))
                        
                        if is_rfc:
                            rfcs.append({
                                'number': pr['number'],
                                'title': pr['title'],
                                'state': pr['state'],
                                'url': pr['url'],
                                'created_at': pr['createdAt'],
                                'updated_at': pr['updatedAt'],
                                'merged_at': pr.get('mergedAt'),
                                'author': pr['author']['login'] if pr['author'] else 'Unknown',
                                'body': pr.get('body') or '',
                                'type': 'RFC Pull Request',
                                'files': files,
                                'labels': labels
                            })
                except Exception as e:
                    print(f"    Date parsing error for community PR: {e}")
            
            # Process Issues
            issues = repo_data.get('issues', {}).get('edges', [])
            for edge in issues:
                issue = edge['node']
                
                # Filter by date
                try:
                    updated_date = date_parser.parse(issue['updatedAt']).replace(tzinfo=None)
                    if updated_date >= since_date:
                        # Get labels
                        labels = [l['node']['name'] for l in issue.get('labels', {}).get('edges', [])]
                        
                        # Check if it's RFC-related or working group related
                        is_rfc = ('rfc' in issue['title'].lower() or
                                 any('rfc' in label.lower() for label in labels) or
                                 any(label.startswith('wg-') for label in labels))
                        
                        if is_rfc:
                            rfcs.append({
                                'number': issue['number'],
                                'title': issue['title'],
                                'state': issue['state'],
                                'url': issue['url'],
                                'created_at': issue['createdAt'],
                                'updated_at': issue['updatedAt'],
                                'closed_at': issue.get('closedAt'),
                                'author': issue['author']['login'] if issue['author'] else 'Unknown',
                                'body': issue.get('body') or '',
                                'type': 'RFC Tracking Issue',
                                'labels': labels
                            })
                except Exception as e:
                    print(f"    Date parsing error for community issue: {e}")
        
        elif 'API rate limit exceeded' in result.stderr:
            print(f"    Warning: GitHub API rate limit exceeded. RFC data unavailable.")
        else:
            print(f"    Error fetching RFCs: {result.stderr}")
        
    except Exception as e:
        print(f"    Error fetching community RFCs: {e}")
    
    return rfcs

def find_previous_update_date(wg_name):
    """Find the most recent update file for the working group and extract its date."""
    updates_dir = Path("toc/working-groups/updates")
    if not updates_dir.exists():
        return None
    
    # Look for files matching the pattern: YYYY-MM-DD-{wg_name}.md
    pattern = f"*-{wg_name}.md"
    update_files = list(updates_dir.glob(pattern))
    
    if not update_files:
        return None
    
    # Sort by filename (which starts with date) to get the most recent
    latest_file = sorted(update_files)[-1]
    
    # Extract date from filename
    filename = latest_file.name
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        try:
            date_str = date_match.group(1)
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print(f"Warning: Could not parse date from {filename}")
    
    return None

def main():
    parser = argparse.ArgumentParser(description='Extract raw working group repository activity data')
    
    # Support both old charter file format and new working group name format
    parser.add_argument('charter_or_wg', help='Path to working group charter file OR working group name (e.g., foundational-infrastructure)')
    parser.add_argument('target_date', nargs='?', help='Target date for report (YYYY-MM-DD, defaults to today)')
    parser.add_argument('--months', type=int, default=3, help='Number of months to look back from target date (default: 3, ignored if previous update found)')
    parser.add_argument('--output', help='Output file for raw activity data (default: tmp/{wg}_activity.json)')
    
    args = parser.parse_args()
    
    # Determine if this is a charter file or working group name
    if args.charter_or_wg.endswith('.md') or '/' in args.charter_or_wg:
        # This is a file path
        charter_file = args.charter_or_wg
        wg_name = Path(charter_file).stem
    else:
        # This is a working group name
        wg_name = args.charter_or_wg
        charter_file = f"toc/working-groups/{wg_name}.md"
        
        if not Path(charter_file).exists():
            print(f"Error: Working group charter not found at {charter_file}")
            print("Available working groups:")
            for wg_file in Path("toc/working-groups").glob("*.md"):
                if wg_file.stem not in ['WORKING-GROUPS']:
                    print(f"  - {wg_file.stem}")
            sys.exit(1)
    
    # Handle target date
    if args.target_date:
        try:
            target_date = datetime.strptime(args.target_date, '%Y-%m-%d')
        except ValueError:
            print(f"Error: Invalid date format '{args.target_date}'. Use YYYY-MM-DD")
            sys.exit(1)
    else:
        target_date = datetime.now()
    
    # Determine start date: check for previous updates first, then fallback to months
    previous_update_date = find_previous_update_date(wg_name)
    if previous_update_date:
        since_date = previous_update_date.replace(microsecond=0, tzinfo=None)
        print(f"Found previous update from {since_date.strftime('%Y-%m-%d')}, using as start date")
    else:
        # Calculate date range (using timezone-naive datetime)
        since_date = target_date.replace(microsecond=0, tzinfo=None) - timedelta(days=args.months * 30)
        print(f"No previous update found, using {args.months} months lookback")
    
    print(f"Extracting activity data for {wg_name} working group")
    print(f"Fetching activity since {since_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Extract configuration from charter
    config = extract_repos_from_charter(charter_file)
    if not config:
        sys.exit(1)
    
    # Collect all repositories
    all_repos = []
    for area in config.get('areas', []):
        repos = area.get('repositories', [])
        for repo in repos:
            all_repos.append({
                'repository': repo,
                'area': area.get('name', 'Unknown')
            })
    
    print(f"Found {len(all_repos)} repositories across {len(config.get('areas', []))} areas")
    
    # Generate activity report
    wg_activity = {
        'working_group': wg_name,
        'generated_at': datetime.now().isoformat(),
        'period_start': since_date.isoformat(),
        'period_end': target_date.isoformat(),
        'areas': []
    }
    
    total_commits = 0
    total_prs = 0
    total_issues = 0
    total_releases = 0
    
    for area in config.get('areas', []):
        print(f"\nProcessing area: {area.get('name', 'Unknown')}")
        area_data = {
            'name': area.get('name', 'Unknown'),
            'repositories': []
        }
        
        repos = area.get('repositories', [])
        for repo in repos:
            activity = get_repo_activity_graphql(repo, since_date)
            area_data['repositories'].append(activity)
            
            total_commits += len(activity['commits'])
            total_prs += len(activity['pull_requests'])
            total_issues += len(activity['issues'])
            total_releases += len(activity['releases'])
        
        wg_activity['areas'].append(area_data)
    
    # Fetch RFCs from community repo
    print(f"\nFetching RFCs from cloudfoundry/community...")
    rfcs = get_community_rfcs(since_date)
    wg_activity['rfcs'] = rfcs
    
    print(f"\nTotal activity found:")
    print(f"  Commits: {total_commits}")
    print(f"  Pull Requests: {total_prs}")
    print(f"  Issues: {total_issues}")
    print(f"  Releases: {total_releases}")
    print(f"  RFCs: {len(rfcs)}")
    
    # Set default output path
    if not args.output:
        args.output = f"tmp/{wg_name}_activity.json"
    
    # Output raw activity data
    output_data = json.dumps(wg_activity, indent=2, default=str)
    with open(args.output, 'w') as f:
        f.write(output_data)
    print(f"\nRaw activity data written to {args.output}")
    
    return args.output

if __name__ == '__main__':
    main()