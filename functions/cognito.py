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
            client = boto3.client('cognito-identity', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)
            
            response = client.list_identity_pools(MaxResults=50)
            for pool in response["IdentityPools"]:
                poolId = pool["IdentityPoolId"]
                client.delete_identity_pool( IdentityPoolId=poolId )
                print ('Deleting cognito pool (' + poolId + ')')
        except:
            print("Wrong Region");
            

    return event
