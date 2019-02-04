import json
import boto3

def lambda_handler(event, context):
    
    aws_access_key_id = event["AccessKeyId"]
    aws_secret_access_key = event["SecretAccessKey"]
    aws_session_token = event["SessionToken"]
    
    client = boto3.client('budgets', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token = aws_session_token)
        
    accountId = boto3.client('sts', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token = aws_session_token).get_caller_identity().get('Account');
    budgets = client.describe_budgets( AccountId=accountId )
    

    if 'Budgets' in budgets:
        for budget in budgets['Budgets']:
            budgetName = budget['BudgetName']
            client.delete_budget( AccountId=accountId, BudgetName= budgetName )
        
    return event;
