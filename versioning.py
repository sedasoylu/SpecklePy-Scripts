from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api.wrapper import StreamWrapper
import pandas as pd

# Speckle Project ID
project_id = "31f8cca4e0"

# Authenticate
client = SpeckleClient(host="macad.speckle.xyz")
account = get_default_account()
client.authenticate_with_account(account)

# Get the Project
project = client.project.get(project_id)

# Get Branch List to Extract IDs
branches = client.branch.list(project_id, 100)
branch_id_map = {branch.name: branch.id for branch in branches}  # Store Name → ID

# Get All Commits
commits = client.commit.list(project_id, 100)

# Extract Commit Data
commit_data = []
for commit in commits:
    commit_date = commit.createdAt.strftime("%d-%m-%Y")
    branch_name = commit.branchName
    branch_id = branch_id_map.get(branch_name, "")  # Get branch ID
    author = commit.authorName
    message = commit.message
    software = commit.sourceApplication

    commit_info = {
        "commit_id": commit.id,
        "author": author,
        "software": software,
        "date": commit_date,
        "message": message,
        "branch": branch_name,
        "branch_id": branch_id,  # Add branch ID
    }
    commit_data.append(commit_info)

# Convert to DataFrame & Save
commit_df = pd.DataFrame(commit_data)
commit_df['date'] = pd.to_datetime(commit_df['date'], format="%d-%m-%Y")
commit_df = commit_df.sort_values(by=['branch', 'date'])
commit_df.to_csv("commit_data.csv", index=False)

print("Commit data exported with branch IDs.")