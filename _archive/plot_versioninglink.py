import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import webbrowser

# Load Data
file_path = "commit_data.csv"
if not os.path.exists(file_path):
    print("Error: commit_data.csv not found. Run versioning.py first.")
    exit()

df = pd.read_csv(file_path)
if df.empty:
    print("Error: The commit file is empty. No data to plot.")
    exit()

# Convert Date
df['date'] = pd.to_datetime(df['date'])

# **Apply "services" Filter**
df = df[df['branch'].str.contains("services", case=False, na=False)]
if df.empty:
    print("No branches contain 'services' in their name. Exiting script.")
    exit()

# **Speckle Project ID**
project_id = "31f8cca4e0"

# Generate Speckle Branch URLs
df["branch_url"] = df.apply(lambda row: f"https://macad.speckle.xyz/projects/{project_id}/models/{row['branch_id']}", axis=1)

# Assign Unique Y Values to Filtered Branches
branch_mapping = {branch: i for i, branch in enumerate(df['branch'].unique())}
df['y_value'] = df['branch'].map(branch_mapping)

# 🎯 **Create a Sidebar for Branch Names + Links (Filtered Branches Only)**
branch_links = pd.DataFrame({
    "branch": list(branch_mapping.keys()),
    "y_value": list(branch_mapping.values()),
    "branch_url": [f"https://macad.speckle.xyz/projects/{project_id}/models/{df[df['branch'] == branch]['branch_id'].values[0]}" for branch in branch_mapping.keys()]
})

# ✅ **Ensure the Legend Displays Branch Names Instead of Authors**
fig = px.scatter(
    df,
    x="date",
    y="y_value",
    color="branch",  # 🎯 Now grouped by branch names instead of author
    size_max=10,
    hover_data=["message", "software"],
    title="Commit History (Filtered for 'services' Branches, Click Names to Open)",
    labels={"y_value": "Branch", "date": "Commit Date"},
)

# ✅ **Place Clickable Branch Names on the Left of the Graph**
for _, row in branch_links.iterrows():
    fig.add_annotation(
        x=min(df["date"]),  # Position at the far left
        y=row["y_value"],
        text=f"<a href='{row['branch_url']}' target='_blank' style='color:black'>{row['branch']}</a>",  # Clickable branch name
        showarrow=False,
        xshift=-80,  # Adjust further left so it’s not on top of the graph
        font=dict(size=12)
    )

# ✅ **Allow Double Click to Isolate a Branch in the Legend**
fig.update_layout(
    xaxis_title="Commit Date",
    yaxis_title="Branch",
    yaxis=dict(
        tickvals=list(branch_mapping.values()),
        ticktext=[],  # Hide duplicate axis labels since we have clickable names
        gridcolor="lightgrey",
    ),
    plot_bgcolor="rgba(0, 0, 0, 0)",
    legend_title="Branch",  # 🎯 Now legend filters branches instead of authors
    hovermode="x unified",
)

# ✅ **Allow Clicking on Legend to Show Only One Branch**
fig.update_traces(marker=dict(symbol="circle"), selector=dict(mode="markers"))

# **Show Interactive Plot**
fig.show()
