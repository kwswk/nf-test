import re
import logging

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup, ResultSet
from functools import partial
from datetime import datetime

logging.basicConfig(level=logging.INFO)


class MKBag(object):

    def __init__(self):
        driver_options = Options()
        driver_options.add_argument("--headless")
        driver_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        self.driver = webdriver.Firefox(options=driver_options)

    def browse_web(
        self,
        url: str = 'https://www.michaelkors.global/hk/en/women/handbags/?pmin=1.00&start=0&sz={max_item}',
        item_count: int = 50,
    ) -> ResultSet:
        self.driver.get(url.format(max_item=item_count))
        return BeautifulSoup(self.driver.page_source, 'html.parser')
    
    def cleanup(self):
        self.driver.quit()

    @staticmethod
    def extract_item_info(raw_result: ResultSet, path: str, get_item: str) -> list:
        found = raw_result.select(path)
        if not found:
            return []
        if get_item == 'text':
            return [txt.text for txt in found]
        else:
            return [item.get(get_item) for item in found]

    def item_data_constructor(self, raw_result: ResultSet, get_all_details: bool) -> dict:

        extract_info_partial = partial(self.extract_item_info, raw_result=raw_result)
        product_link=f"https://www.michaelkors.global/{extract_info_partial(path='div.pdp-link a', get_item='href')[0]}"

        brand = extract_info_partial(path='div.product-brand a', get_item='text')
        item_name=extract_info_partial(path='div.pdp-link a', get_item='text')[0]

        logging.info(f'Pulling Basic information of item: {item_name}')

        basic_details = dict(
            brand=brand[0] if brand else 'MICHAEL Michael Kors',
            item_name=item_name,
            product_link=product_link,
            default_price=max(extract_info_partial(path='span.default-price .value', get_item='content')),
            current_price=min(extract_info_partial(path='span.default-price .value', get_item='content')),
            colors=extract_info_partial(path='div.swatches img', get_item='title'),
            product_images=extract_info_partial(path='div.image-container img', get_item='src'),
            timestamp=datetime.now(),
        )

        if get_all_details:
            logging.info(f'Pulling dtailed information of item: {item_name}')
            extra_details = self.get_item_details(product_link)
            basic_details.update(extra_details)
        
        return basic_details

    def get_all_bags(self, get_all_details: bool = False) -> list:

        total_bags = self.browse_web().select_one('span.results-count-value').text

        logging.info(f'Start pulling total {total_bags} bags data')
 
        lst_bags = self.browse_web(item_count=total_bags).findAll('div', class_='product-tile')

        bags_data = []

        for idx, bags in enumerate(lst_bags):
            logging.info(f'Working on {idx+1}/{total_bags} bags')
            bags_data.append(self.item_data_constructor(bags, get_all_details))

        return bags_data
    
    def get_item_details(self, product_link: str) -> dict:
        raw_product_detail = self.browse_web(product_link)

        extra_data = dict(
            desceiption=raw_product_detail.select('div.col-12.value.content')[0].text.strip(),
            availability=raw_product_detail.select('div.availability')[0].get('data-available'),
            product_details=raw_product_detail.select('div.col-sm-12.col-md-8.col-lg-12.value.content')[0].text.strip().split('\n')
        )
        dim_expression = r'(\d+(?:\.\d+)?)\S\s?([WHD])'
        dimension = [
            re.findall(dim_expression, details) 
            for details in extra_data['product_details'] 
            if re.findall(dim_expression, details)
        ]

        extra_data['dimension'] = {item[1]: item[0] for item in dimension[0]} if dimension else {}

        return extra_data
