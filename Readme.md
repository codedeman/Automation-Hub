

## 🚀 Merge Request Tracker to Google Sheet

This script collects open Merge Requests (MRs) from GitLab and syncs them to a Google Sheet. Super useful for tracking bugs, tasks, and stories across projects — all in one place. 📊✨

---

### 📦 Requirements

You’ll need Python 3.8 or later.

#### Install dependencies:

```bash
pip install requests pandas gspread oauth2client
```

#### Libraries used:

| Library        | Purpose                                                                 |
|----------------|-------------------------------------------------------------------------|
| `requests`     | Makes HTTP requests to the GitLab API                                   |
| `pandas`       | Handles tabular data, making it easy to format and convert to spreadsheet |
| `gspread`      | Talks to Google Sheets API using Python                                 |
| `oauth2client` | Manages Google authentication via a service account                     |

---

### 🛠️ Setup

#### 1. GitLab Access Token

- Visit [GitLab → Access Tokens](https://gitlab.com/-/profile/personal_access_tokens)
- Create a token with the following **scopes**:
  - `read_api`
  - `read_repository`
- Add it to your script:
  ```python
  GITLAB_TOKEN = "your_personal_access_token"
  ```

#### 2. Google Sheets API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable:
   - **Google Sheets API**
   - **Google Drive API**
3. Create a **Service Account**:
   - Go to `IAM & Admin → Service Accounts`
   - Create one, and download the JSON key file
4. Save the file as `credentials.json` in the same directory as your script

#### 3. Grant Access to Your Google Sheet

- Open your Google Sheet
- Click **Share**
- Add the **client email** from `credentials.json` (e.g. `your-service@your-project.iam.gserviceaccount.com`)
- Set permission to **Editor**

#### 4. Define Sheet Info in Script

```python
SHEET_ID = "your_google_sheet_id_here"
SHEET_NAME = "Sheet1"  # or your tab name
```

To find the **Sheet ID**, grab it from the URL:
```
https://docs.google.com/spreadsheets/d/<< THIS IS YOUR ID >>/edit#gid=0
```

---

### ▶️ How to Run

Run the script with:

```bash
python collect_mrs.py
```

If everything is set up correctly, you’ll see:

```bash
✅ Google Sheet updated!
```

---

### ✅ What the Script Does

- Authenticates with GitLab and Google Sheets
- Pulls open MRs from the `main` branch
- Categorizes MRs by type (`[Bug]`, `[Task]`, `[Story]`)
- Updates the specified tab in your Google Sheet with:
  - Project name
  - MR title
  - URL
  - Assignee
  - Type

---
📌 Author
Kevin Pham
Mobile Engineer · Organic Enthusiast · Automation Lover
