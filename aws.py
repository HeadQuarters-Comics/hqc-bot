from settings import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID

import boto3

def list_folders(prefix):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    paginator = s3.get_paginator('list_objects_v2')

    my_bucket = paginator.paginate(Bucket='hqc-hq', Prefix=prefix, Delimiter="/")

    folders = []
    for page in my_bucket:
        folders.extend([x['Prefix'] for x in page.get('CommonPrefixes', [])])

    print(folders)

def list_hqs(prefix):
    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    my_bucket = s3.Bucket('hqc-hq')

    for object_summary in my_bucket.objects.filter(Prefix=prefix, Delimiter=""):
        print(object_summary.key)



list_folders('')
list_hqs('dc/batman_que_ri/')
