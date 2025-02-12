from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from specklepy.api.client import SpeckleClient
from specklepy.api import operations

# Identify the Project and Model
project_id = "28a211b286"
facade_model_id = "7d23073c7b"

# Set up authentication and connection to server
client = SpeckleClient(host = "macad.speckle.xyz")
account = get_default_account()
client.authenticate_with_account(account)
transport = ServerTransport(project_id, client)

# Get the Model
facade_model = client.model.get( model_id = facade_model_id, project_id = "28a211b286")
print(facade_model.name)

# Get the Referenced Object ID of the latest Version
versions = client.version.get_versions(facade_model_id, project_id)
referenced_obj_id = versions.items[0].referencedObject

# Receive the referenced object (speckle object!)
objData = operations.receive(referenced_obj_id, transport)
elements = objData.elements

# Print some properties
for element in elements:
    print("Here are some properties")
