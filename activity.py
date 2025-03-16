from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
import pandas as pd

# Authenticate
client = SpeckleClient(host="macad.speckle.xyz")
account = get_default_account()
client.authenticate_with_account(account)

# Define the project ID (same as stream ID)
project_id = "31f8cca4e0"

# Get activity logs related to model downloads
activities = client.activity.list(project_id, limit=200)  # Get latest 200 events

# Extract relevant data
download_data = []

for activity in activities:
    if "retrieved" in activity.actionMessage.lower():  # Look for retrieval events
        download_info = {
            "model_id": activity.resourceId,
            "user": activity.userName,
            "date": activity.time
        }
        download_data.append(download_info)

# Convert to DataFrame
download_df = pd.DataFrame(download_data)

# Save to CSV
download_df.to_csv("model_downloads.csv", index=False)

print(download_df.to_string())
print("Model download history saved!")
