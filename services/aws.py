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

    return folders

def list_hqs(prefix):
    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    my_bucket = s3.Bucket('hqc-hq')
    prefix = str(prefix).lower()
    editions = []

    for object_summary in my_bucket.objects.filter(Prefix=prefix, Delimiter=""):
        edition_number = str(object_summary.key).replace(f'{prefix}', '').replace('.pdf', '').replace('/', '')
        editions.append(edition_number)
    print('-------------------')
    print(f'Buscando edições em: {prefix}')
    print(f'Quantidade de edições encontradas foi: {len(editions)}')
    if len(editions) == 0:
        return 'Infelizmente não temos nenhuma edição desse título ainda :('
    editions.pop(0)
    return editions

def get_hq(publisher, title, edition):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        s3.download_file(Bucket="hqc-hq", Key=f'{publisher}/{title}/{edition}.pdf', Filename=f'data/{title}_{edition}.pdf')
        return True
    except botocore.exceptions.ClientError as error:
        raise error



#list_folders('dc/')
#list_hqs('marvel/baby/')
#get_hq('marvel', 'abacate', '1')
