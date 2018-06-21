import argparse
import json
import requests
import collections
import re

class GitHubStatistics():
    def process_contributions(self, contributions):
        if len(contributions) > 0:
            current_date = tuple(contributions[0]["date"])
            active_users = set()
            results = []
            for contribution in contributions:
                date = tuple(contribution["date"])
                user = contribution["user"]

                if date != current_date:
                    results.append((current_date, active_users))
                    current_date = date
                    active_users = set()

                active_users.add(user)
            results.append((current_date, active_users))

            return results

    def parse_pages(self, headers):
        return dict(
            [(rel[6:-1], url[url.index('<') + 1:-1]) for url, rel in
             [link.split(';') for link in
              headers['link'].split(',')]])

    def process_page(self, issues):
        contributions = []
        for issue in issues:
            date_match = re.fullmatch('(\d*)-(\d*)-.*', issue["created_at"])
            date = (date_match.group(1), date_match.group(2))
            user = issue["user"]["login"]
            issue_type = "issue"
            if "pull_request" in issue:
                issue_type = "pr"
            contributions.append({"date": date, "user": user, "type": issue_type})
            print(f"  {date}: {user}")
        return contributions


    def fetch_data(self, access_token):
        auth_dict = { "direction" : "asc", "access_token" : access_token }
        r = requests.get("https://api.github.com/repos/allenai/allennlp/issues", {**{"state": "all"}, **auth_dict})
        print(r.content)
        self.process_page(json.loads(r.content))
        contributions = []

        if 'link' in r.headers:
            pages = self.parse_pages(r.headers)
            page = 0
            while 'last' in pages and 'next' in pages:
                page += 1
                print(f"Processing page {page}...")
                r = requests.get(pages['next'], {**{"page" : str(page)}, **auth_dict})
                contributions += self.process_page(json.loads(r.content))
                pages = self.parse_pages(r.headers)
                if pages['next'] == pages['last']:
                    break

        return contributions

    def main(self, access_token, load, save, exclude_prs, exclude_issues):
        contributions = []
        if load:
            with open(load, "r") as fin:
                for line in fin.readlines():
                    contributions.append(json.loads(line))
        else:
            contributions = self.fetch_data(access_token)

        if exclude_prs:
            contributions = [c for c in contributions if c["type"] != "pr"]
        if exclude_issues:
            contributions = [c for c in contributions if c["type"] != "issue"]

        if save:
            with open(save, "w") as fout:
                for contribution in contributions:
                    fout.write(json.dumps(contribution) + "\n")

        monthly_active_contributors = self.process_contributions(contributions)

        print(len(contributions))
        for item in monthly_active_contributors:
            date = item[0]
            users = item[1]
            print(f"{date[0]}-{date[1]}\t{len(users)}")
            print(users)
            print()

    """
        g = Github(access_token)
        issues = g.get_repo("allenai/allennlp").get_issues(milestone="none", assignee="*", state="all")
        seen_users = set()
        counter = Counter()
        total_count = 0
        for issue in issues:
            date = issue.created_at

            user = issue.user.login
            if user not in seen_users:
                counter[(date.year, date.month)] += 1
                seen_users.add(user)
                print("Adding : " + user)
            else:
                print("Skipping : " + user)

            total_count += 1

        print(total_count)
        for item in sorted(counter.items(), key = lambda x: x[0]):
            print(item)
    """

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--access_token", required=False, default=None)
    parser.add_argument("--save", type=str, required=False, default=None)
    parser.add_argument("--load", type=str, required=False, default=None)
    parser.add_argument("--exclude-pull-requests", action='store_true', required=False, default=False)
    parser.add_argument("--exclude-issues", action='store_true', required=False, default=False)
    args = parser.parse_args()
    GitHubStatistics().main(args.access_token, load=args.load, save=args.save,
            exclude_prs=args.exclude_pull_requests,
            exclude_issues=args.exclude_issues)
