import argparse

from .org_management import OrgGenerator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CFF Managed Github Orgs Generator")
    parser.add_argument("-o", "--out", default="orgs.out.yml", help="output file for generated org configuration")
    parser.add_argument(
        "-b", "--branchprotection", default="branchprotection.out.yml", help="output file for generated branch protection rules"
    )
    args = parser.parse_args()

    print("Generating CFF Managed Github Org configuration.")
    generator = OrgGenerator()
    generator.load_from_project()
    if not generator.validate_repo_ownership():
        print("ERROR: Repository ownership is invalid. Refer to RFC-0007 and RFC-0036.")
        exit(1)
    generator.generate_org_members()
    generator.generate_teams()
    generator.generate_branch_protection()
    generator.write_org_config(args.out)
    generator.write_branch_protection(args.branchprotection)
