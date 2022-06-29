from website import dynamo

# Make sure we add the correct env variables
storage = dynamo.AwsDynamoStorage.from_env()
if not storage:
    print("Something went wrong with connecting to the AWS database...")
    exit(1)

# Get the correct table
table = dynamo.Table(storage, 'users', 'username', indexed_fields=[dynamo.IndexKey('email')])

page_token = None
# As long as we don't break (so there is no new page_token) -> keep iterating
while True:
    page = table.scan(pagination_token=page_token)
    for user in page:
        table.update({'username': user.get('username')}, {'epoch': 1})
    page_token = page.next_page_token
    if not page_token:
        break
