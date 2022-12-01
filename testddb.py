
import pprint
from website import dynamo, database

storage = dynamo.AwsDynamoStorage.from_env()
if not storage:
    raise RuntimeError('DDB not configure quickly')

Q = dynamo.Table(storage, 'preferences', partition_key='id', sort_key='level')

recs = database.USERS.get({'username': 'rix0rrr'})
pprint.pprint(recs)
