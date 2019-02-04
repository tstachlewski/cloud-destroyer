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
        ecs = boto3.client('ecs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)

        clusters = ecs.list_clusters()['clusterArns']
        
        for cluster in clusters:
            tasks = ecs.list_tasks( cluster=cluster)['taskArns']
            for task in tasks:
                print ('Deleting ECS task')
                ecs.stop_task( cluster=cluster, task=task)
        
            print ('Deleting ECS cluster (' + cluster + ')')
            ecs.delete_cluster( cluster=cluster )
        
        taskdefs = ecs.list_task_definitions()['taskDefinitionArns']
        for taskdef in taskdefs:
            print ('Deleting task definition (' + taskdef + ')')
            ecs.deregister_task_definition( taskDefinition=taskdef)
            

    return event
