import argparse
from github import Github
from collections import Counter

def main(access_token):
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("access_token")
    args = parser.parse_args()
    main(args.access_token)
