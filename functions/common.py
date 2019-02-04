import boto3

def get_access_key(event):
    if (isinstance(event, list)):
        return event[0]["AccessKeyId"]; 
    else:
        return event["AccessKeyId"];

def get_secret_access_key(event):
    if (isinstance(event, list)):
        return event[0]["SecretAccessKey"]; 
    else:
        return event["SecretAccessKey"];
    
def get_session_token(event):
    if (isinstance(event, list)):
        return event[0]["SessionToken"]; 
    else:
        return event["SessionToken"];

def get_regions(event):
    aws_access_key_id = get_access_key(event);
    aws_secret_access_key = get_secret_access_key(event);
    aws_session_token = get_session_token(event);
    
    ec2 = boto3.client('ec2', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, aws_session_token = aws_session_token)
    regions = ec2.describe_regions()['Regions']
    
    return regions;
