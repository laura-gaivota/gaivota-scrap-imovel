from scrapy import Request


from gaivota_python_nilo_crawler.items import NiloItem

from gaivota_crawler_driver.crawler.spider import GaivotaSpider


class NiloSpider(GaivotaSpider):

    url ="https://rural.niloimoveis.com.br/"
    name = "nilo_crawler"

    def __init__(self):

        __DATABASE_SCHEMA = "registry_layers"

        __TABLE_NAME = "nilo_imovel"
        super().__init__(__DATABASE_SCHEMA, __TABLE_NAME)
    def start_requests(self):
        yield Request(self.url,
                      callback=self.parse,
                      errback=self.errback_httpbin
                      )
    
    def check_response_status(self,response):
        if response.status == 200:
            return True
        else: 
            return False
        

    def parse_code(self,text):
        pass

    def parse_price(self,text):
        
        r = text.strip()
        
        if 'CONSULTE VALOR' in r:
           
            return 
        else:
            return r
    def parse_imovel_detail(self):
        pass
    def parse(self, response):
        
        
        # s3_path = f"nilo/source_file/{self._start_time}/{file_name_with_type}"  # TODO: if necessary, complete the path
        if self.check_response_status(response):           

            try:
                contents = response.css('div.div-content')
                res = []
                
                for content in contents:
                    print('-----')
                    aux = {}                 
                    code = content.css('span.código-imovel::text').get()
                    title = content.css('h2 *::text').get()
                    # finalidade = content.css('p.caracteristica-imovel i').get()
                    price = self.parse_price(content.css('p.valor-imovel::text').get())
                    url = self.url[:-1]+content.css('div.area-texto a::attr(href)').extract()[0]
                    yield Request(url, callback=self.parse_imovel_detail, meta = {'imovel':aux})


                    
                
                # first_next_page = response.css('a.link02::attr(href)')
                
                # if len(first_next_page.extract()) > 0:
                    
                #     first_next_page_url = self.url[:-1] + first_next_page.extract()[0]
                #     print('--- first next page ---')
                #     yield response.follow(first_next_page_url, callback=self.parse)

                # next_page = response.css('[rel="next"] ::attr(href)').get()

                # if next_page is not None:
                #     print('--- next ---')
                #     yield response.follow(next_page, callback=self.parse)



                # # Get data.
                # local_file_path = self.save_response_in_file(response=response, file_name_with_type=file_name_with_type)
                # self.upload_to_s3(local_file_path, s3_path)

                # # if the result it's a JSON:
                # #result = response.json()
                # # Another way to get response
                # #result = json.loads(response.body)
                # result = None
                # # else use another processing below
                # return self.build_items(to_build=result, s3_path=s3_path)

            except Exception as err:
                msg = f"Error while parsing items. Error: {err}"
                print(msg)
                # self.dbutil.report_crawler_status(5, self, observations=msg,
                #                                   s3_path=s3_path)
                # self.logger.exception(f"Error while parsing items", exc_info=err)

    def build_items(self, to_build, s3_path):

        # TODO: Implement build of items - example is using variable to_build. adapt if necessary
        # TODO: If necessary, change this loop to iterate correctly through items
        for item in to_build:
            try:
                data = NiloItem(id_example=to_build['id_example'],
                                content_example=to_build['content_example'],
                                s3_path=s3_path)
                self.num_processed += 1
                yield data
            except Exception as err:
                self.logger.exception("Error in build_item", exc_info=err)
                self.dbutil.report_crawler_status(5, self, observations="Error in build_item",
                                                  s3_path=s3_path)

    def close(self):
        super().close()
        # TODO: Finish any need resources acquired during crawling.
