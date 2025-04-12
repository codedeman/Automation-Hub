import requests
import pandas as pd
import urllib.parse
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔹 Replace with your GitLab personal access token
GITLAB_TOKEN = ""
# 🔹 List of GitLab projects
PROJECTS = [
    "phamtrungkiendev/plugin_architecture"
]

# 🔹 Google Sheet info
SHEET_ID = "1FV0sPRBVDkzdnt7RhFpNZ2TyLrR79LURJ6K3K6uKGxw"
SHEET_NAME = "Sheet1"  # or whatever tab name you want

# GitLab API base
GITLAB_API = "https://gitlab.com/api/v4"

# 🔹 Get GitLab project ID
def get_project_id(project_path):
    encoded_path = urllib.parse.quote(project_path, safe="")
    url = f"{GITLAB_API}/projects/{encoded_path}"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('id')
    print(f"❌ Error: Unable to get project ID for {project_path}. Response: {response.text}")
    return None

# 🔹 Extract type from MR title
def extract_type_from_title(title):
    if title.startswith("[Bug]"):
        return "Bug"
    elif title.startswith("[Task]"):
        return "Task"
    elif title.startswith("[Story]"):
        return "Story"
    else:
        return "Other"

# 🔹 Fetch open MRs
def fetch_merge_requests(project_id, project_name):
    url = f"{GITLAB_API}/projects/{project_id}/merge_requests?state=opened&target_branch=main&per_page=100"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        merge_requests = response.json()
        result = []
        for mr in merge_requests:
            mr_type = extract_type_from_title(mr["title"])
            result.append({
                "Project": project_name,
                "Title": mr["title"],
                "URL": mr["web_url"],
                "Assignee": mr["assignee"]["name"] if mr.get("assignee") else "Unassigned",
                "Type": mr_type
            })
        return result
    print(f"❌ Error: Failed to fetch MRs for {project_name}. Response: {response.text}")
    return []

# 🔹 Authenticate with Google Sheets
def update_google_sheet(data):
    if not data:
        print("⚠️ No MR data to write to Google Sheet.")
        return

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

    df = pd.DataFrame(data)
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

    print("✅ Google Sheet updated!")

# 🔹 Main process
if __name__ == "__main__":
    all_merge_requests = []
    for project in PROJECTS:
        project_id = get_project_id(project)
        if project_id:
            all_merge_requests.extend(fetch_merge_requests(project_id, project))

    update_google_sheet(all_merge_requests)
