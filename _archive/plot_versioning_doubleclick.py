# If this throws a Module Error, install dependencies:
# pip install pandas plotly

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Check if the filtered commit data file exists
file_path = "commit_data.csv"
if not os.path.exists(file_path):
    print("Error: commit_data.csv not found. Run versioning.py first.")
    exit()

# Import the CSV created in versioning.py
df = pd.read_csv(file_path)

# Ensure the file is not empty
if df.empty:
    print("Error: The commit file is empty. No data to plot.")
    exit()

# Convert date to datetime format
df['date'] = pd.to_datetime(df['date'])

# **Filter branches that contain 'services' in their name**
branches_with_services = df[df['branch'].str.contains("services", case=False, na=False)]['branch'].unique()
df = df[df['branch'].isin(branches_with_services)]

# **Check if there are branches left after filtering**
if df.empty:
    print("No branches contain 'services' in their name. Exiting script.")
    exit()

# Assign a unique y value to each branch for better grouping
branch_mapping = {branch: i for i, branch in enumerate(df['branch'].unique())}
df['y_value'] = df['branch'].map(branch_mapping)

# Create an **enhanced** interactive commit timeline visualization
fig = px.scatter(
    df,
    x="date",
    y="y_value",
    color="author",  # Different colors for different authors
    size_max=10,
    hover_data=["message", "software"],  # Display commit messages
    title="Commit History (Filtered for Branches Containing 'services')",
    labels={"y_value": "Branch", "date": "Commit Date"},
)

# Add vertical bars for each commit date to show frequency
for branch, group in df.groupby("branch"):
    fig.add_trace(go.Scatter(
        x=group['date'],
        y=group['y_value'],
        mode="lines+markers",
        marker=dict(size=8, symbol="circle"),
        name=branch,
        hoverinfo="text",
        text=group['message'],
    ))

# Improve the layout and styling
fig.update_layout(
    xaxis_title="Commit Date",
    yaxis_title="Branch",
    yaxis=dict(
        tickvals=list(branch_mapping.values()),
        ticktext=list(branch_mapping.keys()),
        gridcolor="lightgrey",
    ),
    plot_bgcolor="rgba(0, 0, 0, 0)",
    legend_title="Author",
    hovermode="x unified",  # Shows all commit details when hovering on a date
)

# Show the interactive plot
fig.show()