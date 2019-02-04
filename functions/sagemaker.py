import json
import boto3
import common

def lambda_handler(event, context):
    
    aws_access_key_id = common.get_access_key(event);
    aws_secret_access_key = common.get_secret_access_key(event);
    aws_session_token = common.get_session_token(event);
    
    regions = common.get_regions(event);
    
    for region in regions:
        regionName = region['RegionName']
        
        
        try:
            sagemaker = boto3.client('sagemaker', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)
    
            endpoints = sagemaker.list_endpoints()
            for endpoint in endpoints['Endpoints']:
                endpointName = endpoint['EndpointName']
                sagemaker.delete_endpoint( EndpointName=endpointName )
            
            instances = sagemaker.list_notebook_instances()
            for instance in instances['NotebookInstances']:
                instanceName = instance['NotebookInstanceName']
                sagemaker.delete_notebook_instance( NotebookInstanceName=instanceName )
            
        except Exception as e:
            print(e);
            
    return event
