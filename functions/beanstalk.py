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
        beanstalk = boto3.client('elasticbeanstalk', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)

        applications = beanstalk.describe_applications()['Applications']
        for application in applications:
            application_name = application["ApplicationName"]
            
            versions = beanstalk.describe_application_versions( ApplicationName = application_name)["ApplicationVersions"]
            for version in versions:
                print(version)
                beanstalk.delete_application_version( ApplicationName = application_name, VersionLabel=version["VersionLabel"])
                print("Kasuje");
                
            envs = beanstalk.describe_environments(ApplicationName=application_name)["Environments"]
            for env in envs:
                environment_name = env["EnvironmentName"]
                environment_id = env["EnvironmentId"]
                beanstalk.terminate_environment( EnvironmentId=environment_id, EnvironmentName=environment_name)

            beanstalk.delete_application( ApplicationName = application_name )
            

    return event
