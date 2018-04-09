import argparse
import json
import requests
import collections
import re

# "2018-03-25T22:43:52Z"

class Foo():
    def __init__(self):
        self.counter = collections.Counter()
        self.user_dict = {}
        self.seen_users = set()
        self.total_count = 0

    def process_results(self, json):
        for issue in json:
            date_match = re.fullmatch('(\d*)-(\d*)-.*', issue["created_at"])
            date = (date_match.group(1), date_match.group(2))
            user = issue["user"]["login"]

            if user not in self.seen_users:
                self.counter[date] += 1
                self.user_dict[date] = self.user_dict.get(date, []) + [user]
                self.seen_users.add(user)
                print("New User: " + user)

            self.total_count += 1

    def parse_pages(self, headers):
        return dict(
            [(rel[6:-1], url[url.index('<') + 1:-1]) for url, rel in
             [link.split(';') for link in
              headers['link'].split(',')]])

    def main(self, access_token):
        auth_dict = { "direction" : "asc", "access_token" : access_token }
        r = requests.get("https://api.github.com/repos/allenai/allennlp/issues", {**{"state": "all"}, **auth_dict})
        self.process_results(json.loads(r.content))

        if 'link' in r.headers:
            pages = self.parse_pages(r.headers)
            page = 0
            while 'last' in pages and 'next' in pages:
                page += 1
                print(page)
                print(pages['next'])
                print(pages['last'])
                r = requests.get(pages['next'], {**{"page" : str(page)}, **auth_dict})
                self.process_results(json.loads(r.content))
                pages = self.parse_pages(r.headers)
                if pages['next'] == pages['last']:
                    break

        print(self.total_count)
        for item in sorted(self.counter.items(), key = lambda x: x[0]):
            print(item)
            print(self.user_dict[item[0]])

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
    parser.add_argument("access_token")
    args = parser.parse_args()
    Foo().main(args.access_token)
