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
        lambdaClient = boto3.client('lambda', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)
        
        lambdasFunction = lambdaClient.list_functions()
        for lambdasFunction in lambdasFunction['Functions']:
            functionName = lambdasFunction['FunctionName']
            lambdaClient.delete_function(FunctionName=functionName)
            print ('Deleting Lambda (' + functionName + ')') 
    
    return event;
