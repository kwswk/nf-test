from scraper.michaelkors import MKBag


if __name__ == '__main__':
    mk_obj = MKBag()
    bags_data = mk_obj.get_all_bags(get_all_details=True)
    mk_obj.cleanup()
