import pandas as pd
import plotly.graph_objects as go
import os

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

# Apply "services" Filter
df = df[df['branch'].str.contains("services", case=False, na=False)]
if df.empty:
    print("No branches contain 'services' in their name. Exiting script.")
    exit()

# Speckle Project ID
project_id = "31f8cca4e0"

# Generate Speckle Branch URLs
df["branch_url"] = df.apply(lambda row: f"https://macad.speckle.xyz/projects/{project_id}/models/{row['branch_id']}", axis=1)

# Assign Unique Y Values to Filtered Branches
branch_mapping = {branch: i for i, branch in enumerate(df['branch'].unique())}
df['y_value'] = df['branch'].map(branch_mapping)

# Get unique committers and assign unique symbols
committers = df['author'].unique()
symbol_mapping = {author: symbol for author, symbol in zip(committers, ["circle", "square", "diamond", "triangle-up", "triangle-down", "star"])}  # More symbols if needed

# Create Figure
fig = go.Figure()

# Add Commit Markers for Each Branch (Branches in Legend)
for branch, branch_df in df.groupby("branch"):
    y_value = branch_mapping[branch]  # Get Y position for the branch

    # Add commit markers (dots) for each branch (no lines)
    fig.add_trace(go.Scatter(
        x=branch_df["date"],
        y=[y_value] * len(branch_df),  # Keep Y constant per branch
        mode="markers",
        name=f"Branch: {branch}",  # Only branches appear in the legend
        legendgroup=branch,  # Group branches separately
        marker=dict(size=10, symbol="circle"),  # Dots only, no lines
        hovertext=branch_df.apply(lambda row: f"Branch: {row['branch']}<br>Commit: {row['message']}", axis=1),
        hoverinfo="text",
        visible=True,  # Ensure branches are visible by default
    ))

# Add Commit Markers for Each Committer (Hidden by Default)
for author, author_df in df.groupby("author"):
    fig.add_trace(go.Scatter(
        x=author_df["date"],
        y=author_df["y_value"],  # Match Y position with branch
        mode="markers",
        name=f"Committer: {author}",  # Separate committers in the legend
        legendgroup="committers",  # Separate group for committers
        marker=dict(size=10, symbol=symbol_mapping.get(author, "circle")),  # Unique marker symbols for committers
        hovertext=author_df.apply(lambda row: f"Branch: {row['branch']}<br>Committer: {row['author']}<br>Message: {row['message']}", axis=1),
        hoverinfo="text",
        visible="legendonly",  # Committers are hidden until selected
    ))

# Make Branch Titles Clickable in the Legend
for branch, y_value in branch_mapping.items():
    branch_url = df[df['branch'] == branch]['branch_url'].values[0]
    fig.add_annotation(
        x=df["date"].min() - pd.Timedelta(days=5),
        y=y_value,
        text=f"<a href='{branch_url}' target='_blank' style='color:black'>{branch}</a>",
        showarrow=False,
        xanchor="right",
        align="right",
        font=dict(size=8)
    )

# Adjust Layout to Ensure Fixed Positions and Prevent Movement
fig.update_layout(
    xaxis_title="Commit Date",
    yaxis_title="Branch",
    xaxis=dict(
        range=[df["date"].min() - pd.Timedelta(days=10), df["date"].max() + pd.Timedelta(days=10)],
        fixedrange=True
    ),
    yaxis=dict(
        tickvals=list(branch_mapping.values()),
        ticktext=[],  # Hide duplicate labels since clickable names are added
        gridcolor="lightgrey",
        range=[min(branch_mapping.values()) - 1, max(branch_mapping.values()) + 1],
        fixedrange=True
    ),
    margin=dict(l=150),  # Reduce left margin to keep labels visible
    plot_bgcolor="rgba(0, 0, 0, 0)",
    legend_title="Filter by Branch & Committer",  # Legend now has both
    hovermode="x unified",
)

# Show Interactive Plot
fig.show()
