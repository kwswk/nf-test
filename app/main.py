import argparse
import logging

from scraper.michaelkors import MKBag
from scraper.common import (
    get_json,
    upload_to_s3,
)

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--get_all_details', type=int, default=0)
    parser.add_argument('--s3_bucket', type=str)
    parser.add_argument('--s3_prefix', type=str)
    parser.add_argument('--aws_profile', type=str, default=None)
    args = parser.parse_args()

    logging.info('Starts scraping')
    mk_obj = MKBag()
    bags_data = mk_obj.get_all_bags(get_all_details=bool(args.get_all_details))
    mk_obj.cleanup()

    logging.info('Uploading Data to S3')
    get_json(bags_data)
    upload_to_s3(
        s3_bucket=args.s3_bucket,
        s3_prefix=args.s3_prefix,
        aws_profile=args.aws_profile,
    )
