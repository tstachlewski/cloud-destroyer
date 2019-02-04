import json
import boto3
import common

def lambda_handler(event, context):
    
    aws_access_key_id = common.get_access_key(event);
    aws_secret_access_key = common.get_secret_access_key(event);
    aws_session_token = common.get_session_token(event);
    
    iam = boto3.client('iam',aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, aws_session_token = aws_session_token) 
                
    users = iam.list_users()["Users"]
    for user in users:
        groups = iam.list_groups_for_user( UserName=user["UserName"] )["Groups"]
        for group in groups:
            iam.remove_user_from_group( GroupName=group["GroupName"], UserName=user["UserName"] )
            
            keys = iam.list_access_keys(UserName = user["UserName"])['AccessKeyMetadata']
            for key in keys:
                iam.delete_access_key(UserName = user["UserName"],AccessKeyId = key['AccessKeyId'])
            
        iam.delete_login_profile(UserName = user["UserName"])
        iam.delete_user( UserName=user["UserName"] )
        print("Deleting User (" + user["UserName"] + ")")
        
    groups = iam.list_groups()["Groups"]
    for group in groups:
        policies = iam.list_attached_group_policies( GroupName=group["GroupName"] )["AttachedPolicies"]
        for policy in policies:
            response = iam.detach_group_policy( GroupName=group["GroupName"], PolicyArn=policy["PolicyArn"])
            iam.delete_group( GroupName= group["GroupName"] )
                        
    roles = iam.list_roles()["Roles"]
    for role in roles:
        role_name = role["RoleName"] 
        if not role_name.startswith("AWSServiceRoleFor"):
            if (("AdminAccessRole" != role_name) and not (role_name.startswith('AWS'))):
                policies = iam.list_attached_role_policies( RoleName=role_name )["AttachedPolicies"]
                for policy in policies:
                    policy_arn = policy["PolicyArn"]
                    iam.detach_role_policy( RoleName=role_name, PolicyArn= policy_arn )
                    
                profiles = iam.list_instance_profiles_for_role( RoleName= role_name )["InstanceProfiles"]
                for profile in profiles:
                    response = iam.remove_role_from_instance_profile( InstanceProfileName=profile['InstanceProfileName'], RoleName= role_name )
                    iam.delete_instance_profile( InstanceProfileName=profile['InstanceProfileName'] )

                policies = iam.list_role_policies( RoleName=role_name )["PolicyNames"]
                for policy in policies:
                    iam.delete_role_policy( RoleName=role_name, PolicyName=policy )
                
                iam.delete_role( RoleName=role_name )
            

    return event
