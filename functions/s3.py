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
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)
        
        for bucket in s3.list_buckets()["Buckets"]:
            bucketName = bucket["Name"]
            print ('Deleting bucket: ' + bucketName)
            
            try:
                s3.delete_bucket_policy(Bucket=bucketName)
                objects = s3.list_objects_v2(Bucket=bucketName, MaxKeys=1000)

                if "Contents" in objects:
                    for object in objects["Contents"]:
                        print ("Deleting S3 object (" + object["Key"] + ")")
                        s3.delete_objects(Bucket=bucketName, Delete={'Objects': [{'Key': object["Key"]}]})
                
                verisons = s3.list_object_versions(Bucket=bucketName)
                if 'Versions' in verisons:
                    objects = s3.list_object_versions(Bucket=bucketName)['Versions']
                    for object in objects:
                        s3.delete_objects(Bucket=bucketName, Delete={'Objects': [{'Key': object["Key"], 'VersionId':object["VersionId"] }]})
                
                if 'DeleteMarkers' in verisons:
                    objects = s3.list_object_versions(Bucket=bucketName)['DeleteMarkers']
                    for object in objects:
                        s3.delete_objects(Bucket=bucketName, Delete={'Objects': [{'Key': object["Key"], 'VersionId':object["VersionId"] }]})
                
                s3.delete_bucket(Bucket=bucketName)
                
            except Exception as e:
                print ('Error')
                print(e)
    return event;
			
