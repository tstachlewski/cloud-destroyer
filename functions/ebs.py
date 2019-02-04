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
        ec2client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)

        volumes = ec2client.describe_volumes()
        for volume in volumes['Volumes']:
            print ('Deleting EBS (' + volume['VolumeId'] + ')')
            ec2client.delete_volume(VolumeId=volume['VolumeId'], DryRun=False)
        
        snapshots = ec2client.describe_snapshots(OwnerIds = [accountId])
        for snapshot in snapshots['Snapshots']:
            print ('Deleting Snapshot (' + snapshot['SnapshotId'] + ')')
            ec2client.delete_snapshot(SnapshotId = snapshot['SnapshotId'], DryRun=False)
            

    return event
