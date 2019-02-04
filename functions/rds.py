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
        rds = boto3.client('rds', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)
        
        clusters = rds.describe_db_clusters()['DBClusters']
    
        for cluster in clusters:
            
            clusterId = cluster['DBClusterIdentifier']
            rds.delete_db_cluster( DBClusterIdentifier=clusterId, SkipFinalSnapshot=True )
         
        subnets = rds.describe_db_subnet_groups()["DBSubnetGroups"]
        for subnet in subnets:
            subnet_group_name = subnet["DBSubnetGroupName"]
            rds.delete_db_subnet_group( DBSubnetGroupName=subnet_group_name)
        

    return event
