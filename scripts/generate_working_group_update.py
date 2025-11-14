#!/usr/bin/env python3
"""
Cloud Foundry Working Group Update Generator - OpenCode Run Integration

This script generates comprehensive working group activity reports by:
1. Using extract_wg_activity.py to extract raw GitHub data
2. Calling OpenCode Run with a structured prompt to analyze the data
3. Generating strategic, community-focused reports for TOC consumption

The approach separates data extraction from analysis, allowing OpenCode Run's 
AI capabilities to provide intelligent interpretation of raw GitHub activity.

Usage:
    python generate_working_group_update.py <working_group_name> [date]

Examples:
    python generate_working_group_update.py foundational-infrastructure
    python generate_working_group_update.py app-runtime-platform 2025-08-15

Requirements:
- OpenCode CLI installed and available in PATH
- GitHub CLI (gh) installed and authenticated with GitHub
- Network access to GitHub API

The script leverages OpenCode Run's AI capabilities to transform raw data into
strategic insights that celebrate community collaboration and technical achievements.
"""

import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

def check_opencode_available():
    """Check if OpenCode CLI is available."""
    try:
        result = subprocess.run(['opencode', '--version'], 
                              capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def validate_working_group(wg_name):
    """Validate that the working group exists."""
    valid_wgs = [
        'foundational-infrastructure', 'app-runtime-platform', 
        'app-runtime-deployments', 'app-runtime-interfaces',
        'cf-on-k8s', 'concourse', 'docs', 'paketo',
        'service-management', 'vulnerability-management'
    ]
    
    if wg_name not in valid_wgs:
        print(f"Error: Unknown working group '{wg_name}'")
        print(f"Available working groups: {', '.join(valid_wgs)}")
        return False
    
    # Check if charter file exists
    charter_path = Path(f"toc/working-groups/{wg_name}.md")
    if not charter_path.exists():
        print(f"Error: Working group charter not found at {charter_path}")
        return False
    
    return True

def validate_date(date_str):
    """Validate date format."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD")
        return False

def generate_opencode_prompt(wg_name, target_date=None):
    """Generate the OpenCode Run prompt for working group analysis."""
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')
    
    prompt = f"""I need to generate a Cloud Foundry working group activity update report for the {wg_name} working group that celebrates community collaboration and strategic initiatives.

**Raw Activity Data Available:**
The file `tmp/{wg_name}_activity.json` contains comprehensive GitHub activity data for this working group, extracted for the period ending {target_date}. This JSON file has the following structure:

```json
{{
  "working_group": "working-group-name",
  "period_end": "YYYY-MM-DD", 
  "repositories": [
    {{
      "name": "org/repo-name",
      "commits": [
        {{
          "sha": "commit-hash",
          "author": "username",
          "date": "YYYY-MM-DD",
          "message": "commit message",
          "url": "github-url"
        }}
      ],
      "pull_requests": [
        {{
          "number": 123,
          "title": "PR title",
          "author": "username", 
          "state": "open|closed|merged",
          "created_at": "YYYY-MM-DD",
          "url": "github-url",
          "comments": 5
        }}
      ],
      "issues": [
        {{
          "number": 456,
          "title": "Issue title",
          "author": "username",
          "state": "open|closed",
          "created_at": "YYYY-MM-DD", 
          "url": "github-url",
          "comments": 3
        }}
      ],
      "releases": [
        {{
          "tag_name": "v1.2.3",
          "name": "Release Name",
          "published_at": "YYYY-MM-DD",
          "url": "github-url"
        }}
      ]
    }}
  ],
  "rfcs": [
    {{
      "number": "rfc-0001",
      "title": "RFC Title", 
      "status": "accepted|draft|withdrawn",
      "authors": ["author1", "author2"],
      "url": "github-url"
    }}
  ]
}}
```

**Analysis Instructions:**

 1. **Analyze Raw Activity Data with jq**
    - Use `jq` commands to extract and analyze the JSON data from `tmp/{wg_name}_activity.json`
    - **PRIORITIZE RFC-RELATED ACTIVITY**: Give highest priority to PRs, issues, and commits related to RFCs
    - Identify major features, cross-repository collaboration, key contributors, and technology themes
    - Look for patterns in commit messages, PR titles, and issue descriptions that mention RFCs
    - Find related work spanning multiple repositories, especially RFC implementations

2. **Analyze the Working Group Charter**
   - Read the working group charter from `toc/working-groups/{wg_name}.md`
   - Parse the YAML frontmatter to understand the working group's mission and scope
   - Note the working group leads to avoid highlighting them in the report (no self-praise)

3. **Analyze Existing Report Templates**
   - Look for existing reports in `toc/working-groups/updates/` to understand format and style
   - Use the most recent report for the same working group as a template if available
   - Follow established patterns for structure, tone, and technical depth

 4. **Filter and Prioritize RFCs for Working Group Relevance**
    - From the RFC data in the JSON, identify RFCs most relevant to this working group
    - **MANDATORY**: Include all in-progress RFCs that affect this working group
    - Consider working group labels, keywords related to the WG's scope, and organizational changes
    - Give RFC-related PRs and implementation work top priority in the analysis

5. **Create Community-Focused Strategic Report**
   Generate a markdown report at `toc/working-groups/updates/{target_date}-{wg_name}.md` with:
   
   **Report Structure:**
   - **Title**: "{wg_name.replace('-', ' ').title()} Working Group Update"
   - **Frontmatter**: Include title, date, and period
     - **Major Initiatives**: 
       * Focus on completed and in-progress strategic work
       * Highlight specific contributors and their organizations (avoid WG leads)
       * **Include contributor GitHub profile links**: Use format [Name](https://github.com/username)
       * **Integrate PR/Issue links directly in text**: Link specific work to PRs/issues inline within descriptions
        * **Include RFC coverage as top priority**: Always mention in-progress RFCs relevant to the working group
        * **Prioritize RFC-related activity**: Give highest priority to PRs, issues, and commits related to RFCs
       * **Limit each initiative to exactly 3 paragraphs** for conciseness and focus
       * **Keep paragraphs short**: Maximum 40 words per paragraph for readability
       * Do NOT include separate "Related Work" sections - all links should be integrated into the text

6. **Apply Community-Focused Writing Guidelines**
   - **Celebrate Collaboration**: Emphasize how contributors from different organizations work together
   - **Avoid Self-Praise**: Never highlight working group leads when they're giving the update
   - **Focus on Impact**: Prioritize "why this matters" over "what was done"
   - **Technical Depth**: Provide substantial detail about major initiatives
   - **Comprehensive Linking**: Link to specific PRs, issues, and related work throughout
   - **Issue Format**: Use descriptive links primarily, with shorthand format: `[Description](url) - org/repo#number`
   - **No Duplicate Links**: Never link to the same PR/issue twice within the same paragraph
   - **Prefer Descriptive Links**: Use PR change descriptions as link text rather than repo#PR format
   - **Inline Integration**: Integrate all PR/issue links directly into descriptive text, not in separate sections
   - **Community Language**: Use open-source, collaborative terminology rather than business speak
    - **RFC Priority**: Always include in-progress RFCs and prioritize RFC-related activity highest
   - **Concise Format**: Each major initiative must be exactly 2 paragraphs, maximum 40 words per paragraph

**Key Success Criteria:**
- **RFC Coverage**: All in-progress RFCs relevant to the working group are prominently featured
- **RFC Activity Priority**: RFC-related PRs, issues, and commits receive top priority in analysis
- Major technical achievements are prominently featured with detailed context
- Non-lead contributors are recognized inline with GitHub profile links: [Name](https://github.com/username)
- Cross-organizational collaboration is highlighted
- Strategic themes (IPv6, security, modernization) are clearly articulated
- All PR/Issue links use descriptive text and avoid duplication within paragraphs
- Report reads as a celebration of open-source innovation
- Technical depth demonstrates the working group's strategic impact

Generate a comprehensive report that helps the TOC understand both the technical progress and collaborative community dynamics of this working group."""

    return prompt

def run_opencode_analysis(wg_name, target_date=None):
    """Execute OpenCode Run with the generated prompt."""
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Generating working group update for {wg_name} (target date: {target_date})")
    
    # First, extract raw activity data
    print("Extracting raw activity data...")
    activity_file = Path(f"tmp/{wg_name}_activity.json")
    activity_file.parent.mkdir(exist_ok=True)
    
    try:
        result = subprocess.run(['python3', 'scripts/extract_wg_activity.py', wg_name, target_date], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Raw activity data extracted: {activity_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting activity data: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return None
    
    # Check if activity file was generated
    if not activity_file.exists():
        print(f"Error: Activity file not found at {activity_file}")
        return None
    
    print("Running OpenCode analysis...")
    
    prompt = generate_opencode_prompt(wg_name, target_date)
    
    try:
        # Run OpenCode with the generated prompt
        result = subprocess.run(['opencode', 'run', prompt], 
                              capture_output=False, text=True, check=True)
        
        # Check if the expected report was generated
        expected_report = Path(f"toc/working-groups/updates/{target_date}-{wg_name}.md")
        if expected_report.exists():
            print(f"✅ Working group update generated: {expected_report}")
            return str(expected_report)
        else:
            print(f"⚠️  OpenCode analysis completed, but report not found at expected location: {expected_report}")
            print("The report may have been generated with a different filename or date.")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"Error running OpenCode analysis: {e}")
        return None

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h', 'help']:
        print("Usage: python generate_working_group_update.py <working_group_name> [date]")
        print("\nAvailable working groups:")
        print("- foundational-infrastructure")
        print("- app-runtime-platform") 
        print("- app-runtime-deployments")
        print("- app-runtime-interfaces")
        print("- cf-on-k8s")
        print("- concourse")
        print("- docs")
        print("- paketo")
        print("- service-management")
        print("- vulnerability-management")
        print("\nExamples:")
        print("  python generate_working_group_update.py foundational-infrastructure")
        print("  python generate_working_group_update.py app-runtime-platform 2025-08-15")
        print("\nRequirements:")
        print("- OpenCode CLI installed and available in PATH")
        print("- GitHub CLI (gh) installed and authenticated with GitHub")
        print("\nSee toc/working-groups/updates/README.md for detailed documentation.")
        sys.exit(0)
    
    if not check_opencode_available():
        print("Error: OpenCode CLI not found in PATH")
        print("Please install OpenCode CLI: https://github.com/sst/opencode")
        print("Or use the core analysis script directly: python3 scripts/extract_wg_activity.py")
        sys.exit(1)
    
    # Validate arguments
    wg_name = sys.argv[1]
    if not validate_working_group(wg_name):
        sys.exit(1)
    
    target_date = sys.argv[2] if len(sys.argv) > 2 else None
    if target_date and not validate_date(target_date):
        sys.exit(1)
    
    # Run the analysis
    report_path = run_opencode_analysis(wg_name, target_date)
    
    if report_path:
        print(f"\n🎉 Working group update completed!")
        print(f"📄 Report: {report_path}")
        print(f"📁 All reports: toc/working-groups/updates/")
    else:
        print(f"\n⚠️  Analysis completed but report location unclear")
        print(f"Check toc/working-groups/updates/ for generated files")

if __name__ == "__main__":
    main()