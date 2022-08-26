from website import dynamo

# Make sure we add the correct env variables
storage = dynamo.AwsDynamoStorage.from_env()
if not storage:
    print("Something went wrong with connecting to the AWS database...")
    exit(1)

# Get the correct tables
USERS = dynamo.Table(storage, 'users', 'username', indexed_fields=[dynamo.IndexKey('email')])
CLASSES = dynamo.Table(storage, 'classes', 'id', indexed_fields=[dynamo.IndexKey(v) for v in ['teacher', 'link']])

classes = CLASSES.scan()
print(classes)
