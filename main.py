from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from specklepy.api.client import SpeckleClient
from specklepy.api import operations

# Identify the Project and Model
project_id = "31f8cca4e0"
model_id = "bb2b38e5f9"

# Set up authentication and connection to server
client = SpeckleClient(host = "macad.speckle.xyz")
account = get_default_account()
client.authenticate_with_account(account)
transport = ServerTransport(project_id, client)

# Get the Model
facade_model = client.model.get( model_id = model_id, project_id = "28a211b286")
print(facade_model.name)

# Get the Referenced Object ID of the latest Version
versions = client.version.get_versions(model_id, project_id)
referenced_obj_id = versions.items[0].referencedObject

# Receive the referenced object (speckle object!)
print("Fetching data from the server...")
objData = operations.receive(referenced_obj_id, transport)
print("Got the data!")

# Print some properties
speckle_object = objData["@Data"]
child_obj = speckle_object["@{0;0}"][0]
obj_properties = child_obj.get_member_names()
print(obj_properties)

surface_south = child_obj["tot surf South"]
print(surface_south)