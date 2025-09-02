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

Please follow these steps:

1. **Extract Raw Activity Data**
   - Execute: `python3 scripts/extract_wg_activity.py {wg_name} {target_date}`
   - This will generate a JSON file with raw GitHub activity data at `tmp/{wg_name}_activity.json`
   - The data includes commits, PRs, issues, releases, and RFCs for all repositories in the working group

2. **Analyze the Working Group Charter**
   - Read the working group charter from `toc/working-groups/{wg_name}.md`
   - Parse the YAML frontmatter to understand the working group's mission and scope
   - Note the working group leads to avoid highlighting them in the report (no self-praise)

3. **Analyze Raw Activity Data for Strategic Insights**
   Using the raw JSON data from step 1, analyze and identify:
   - **Major Features & Initiatives**: Look for PRs with significant impact, multiple comments, or strategic themes
   - **Cross-Repository Collaboration**: Find related work spanning multiple repositories
   - **Key Contributors**: Identify active non-lead contributors and their organizations
   - **Technology Themes**: Detect patterns like security improvements, infrastructure modernization, IPv6, etc.
   - **Community Impact**: Assess how changes benefit the broader Cloud Foundry ecosystem

4. **Analyze Existing Report Templates**
   - Look for existing reports in `toc/working-groups/updates/` to understand format and style
   - Use the most recent report for the same working group as a template if available
   - Follow established patterns for structure, tone, and technical depth

5. **Filter RFCs for Working Group Relevance**
   - From the RFC data in the JSON, identify RFCs most relevant to this working group
   - Consider working group labels, keywords related to the WG's scope, and organizational changes

6. **Create Community-Focused Strategic Report**
   Generate a markdown report at `toc/working-groups/updates/{target_date}-{wg_name}.md` with:
   
   **Report Structure:**
   - **Title**: "{wg_name.replace('-', ' ').title()} Working Group Update"
   - **Frontmatter**: Include title, date, and period
   - **Summary**: Single paragraph high-level overview emphasizing community collaboration and strategic direction
     - **Major Initiatives**: 
       * Focus on completed and in-progress strategic work
       * Highlight specific contributors and their organizations (avoid WG leads)
       * **Include contributor GitHub profile links**: Use format [Name](https://github.com/username)
       * **Integrate PR/Issue links directly in text**: Link specific work to PRs/issues inline within descriptions
       * **Include relevant RFCs**: Integrate RFC developments within appropriate initiatives
       * **Limit each initiative to exactly 2 paragraphs** for conciseness and focus
       * **Keep paragraphs short**: Maximum 40 words per paragraph for readability
       * Do NOT include separate "Related Work" sections - all links should be integrated into the text
   - **Looking Forward**: Opportunities for community involvement

7. **Apply Community-Focused Writing Guidelines**
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
   - **Strategic Themes**: Highlight platform-wide improvements and modernization efforts
   - **Concise Format**: Each major initiative must be exactly 2 paragraphs, maximum 40 words per paragraph

**Key Success Criteria:**
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