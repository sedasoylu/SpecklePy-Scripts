from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from specklepy.api.client import SpeckleClient
from specklepy.api import operations
from specklepy.objects.base import Base
from specklepy.core.api.inputs.version_inputs import CreateVersionInput

# Identify the Project and Model
project_id = "31f8cca4e0"
model_id = "bb2b38e5f9"

# Set up authentication and connection to server
client = SpeckleClient(host ="macad.speckle.xyz")
account = get_default_account()
client.authenticate_with_account(account)
transport = ServerTransport(project_id, client)

# Get a list of active projects
projects = client.active_user.get_projects(limit=3)
for project in projects.items:
    print(project.name)

# Get a specific Model by ID
my_model = client.model.get(model_id, project_id)
print(my_model.name)

# Get the Referenced Object ID of the latest Version
versions = client.version.get_versions(model_id, project_id)
referenced_obj_id = versions.items[0].referencedObject

# Receive the referenced object (speckle object!)
print("Fetching data from the server...")
objData = operations.receive(referenced_obj_id, transport)
print("Got the data!")

# Navigate down the structure of a speckle object
for attribute_name in objData.get_member_names():
    attribute = getattr(objData, attribute_name)
    print(type(attribute))
    if isinstance(attribute, Base):
        test = attribute.get_member_names() 
        print(test)
       # we could go on and on, deeper into the object nested structure

# Get a property
# Look at the structure on the viewer so you know what keys to use
speckle_object = objData["@Data"]
child_obj = speckle_object["@{0;0}"][0]

all_properties = child_obj.get_member_names()
typed_properties = child_obj.get_typed_member_names()
dynamic_properties = child_obj.get_dynamic_member_names()

surface_south = child_obj["tot surf South"]
print(surface_south)

# Check if a property exists
if "SomeProp" not in all_properties:
    print("Couldnt find SomeProp!")

# Add a new property and push back to speckle
child_obj["MyProp"] = "JustATest"

# Send it to the server to get an object Id
send_transport = ServerTransport("f778fc7012", client) #sending to a different project/model
hash = operations.send(base=child_obj, transports=[send_transport])

# Create the actual commit that references this object
version_data = CreateVersionInput(objectId=hash, modelId="c17a9be343", projectId="f778fc7012")
client.version.create(version_data)
