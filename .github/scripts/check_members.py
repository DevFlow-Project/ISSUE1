import os
import requests
import json

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = os.environ['ORG_NAME']
REPO_NAME = os.environ['REPO_NAME']
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_org_members():
    response = requests.get(
        f"https://api.github.com/orgs/{ORG_NAME}/members",
        headers=HEADERS
    )
    response.raise_for_status()
    return [member['login'] for member in response.json()]

def create_issue(username):
    issue_title = f"🎉 New member joined: {username}"
    issue_body = f"Welcome @{username} to the organization!"
    response = requests.post(
        f"https://api.github.com/repos/{ORG_NAME}/{REPO_NAME}/issues",
        headers=HEADERS,
        json={"title": issue_title, "body": issue_body}
    )
    response.raise_for_status()

def main():
    new_members = get_org_members()

    if os.path.exists("members.json"):
        with open("members.json", "r") as f:
            old_members = json.load(f)
    else:
        old_members = []

    joined = list(set(new_members) - set(old_members))

    for user in joined:
        create_issue(user)

    with open("members.json", "w") as f:
        json.dump(new_members, f)

if __name__ == "__main__":
    main()
