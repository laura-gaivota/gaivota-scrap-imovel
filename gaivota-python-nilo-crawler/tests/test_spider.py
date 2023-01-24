from gaivota_python_nilo_crawler.spiders import NiloSpider
from unittest import TestCase

class NiloSpiderTests(TestCase):

    def test_parse_got_resource_and_yield_item_successfully(self):
        # TODO: Implement the logic of a successfull scraping, returning a valid item.
        pass

    def test_parse_got_resource_but_there_is_no_data_to_yield__stops_crawler_and_send_notification(self):
        # TODO: Implement the logic of a successfull scraping without item to be returned,
        #       status data being added to database and notification being sent.
        pass

    def test_parse_got_bad_answer_from_source__stops_crawler_and_send_notification(self):
        # TODO: Implement the logic of a bad answer when scraping without,
        #       status data being added to database and notification being sent.
        pass
