from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account, get_local_accounts
from specklepy.api import operations
from specklepy.transports.server import ServerTransport
from specklepy.serialization.base_object_serializer import BaseObjectSerializer
import json

hyper = "https://macad.speckle.xyz/projects/28a211b286/models/7d23073c7b"
# initialise the client
client = SpeckleClient(host="macad.speckle.xyz")
SpeckleClient()
# authenticate the client
accounts = get_local_accounts()
account = get_default_account()

client.authenticate_with_account(account)

stream_id = "28a211b286"  #  stream ID
object_id = "fbe9b88c1146f0ce7a3fb53ad7b09491"  # Model ID

transport = ServerTransport(stream_id, client)
data = operations.receive(object_id, remote_transport=transport)  # get the top level Collection

types_referenceId = data["@Types"].id  # here you get the referenceID from @Types in order to access the "@facade", "@columns", etc...

types_data = operations.receive(types_referenceId, remote_transport=transport)

serializer = BaseObjectSerializer()
json_data = serializer.write_json(types_data)

print(json_data)