import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

# Define the update expression and attribute values
update_expression = "SET #lvl = :new_level"
expression_attribute_names = {'#lvl': 'level'}

# Define the table name
table_name = 'programs'

# Scan the table and update the matching items
response = dynamodb.scan(
    TableName=table_name,
    ProjectionExpression='id, #lvl',
    ExpressionAttributeNames = expression_attribute_names
)

sorted_list = sorted(response['Items'], key=lambda k: int(k['level']['N']), reverse=True)

for item in sorted_list:
    program_id = item['id']['S']
    current_level = int(item['level']['N'])
    
    if current_level >= 15:
        new_level = current_level + 3
    elif current_level >= 13:
        new_level = current_level + 2
    elif current_level >= 12:
        new_level = current_level + 1
    else:
        continue

    attribute_values = {':new_level': {'N': str(new_level)}}
    dynamodb.update_item(
        TableName=table_name,
        Key={
            'id': {'S': program_id}
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=attribute_values,
        ExpressionAttributeNames=expression_attribute_names
    )
