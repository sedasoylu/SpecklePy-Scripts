

from specklepy.api.wrapper import StreamWrapper
from specklepy.api import operations


project_url = "https://macad.speckle.xyz/projects/28a211b286/models/7d23073c7b"

# Set up the wrapper, client and transport
wrapper = StreamWrapper(project_url)
client = wrapper.get_client()
transport = wrapper.get_transport()

# Find a specific Model
branch = client.branch.get(wrapper.stream_id, name="facade")
print("The branch is: " + str(branch))