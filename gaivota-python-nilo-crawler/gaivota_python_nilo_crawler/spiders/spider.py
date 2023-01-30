from scrapy import Request
import re

from gaivota_python_nilo_crawler.items import NiloItem

from gaivota_crawler_driver.crawler.spider import GaivotaSpider


class NiloSpider(GaivotaSpider):

    url ="https://rural.niloimoveis.com.br/"
    name = "nilo_crawler"
    r = []
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

    def get_imovel_data_md_4(self,text,response):
        return [re.search('<p>(.*)</p>', x).group(1) for x in response.css('div.col-md-4').extract() if text in x][0]

    def get_estructura_e_caracteristicas(self):
        pass
    def parse_imovel_detail(self, response):
        print('detail-imovel-------', response.meta.get('imovel')['url'])
        aux = response.meta.get('imovel')
        # description = response.css('div.mt-50 p::text').extract()
        cidade = self.get_imovel_data_md_4('Cidade',response)
        estado = self.get_imovel_data_md_4('Estado',response)
        area_total  = self.get_imovel_data_md_4('Área Total',response)
        finalidade = self.get_imovel_data_md_4('Finalidade',response)
        aux['estado'] = estado
        aux['cidade'] = cidade
        aux['area_total'] = area_total
        aux['finalidade'] = finalidade
        estr = response.css('table.table tr')
        feat_contain = []
        not_contain = []
        for c in estr:
            trs = c.css('td ::text').extract()
            check = c.css('td i.fa').xpath("@class").extract()
            
            if (trs[0].strip() != '') and (trs[0].strip() != ','):
                if check[0].strip() != '' :
                    if 'fa-check' in check[0]:

                        feat_contain.append(trs[0].strip())
                    else:
                        not_contain.append(trs[0].strip())
        aux['features_contain'] = feat_contain
        aux['features_not_contain'] = not_contain
        
        return self.build_items(to_build=aux, s3_path='s3_path')
        


    def parse(self, response):        
        # s3_path = f"nilo/source_file/{self._start_time}/{file_name_with_type}"  # TODO: if necessary, complete the path
        if self.check_response_status(response):           

            try:
                contents = response.css('div.div-content')
                res = []
                
                for content in contents:
                    
                    aux = {}                 
                    code = content.css('span.código-imovel::text').get()
                    aux['code'] = code
                    title = content.css('h2 *::text').get()
                    aux['title'] = title
                    price = self.parse_price(content.css('p.valor-imovel::text').get())
                    aux['price'] = price
                    url = self.url[:-1]+content.css('div.area-texto a::attr(href)').extract()[0]
                    aux['url'] = url
                    
                    yield Request(url, callback=self.parse_imovel_detail, meta = {'imovel':aux})
                    

                    
                
                first_next_page = response.css('a.link02::attr(href)')
                
                if len(first_next_page.extract()) > 0:
                    
                    first_next_page_url = self.url[:-1] + first_next_page.extract()[0]
                    yield response.follow(first_next_page_url, callback=self.parse)

                next_page = response.css('[rel="next"] ::attr(href)').get()

                if next_page is not None:
                    yield response.follow(next_page, callback=self.parse)



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
        
        
        try:
            data = NiloItem(code=to_build['code'],title= to_build['title'],price = to_build['price'],
                            finalidade = to_build['finalidade'], area_total = to_build['area_total'],
                            cidade = to_build['cidade'], estado = to_build['estado'],
                            features_contain = to_build['features_contain'],
                            s3_path=s3_path, url = to_build['url'])
            self.num_processed += 1
            
            yield data
        except Exception as err:
            print('ERROR',err)
            self.logger.exception("Error in build_item", exc_info=err)
            self.dbutil.report_crawler_status(5, self, observations="Error in build_item",
                                                s3_path=s3_path)

    def close(self):
        super().close()
        # TODO: Finish any need resources acquired during crawling.
