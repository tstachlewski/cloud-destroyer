import json
import boto3
import common

def lambda_handler(event, context):
    
    aws_access_key_id = common.get_access_key(event);
    aws_secret_access_key = common.get_secret_access_key(event);
    aws_session_token = common.get_session_token(event);
    
    
    sts = boto3.client('sts', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, aws_session_token = aws_session_token)
    accountId = sts.get_caller_identity()["Account"]
    
    regions = common.get_regions(event);
    
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
