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
        try:
            
            cloud9 = boto3.client('cloud9', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)
    
            envs = cloud9.list_environments()['environmentIds']
            for env in envs:
                print ('Deleting Cloud9')
                cloud9.delete_environment(environmentId=env)
            
        except:
            print("Wrong Region");
            
    return event
