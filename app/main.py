import argparse
import logging

from scraper.michaelkors import MKBag

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--get_all_details', action='store_true', default=False)
    parser.add_argument('--to_s3', action='store_true', default=False)
    args = parser.parse_args()

    logging.info('Starts scraping')
    mk_obj = MKBag()
    bags_data = mk_obj.get_all_bags(get_all_details=args.get_all_details)
    mk_obj.cleanup()

    if args.to_s3:
        logging.info('Uploading Data to S3')
