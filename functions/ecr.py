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
        ecr = boto3.client('ecr', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)

        describe_repo_paginator = ecr.get_paginator('describe_repositories')
        for response_listrepopaginator in describe_repo_paginator.paginate():
            for repo in response_listrepopaginator['repositories']:
         
                repoName = repo['repositoryName']
                registryId= repo['registryId']
                images = ecr.list_images(repositoryName=repoName)['imageIds']
                for image in images:
                    ecr.batch_delete_image(repositoryName=repoName, imageIds=[ { 'imageDigest': image['imageDigest'] }] )
                
                print ('Deleting ECR Repo (' + repoName + ')')
                ecr.delete_repository(repositoryName=repoName)
            

    return event
