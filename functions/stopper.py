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
            sagemaker = boto3.client('sagemaker', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)
            print(regionName);

            instances = sagemaker.list_notebook_instances()
            for instance in instances['NotebookInstances']:
                instanceName = instance['NotebookInstanceName']
                sagemaker.stop_notebook_instance( NotebookInstanceName=instanceName )
                print("Stopping (SageMaker) :" + instanceName)
            
        except Exception as e:
            print(e);
            
    return event
