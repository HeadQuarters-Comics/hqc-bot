from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

import boto3
import botocore

def list_folders(prefix):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    paginator = s3.get_paginator('list_objects_v2')

    my_bucket = paginator.paginate(Bucket='hqc-hq', Prefix=prefix, Delimiter="/")

    folders = []
    for page in my_bucket:
        folders.extend([x['Prefix'] for x in page.get('CommonPrefixes', [])])

    print(folders)
    return folders

def list_hqs(prefix):
    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    my_bucket = s3.Bucket('hqc-hq')

    for object_summary in my_bucket.objects.filter(Prefix=prefix, Delimiter=""):
        print(object_summary.key)

def get_hq(publisher, title, edition):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        s3.download_file(Bucket="hqc-hq", Key=f'{publisher}/{title}/{edition}.pdf', Filename=f'data/{title}_{edition}.pdf')
        return True
    except botocore.exceptions.ClientError as error:
        raise error



#list_folders('dc/')
#list_hqs('dc/batman_que_ri/')
#get_hq('marvel', 'abacate', '1')
