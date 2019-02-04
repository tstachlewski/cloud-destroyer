import json
import boto3
from botocore.exceptions import EndpointConnectionError

def lambda_handler(event, context):
    
    aws_access_key_id = event["AccessKeyId"]
    aws_secret_access_key = event["SecretAccessKey"]
    aws_session_token = event["SessionToken"]
    
    ec2 = boto3.client('ec2', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, aws_session_token = aws_session_token)
    regions = ec2.describe_regions()['Regions']
    
    try: 
        for region in regions:
            regionName = region['RegionName']
            firehose = boto3.client('firehose', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)
    
            streams = firehose.list_delivery_streams()
            for stream in streams['DeliveryStreamNames']:
                firehose.delete_delivery_stream( DeliveryStreamName=stream )
                print ('Deleting Firehose  (' + stream + ')')
    except EndpointConnectionError:
        print ("Endpoint Connection Error - OK");

    return event
