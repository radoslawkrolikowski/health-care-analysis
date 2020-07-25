import re
import scrapy
from scrapy.http import FormRequest

params_dict = {
    'medical oncology': {'especialidad': '14', 'parametros_query': 'czoxMjA6IiBjYXRlZ29yaWFfbm9tYnJlX3VzdWFyaW8gPSAxICBBTkQgKCAgIGVzcGVjaWFsaWRhZCA9JzE0JyApICDCmCoqwphmYWxzZcKYKirCmDEywpgqKsKYMTLCmCoqwphidXNxdWVkYV9tZWRpY2ExNMKYKirCmDEwMSI7'},
    'pediatric oncology': {'especialidad': '15', 'parametros_query': 'czoxMTk6IiBjYXRlZ29yaWFfbm9tYnJlX3VzdWFyaW8gPSAxICBBTkQgKCAgIGVzcGVjaWFsaWRhZCA9JzE1JyApICDCmCoqwphmYWxzZcKYKirCmDEywpgqKsKYMTLCmCoqwphidXNxdWVkYV9tZWRpY2ExNcKYKirCmDI2Ijs='},
    'oncologic surgery': {'especialidad': '3', 'parametros_query': 'czoxMTg6IiBjYXRlZ29yaWFfbm9tYnJlX3VzdWFyaW8gPSAxICBBTkQgKCAgIGVzcGVjaWFsaWRhZCA9JzMnICkgIMKYKirCmGZhbHNlwpgqKsKYMTLCmCoqwpgxMsKYKirCmGJ1c3F1ZWRhX21lZGljYTPCmCoqwpgzMDAiOw=='},
    'general surgery':  {'especialidad': '2', 'parametros_query': 'czoxMTc6IiBjYXRlZ29yaWFfbm9tYnJlX3VzdWFyaW8gPSAxICBBTkQgKCAgIGVzcGVjaWFsaWRhZCA9JzInICkgIMKYKirCmGZhbHNlwpgqKsKYMTLCmCoqwpgxMsKYKirCmGJ1c3F1ZWRhX21lZGljYTLCmCoqwpgyNyI7'},
    'gastroenterology': {'especialidad': '10', 'parametros_query': 'czoxMTg6IiBjYXRlZ29yaWFfbm9tYnJlX3VzdWFyaW8gPSAxICBBTkQgKCAgIGVzcGVjaWFsaWRhZCA9JzEwJyApICDCmCoqwphmYWxzZcKYKirCmDEywpgqKsKYMTLCmCoqwphidXNxdWVkYV9tZWRpY2ExMMKYKirCmDYiOw=='},
    'urology': {'especialidad': '26', 'parametros_query': 'czoxMTg6IiBjYXRlZ29yaWFfbm9tYnJlX3VzdWFyaW8gPSAxICBBTkQgKCAgIGVzcGVjaWFsaWRhZCA9JzI2JyApICDCmCoqwphmYWxzZcKYKirCmDEywpgqKsKYMTLCmCoqwphidXNxdWVkYV9tZWRpY2EyNsKYKirCmDQiOw'},
    'oncological radiotherapy': {'especialidad': '24', 'parametros_query': 'czoxMTk6IiBjYXRlZ29yaWFfbm9tYnJlX3VzdWFyaW8gPSAxICBBTkQgKCAgIGVzcGVjaWFsaWRhZCA9JzI0JyApICDCmCoqwphmYWxzZcKYKirCmDEywpgqKsKYMTLCmCoqwphidXNxdWVkYV9tZWRpY2EyNMKYKirCmDUyIjs'}
}


class VenHealthSpecialists(scrapy.Spider):
    """Implementation of the Scrapy Spider that extracts the health specialists data from
    http://oncologia.org.ve/site/estructuras/

    Parameters
    ----------
    spec: str
        Health specialization.
    phpsessid: str
        Browser's cookie (PHPSESSID) containing the search information.


    Yields
    ------
    dict
        Dictionary that represents scraped item.

    """

    name = "ven_health_spec_spider"
    allowed_domains = ["oncologia.org.ve"]
    start_urls = ["http://oncologia.org.ve/site/estructuras/"]
    search_url = "http://oncologia.org.ve/site/estructuras/busqueda_medica.php"
    db_query_url = "http://www.oncologia.org.ve/site/controladores/controladores_ajax/ajax_controller_busqueda_medica.php"
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'COOKIES_DEBUG': True
    }

    def __init__(self, spec, phpsessid):

        super(VenHealthSpecialists, self).__init__()

        self.spec = spec
        self.phpsessid = phpsessid

    def start_requests(self):

        yield scrapy.Request(
            self.start_urls[0],
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
                'Content-Type': 'text/html; charset=UTF-8'
            },
            callback=self.search_request)

    def search_request(self, response):

        yield FormRequest(
            self.search_url,
            method="POST",
            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'deflate',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'DNT': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
                'Referer': 'http://oncologia.org.ve/site/estructuras/',
                'Upgrade-Insecure-Requests': '1'
            },
            formdata={
                'nombre': 'Nombre+o+Apellido',
                'especialidad': params_dict[self.spec]['especialidad'],
                'ciudad': 'Ciudad'
            },
            cookies={'PHPSESSID': self.phpsessid},
            callback=self.db_query)

    def db_query(self, response):

        yield FormRequest(
            self.db_query_url,
            method='POST',
            headers={
                'Accept': 'text/html, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'deflate',
                'Cache-Control': 'max-age=0, no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
                'Referer': 'http://www.oncologia.org.ve/site/estructuras/busqueda_medica.php',
                'Host': 'www.oncologia.org.ve',
                'Pragma': 'no-cache'
            },
            formdata={
                'v_post': 'POST',
                'v_div_pager': 'vista_mod_lis_ajax',
                'v_url_pager': '../controladores/controladores_ajax/ajax_controller_busqueda_medica.php',
                'parametros_query': params_dict[self.spec]['parametros_query'],
                'v_pagina_cargar': '1'
            },
            cookies={'PHPSESSID': self.phpsessid},
            callback=self.parse_pages
        )


    def parse_pages(self, response):

        response = response.replace(encoding='latin1')

        if "Could not successfully run query" in response.text:
            raise ValueError('Make sure that passed PHPSESSID corresponds to current search parameters.')
            raise scrapy.exceptions.CloseSpider

        items = response.xpath("//div[@id='contein']/div[@class='iten_reorder']")
        for item in items:
            item_data= item.xpath(".//div/text()").extract()
            item_data = [data.strip(": ") for data in item_data if not data.startswith("\n")]

            try:
                name = item_data[0]
                # specialization = item_data[1]
                address = item_data[2]

                if address == 'N/A':
                    continue

                yield {
                    'name': name.strip("\t"),
                    'specialization': self.spec,
                    'address': address
                }

            except IndexError:
                continue

        num_pages = response.xpath("//div[@id='paginador_inf']/table/tr/td/div/a[@title='Ultima pagina']/@onclick").extract_first()

        if num_pages:
            num_pages = int(re.findall(r"\d{1,2}'\)", num_pages)[0].strip("')"))

            if num_pages > 1:
                for page in range(2, num_pages + 1):
                    yield FormRequest(
                        self.db_query_url,
                        method='POST',
                        headers={
                            'Accept': 'text/html, */*',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'deflate',
                            'Cache-Control': 'max-age=0, no-cache',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-Requested-With': 'XMLHttpRequest',
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
                            'Referer': 'http://www.oncologia.org.ve/site/estructuras/busqueda_medica.php',
                            'Host': 'www.oncologia.org.ve',
                            'Pragma': 'no-cache'
                        },
                        formdata={
                            'v_post': 'POST',
                            'v_div_pager': 'vista_mod_lis_ajax',
                            'v_url_pager': '../controladores/controladores_ajax/ajax_controller_busqueda_medica.php',
                            'parametros_query': params_dict[self.spec]['parametros_query'],
                            'v_pagina_cargar': str(page)
                        },
                        cookies={'PHPSESSID': self.phpsessid},
                        callback=self.parse_items
                    )

    def parse_items(self, response):

        response = response.replace(encoding='latin1')

        items = response.xpath("//div[@id='contein']/div[@class='iten_reorder']")
        for item in items:
            item_data= item.xpath(".//div/text()").extract()
            item_data = [data.strip(": ") for data in item_data if not data.startswith("\n")]
            try:
                name = item_data[0]
                # specialization = item_data[1]
                address = item_data[2]

                if address == 'N/A':
                    continue

                yield {
                    'name': name.strip("\t"),
                    'specialization': self.spec,
                    'address': address
                }

            except IndexError:
                continue
