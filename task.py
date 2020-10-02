import boto3
s3 = boto3.resource('s3', 
    aws_access_key_id='AKIA6Q6ENXXUXYKSL5UX',
    aws_secret_access_key='no secret key here'
)
try:
    s3.create_bucket(Bucket='testuser00', CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
except:
    print("this may already exist")

bucket = s3.Bucket("testuser00")
bucket.Acl().put(ACL='public-read')

body = open('hi.txt', 'rb')
o = s3.Object('testuser00', 'test').put(Body=body)
s3.Object('testuser00', 'test').Acl().put(ACL='public-read')

dyndb = boto3.resource('dynamodb',
    region_name='us-west-2',
    aws_access_key_id='AKIA6Q6ENXXUXYKSL5UX',
    aws_secret_access_key='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'
)

try:
    table = dyndb.create_table(
        TableName='DataTable',
        KeySchema=[
            {
                'AttributeName': 'PartitionKey',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'RowKey',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PartitionKey',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'RowKey',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
except:
    #if there is an exception the table may already exist. If so....
    table = dyndb.Table("DataTable")
    #wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName='DataTable')
    print(table.item_count)

import csv 
with open('experiments.csv') as csvfile:
    csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
    for item in csvf:
        print(item)
        body = open(item[3]+'.txt','rb')
        s3.Object('testuser00',item[3]).put(Body=body)
        md = s3.Object('testuser00', item[3]).Acl().put(ACL='public-read')
        
        url = "https://s3-us-west-2.amazonaws.com/testuser00/"+item[3]
        metadata_item = {'PartitionKey': item[0], 'RowKey': item[1],
            'description': item[4], 'date': item[2], 'url': url}
            
        try:
            table.put_item(Item=metadata_item)
        except:
            print("item may already be there or another failure")
            
response = table.get_item(
    Key={
        'PartitionKey' : 'experiment3',
        'RowKey' : '4'
        }
    )
item = response['Item']
print(item)
response
