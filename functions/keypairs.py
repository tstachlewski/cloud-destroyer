import json
import boto3

def lambda_handler(event, context):
    
    aws_access_key_id = event["AccessKeyId"]
    aws_secret_access_key = event["SecretAccessKey"]
    aws_session_token = event["SessionToken"]
    
    ec2 = boto3.client('ec2', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, aws_session_token = aws_session_token)
    regions = ec2.describe_regions()['Regions']
    
    for region in regions:
        regionName = region['RegionName']
        ec2Client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)

        keyPairs = ec2Client.describe_key_pairs()
        for keyPair in keyPairs["KeyPairs"]:
        	keyPair = keyPair["KeyName"]
        	ec2Client.delete_key_pair(KeyName=keyPair,DryRun=False)
        	print ("Deleting KeyPair (" + keyPair + ")")
            

    return event
