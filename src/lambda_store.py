import json
import boto3


s3Client = boto3.client('s3')
s3Res = boto3.resource('s3')
def store(event, context):
    bucketname = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print('Reading object {} from bucket {}.'.format(key, bucketname))

    try:
        # Get the object
        response = s3Client.get_object(Bucket=bucketname, Key=key)
        data = response['Body'].read().decode('utf-8')
        obj = s3Res.Object('salardestbucket', 'Data/Raw/Input/{}'.format('pace-data.csv'))
        obj.put(Body=data)
        print('File stored successfully!!')
    
        return {
            'statusCode': 200,
            'body': json.dumps('Copy File Successfully!')
        }

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}.'.format(key, bucketname))
        raise e
