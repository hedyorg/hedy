import boto3
db3 = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', aws_secret_access_key='ticTacToeSampleApp', aws_access_key_id='ticTacToeSampleApp', region_name='us-west-2')
db3.create_table(
    TableName= 'test-users',
    KeySchema=[
        {
            'AttributeName': "username", 
            'KeyType': "HASH"
        }

    ],
    AttributeDefinitions=[
        { 
            'AttributeName': "username", 
            'AttributeType': "S" 
        }

    ],
    ProvisionedThroughput= {
            "WriteCapacityUnits": 5,
            "ReadCapacityUnits": 10
        }
)
print(db3.meta.client.list_tables())


