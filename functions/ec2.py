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
        ec2client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)

        reservations = ec2client.describe_instances()['Reservations']
        for reservation in reservations:
            instances = reservation['Instances']
            for instance in instances:
                instanceId = instance['InstanceId']
                state = instance['State']['Name']
                if (state == "running") or (state == "stopped"):
                    print ('Terminating instance ' + instanceId)
                    ec2client.terminate_instances(InstanceIds=[instanceId])
            

    return event
