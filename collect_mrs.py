
import requests
import pandas as pd
import urllib.parse

# 🔹 Replace with your GitLab personal access token
GITLAB_TOKEN = ""


# 🔹 List of project paths (namespace/project-name)
PROJECTS = [
    "phamtrungkiendev/plugin_architecture"
]

# GitLab API base URL
#https://gitlab.com/api/v4
GITLAB_API = ""

# Get project ID dynamically
def get_project_id(project_path):
    encoded_path = urllib.parse.quote(project_path, safe="")
    url = f"{GITLAB_API}/projects/{encoded_path}"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('id')

    print(f"❌ Error: Unable to get project ID for {project_path}. Response: {response.text}")
    return None

# Fetch open Merge Requests targeting 'main'
def fetch_merge_requests(project_id, project_name):
    url = f"{GITLAB_API}/projects/{project_id}/merge_requests?state=opened&target_branch=main"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        merge_requests = response.json()
        return [
            {
                "Project": project_name,
                "Title": mr["title"],
                "URL": mr["web_url"],
                "Assignee": mr["assignee"]["name"] if mr.get("assignee") else "Unassigned"
            }
            for mr in merge_requests
        ]

    print(f"❌ Error: Failed to fetch MRs for {project_name}. Response: {response.text}")
    return []

# Save MR details to an Excel file
def save_to_excel(mrs):
    if not mrs:
        print("⚠️ No open MRs found in any project!")
        return

    df = pd.DataFrame(mrs)
    output_file = "merge_requests.xlsx"
    df.to_excel(output_file, index=False)
    print(f"✅ Excel file generated: {output_file}")

if __name__ == "__main__":
    all_merge_requests = []

    for project in PROJECTS:
        project_id = get_project_id(project)
        if project_id:
            all_merge_requests.extend(fetch_merge_requests(project_id, project))

    save_to_excel(all_merge_requests)
