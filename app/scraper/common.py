import boto3
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)


def get_df(data: dict) -> pd.DataFrame:
    return pd.DataFrame(data)


def get_json(data, file_name: str = 'bags-data.json'):
    logging.info(f'Converting into Json @ {file_name}')
    df = get_df(data)
    return df.to_json(file_name, orient='records')


def upload_to_s3(
    s3_bucket: str, 
    s3_prefix: str,
    file_path: str = 'bags-data.json',
    aws_profile: str = None
):
    if aws_profile:
        boto_session = boto3.Session(profile_name=aws_profile)
        s3 = boto_session.client('s3')
    else:
        s3 = boto3.client('s3')

    logging.info(f'Uploading {file_path} to s3://{s3_bucket}/{s3_prefix}')

    s3.upload_file(
        file_path, 
        s3_bucket, 
        s3_prefix,
    )

    logging.info('Uploaded')
