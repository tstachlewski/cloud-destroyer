import json
import boto3
import uuid
import time
import common
from botocore.exceptions import EndpointConnectionError

def lambda_handler(event, context):
    
    aws_access_key_id = common.get_access_key(event);
    aws_secret_access_key = common.get_secret_access_key(event);
    aws_session_token = common.get_session_token(event);
    
    regions = common.get_regions(event);
    
    for region in regions:
        
        try: 
            regionName = region['RegionName']
            client = boto3.client('athena', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)
    
            s3_bucket =  str(uuid.uuid4());

            response = client.start_query_execution( QueryString='show databases;', ResultConfiguration={ 'OutputLocation': 's3://' + s3_bucket, 'EncryptionConfiguration': { 'EncryptionOption': 'SSE_S3', 'KmsKey': 'string' } } )
        
            databases_names_file = response['QueryExecutionId'] + ".txt";
            
            time.sleep(2)
            
            s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=regionName, aws_session_token = aws_session_token)
            s3.meta.client.download_file(s3_bucket, databases_names_file, "/tmp/"+databases_names_file);
        
            # Reading a file
            with open("/tmp/"+databases_names_file, 'r') as myfile:
                databases_string=myfile.read();
                
                databases = databases_string.splitlines();
                for database in databases:
                    response = client.start_query_execution( QueryString='show tables', QueryExecutionContext={ 'Database': database }, ResultConfiguration={ 'OutputLocation': 's3://' + s3_bucket, 'EncryptionConfiguration': { 'EncryptionOption': 'SSE_S3', 'KmsKey': 'string' } } )
                    tables_names_file = response['QueryExecutionId'] + ".txt";
                    
                    time.sleep(2)
                    s3.meta.client.download_file(s3_bucket, tables_names_file, "/tmp/"+tables_names_file);
                    
                    # Reading a file
                    with open("/tmp/"+tables_names_file, 'r') as myfile:
                        tables_file=myfile.read();
                        tables = tables_file.splitlines();
                        for table in tables:
                            client.start_query_execution( QueryString='drop table ' + table, QueryExecutionContext={ 'Database': database }, ResultConfiguration={ 'OutputLocation': 's3://' + s3_bucket, 'EncryptionConfiguration': { 'EncryptionOption': 'SSE_S3', 'KmsKey': 'string' } } )
                            print('Deleting table (' + table + ')');
                    client.start_query_execution( QueryString='drop database ' + database, ResultConfiguration={ 'OutputLocation': 's3://' + s3_bucket, 'EncryptionConfiguration': { 'EncryptionOption': 'SSE_S3', 'KmsKey': 'string' } } )
                    print('Deleting database (' + database + ')');
                    
        except EndpointConnectionError:
            print ("Endpoint Connection Error - OK");
    
            
    return event
