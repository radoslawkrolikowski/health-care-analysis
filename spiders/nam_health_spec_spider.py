import scrapy


class NamHealthSpecialists(scrapy.Spider):
    """Implementation of the Scrapy Spider that extracts the health specialists data from
    methealth.com.na

    Parameters
    ----------
    spec_list: str
        String object with specializations separated by commas.

    Yields
    ------
    dict
        Dictionary that represents scraped item.

    """

    name = "nam_health_spec_spider"
    allowed_domains = ["methealth.com.na"]
    start_urls = ["http://www.methealth.com.na/doctor_types.php"]

    def __init__(self, spec_list):

        super(NamHealthSpecialists, self).__init__()

        self.spec_list = spec_list.split(',')

    def parse(self, response):

        spec_names = response.xpath("//strong/h19/a/text()").extract()
        spec_links = response.xpath("//strong/h19/a/@href").extract()

        spec_names = [name[:name.find("(")].strip() for name in spec_names]

        for name, link in zip(spec_names, spec_links):
            for spec in self.spec_list:
                if name == spec:
                    url = response.urljoin(link)

                    yield scrapy.Request(url, callback=self.parse_page, meta=dict(spec=spec))

    def parse_page(self, response):

        spec = response.meta.get('spec')
        rows = response.xpath("//table/tbody/tr")

        for row in rows:
            data = row.xpath(".//td/text()").extract()
            city = row.xpath(".//td/hmred/text()").extract_first()

            name = data[0]
            address = data[1].strip(", ") + ', ' + city

            yield {
                'name': name.capitalize(),
                'specialization': spec,
                'address': address
            }



