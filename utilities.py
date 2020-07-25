import subprocess
import re
import urllib
import json
from shapely.geometry import Point

apiKey = "5b3ce3597851110001cf6248efeb7e35b81142ed8974c609ac1cedcf"

health_specialists_countries = {
    'Venezuela': ['medical oncology', 'pediatric oncology', 'oncologic surgery', 'general surgery', 'gastroenterology', 'urology', 'oncological radiotherapy'],
    'Namibia': ['Dentist', 'Gynecologist', 'Internists', 'Medical Technology Laboratory', 'Ophthalmologist', 'Orthopedic Surgeon', 'Surgeon', 'Pediatrician', 'Radiation Oncologist', 'Urologist']
}

def generate_population_table(rows):
    """Returns the HTML table of the following structure:
    |    Range   |   Population  |% pop. in district |
    --------------------------------------------------
    | rows[0][0] | rows[0][1][0] |   rows[0][1][1]   |
    --------------------------------------------------
    | rows[1][0] | rows[1][1][0] |   rows[1][1][1]   |
    ...
    """
    html_rows = []

    for row_title, values in rows:
        html_rows.append(
            """<tr>
        <td><strong style="font-size: 12px;">{row}</strong></td>
        <td><strong style="font-size: 11px;">{value1}</strong></td>
        <td><strong style="font-size: 11px;">{value2}</strong></td>
      </tr>
      """.format(row=row_title, value1=values[0], value2=values[1]))

    html_rows = "".join(html_rows)

    html_table = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {{ width:100%;}}
    table, th, td {{
        border: 1px solid black;
        border-collapse: collapse;
    }}
    th, td {{
        padding: 3px;
        text-align: left;
    }}
    thead {{
        background-color: #b9d5ed;
    }}

    </style>
    </head>
    <body>

    <table id="t01">
     <thead>
       <tr>
        <td><strong style="font-size: 12px;">Range</strong></td>
        <td><strong style="font-size: 12px;">Population</strong></td>
        <td><strong style="font-size: 12px;">% pop. in district</strong></td>
       </tr>
     </thead>
     {row}
    </table>
    </body>
    </html>
    """.format(row=html_rows)

    return html_table


def get_health_spec_data(country, specialist, output_file, **kwargs):
    """Gets the health specialists data for a given country and specialization.

    Parameters
    ----------
    country: str
        Name of the country.
    specialist: str
        Health specialization(s)
    output_file: str
        Output file path.
    **kwargs
        Keyword arguments ('phpsessid', 'output_file')

    Raises
    ------
    ValueError
        If passed PHPSESSID is incorect.
    AssertionError
        If required PHPSESSID argument hasn't been passed.

    """

    if country == 'Venezuela':

        assert  'phpsessid' in kwargs.keys(), "You need to specify 'phpsessid' parameter."

        process = subprocess.Popen(['scrapy', 'runspider', '-a', 'spec='+specialist, '-a', 'phpsessid='+kwargs['phpsessid'], '-o'+output_file+':csv', 'spiders/ven_health_spec_spider.py'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = process.communicate()

        if 'ERROR' in str(stderr):
            error_mssg = re.findall(r"raise ValueError\((.*?)(?=\\n)", str(stderr))
            raise ValueError(error_mssg[0].strip("\')"))

    if country in ['Namibia']:
        process = subprocess.Popen(['scrapy', 'runspider', '-a', 'spec_list='+specialist, '-o'+output_file+':csv', 'spiders/nam_health_spec_spider.py'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = process.communicate()

        if 'ERROR' in str(stderr):
            error_mssg = re.findall(r"raise ValueError\((.*?)(?=\\n)", str(stderr))
            raise ValueError(error_mssg[0].strip("\')"))


def photon_geocoder(address):
    """ Converts addresses into geographic coordinates using photon.komoot.de API.

    Parameters
    ----------
    address: str
        String object containing the address of interest.

    Returns
    -------
    geometry: shapely.geometry.Point / None
        Shapely Point object representing the address coordinates.
    addr_street: str / None
        String containing the address found by the geocoder API.

    """

    url = "http://photon.komoot.de/api/?q=" + urllib.parse.quote(address)

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0')]
    urllib.request.install_opener(opener)

    response = urllib.request.urlopen(url)
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')

    data = json.loads(data.decode(encoding))

    geometry, addr_street = None, None

    if data['features']:
        geometry =  Point(data['features'][0]['geometry']['coordinates'])
        city = data['features'][0]['properties'].get('city', '')
        country = data['features'][0]['properties'].get('country', '')
        postcode = data['features'][0]['properties'].get('postcode', '')
        name = data['features'][0]['properties'].get('name', '')
        state = data['features'][0]['properties'].get('state', '')
        addr_street = ", ".join([name, city, postcode, state, country])

        return geometry, addr_street

    else:
        return geometry, addr_street

def ORS_geocoder(address, country_code):
    """ Converts addresses into geographic coordinates using Openrouteservice Geocode API.

    Parameters
    ----------
    address: str
        String object containing the address of interest.
    country_code: str
        The ISO 3166 alpha-3 code of the given country.

    Returns
    -------
    geometry: shapely.geometry.Point / None
        Shapely Point object representing the address coordinates.
    address: str
        Returns the original address.

    """

    url = "https://api.openrouteservice.org/geocode/search?api_key=" + apiKey + "&text=" + \
          urllib.parse.quote(address) + "&boundary.country=" + country_code

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0')]
    urllib.request.install_opener(opener)

    response = urllib.request.urlopen(url)
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')

    data = json.loads(data.decode(encoding))

    geometry = None

    if data['features']:
        geometry =  Point(data['features'][0]['geometry']['coordinates'])

        return geometry, address

    else:
        return geometry, address

def amend_address(address):
    """Amends the address, so that it can be better interpreted by the geocoder.

    """
    address = address.title()
    if address.startswith("Av.") or address.startswith("Av "):
        addr_list = address.split()
        if len(addr_list) >= 3:
            address = " ".join([addr_list[0], addr_list[1], addr_list[-1]])
            return address
    if address.startswith("Urb.") or address.startswith("Urb "):
        addr_list = address.split()
        if len(addr_list) >= 3:
            address = " ".join([addr_list[0], addr_list[1], addr_list[2]])
            return address
    else:
        return address

health_specialists_instructions = {
    'Venezuela': 'Venezuela health specialist Scrapy spider instructions:<br>Pass the following arguments to the function: get_health_spec_data(country, specialist, phpsessid, output_file), '\
                 "phpsessid is the browser's cookie containing the search information. To obtain it, firstly you have to go to http://oncologia.org.ve/site/estructuras, fill in the search "\
                 "parameters (for example 'medical oncology'), click search, then turn on the inspector (right-click -> inspect element) and go to the Storage tab and copy the PHPSESSID value;"\
                 " ouptut_file is the name of the CSV output file.<br>"
                 "When executing the get_health_spec_data function, you will be asked to manually perform the search for each specialization on the source website, so that subsequently "\
                 "the Scrapy spider will be able to use your PHPSESSID to access the website and scrap the data.",
    'Namibia': 'Namibia health specialist Scrapy spider instructions:<br>Pass the following arguments to the function: get_health_spec_data(country, spec_list, output_file), '\
               'where spec_list is the list of specializations separated by commas and ouptut_file is the name of the CSV output file.<br>'

}

# The ISO 3166 alpha-3 codes
country_codes = {
    "Afghanistan": "AFG",
    "Albania": "ALB",
    "Algeria": "DZA",
    "Andorra": "AND",
    "Angola": "AGO",
    "Anguilla": "AIA",
    "Antigua and Barbuda": "ATG",
    "Argentina": "ARG",
    "Armenia": "ARM",
    "Australia": "AUS",
    "Austria": "AUT",
    "Azerbaijan": "AZE",
    "Bahrain": "BHR",
    "Bangladesh": "BGD",
    "Barbados": "BRB",
    "Belarus": "BLR",
    "Belgium": "BEL",
    "Belize": "BLZ",
    "Benin": "BEN",
    "Bermuda": "BMU",
    "Bhutan": "BTN",
    "Bolivia": "BOL",
    "Bosnia and Herzegovina": "BIH",
    "Botswana": "BWA",
    "Brazil": "BRA",
    "Brunei": "BRN",
    "Bulgaria": "BGR",
    "Burkina Faso": "BFA",
    "Burundi": "BDI",
    "Cambodia": "KHM",
    "Cameroon": "CMR",
    "Canada": "CAN",
    "Cayman Islands": "CYM",
    "Central African Republic": "CAF",
    "Chile": "CHL",
    "China": "CHN",
    "Colombia": "COL",
    "Comoros": "COM",
    "Cook Islands": "COK",
    "Costa Rica": "CRI",
    "Croatia": "HRV",
    "Cuba": "CUB",
    "Cyprus": "CYP",
    "Czechia": "CZE",
    "Denmark": "DNK",
    "Djibouti": "DJI",
    "Dominica": "DMA",
    "Dominican Republic": "DOM",
    "Ecuador": "ECU",
    "Egypt": "EGY",
    "El Salvador": "SLV",
    "Equatorial Guinea": "GNQ",
    "Eritrea": "ERI",
    "Estonia": "EST",
    "Ethiopia": "ETH",
    "Falkland Islands": "FLK",
    "Faroe Islands": "FRO",
    "Fiji": "FJI",
    "Finland": "FIN",
    "France": "FRA",
    "Gabon": "GAB",
    "Georgia": "GEO",
    "Germany": "DEU",
    "Ghana": "GHA",
    "Greece": "GRC",
    "Greenland": "GRL",
    "Grenada": "GRD",
    "Guatemala": "GTM",
    "Guinea": "GIN",
    "Guyana": "GUY",
    "Haiti": "HTI",
    "Hungary": "HUN",
    "Iceland": "ISL",
    "India": "IND",
    "Indonesia": "IDN",
    "Iran": "IRN",
    "Iraq": "IRQ",
    "Ireland": "IRL",
    "Isle of Man": "IMN",
    "Israel": "ISR",
    "Italy": "ITA",
    "Jamaica": "JAM",
    "Japan": "JPN",
    "Jordan": "JOR",
    "Kazakhstan": "KAZ",
    "Kenya": "KEN",
    "North Korea": "PRK",
    "South Korea": "KOR",
    "Kuwait": "KWT",
    "Kyrgyzstan": "KGZ",
    "Latvia": "LVA",
    "Lebanon": "LBN",
    "Liberia": "LBR",
    "Libya": "LBY",
    "Lithuania": "LTU",
    "Madagascar": "MDG",
    "Malawi": "MWI",
    "Mali": "MLI",
    "Mauritania": "MRT",
    "Mexico": "MEX",
    "Moldova": "MDA",
    "Mongolia": "MNG",
    "Montenegro": "MNE",
    "Morocco": "MAR",
    "Mozambique": "MOZ",
    "Myanmar": "MMR",
    "Namibia": "NAM",
    "Nepal": "NPL",
    "Netherlands": "NLD",
    "New Zealand": "NZL",
    "Nicaragua": "NIC",
    "Niger": "NER",
    "Nigeria": "NGA",
    "North Macedonia": "MKD",
    "Norway": "NOR",
    "Oman": "OMN",
    "Pakistan": "PAK",
    "Panama": "PAN",
    "Papua New Guinea": "PNG",
    "Paraguay": "PRY",
    "Peru": "PER",
    "Philippines": "PHL",
    "Poland": "POL",
    "Portugal": "PRT",
    "Qatar": "QAT",
    "Romania": "ROU",
    "Russia": "RUS",
    "Rwanda": "RWA",
    "Saudi Arabia": "SAU",
    "Senegal": "SEN",
    "Serbia": "SRB",
    "Sierra Leone": "SLE",
    "Singapore": "SGP",
    "Slovakia": "SVK",
    "Slovenia": "SVN",
    "South Africa": "ZAF",
    "South Sudan": "SSD",
    "Sri Lanka": "LKA",
    "Sudan": "SDN",
    "Sweden": "SWE",
    "Switzerland": "CHE",
    "Syria": "SYR",
    "Taiwan": "TWN",
    "Tajikistan": "TJK",
    "Thailand": "THA",
    "Togo": "TGO",
    "Tonga": "TON",
    "Trinidad and Tobago": "TTO",
    "Tunisia": "TUN",
    "Turkey": "TUR",
    "Turkmenistan": "TKM",
    "Uganda": "UGA",
    "Ukraine": "UKR",
    "United Arab Emirates": "ARE",
    "United Kingdom": "GBR",
    "United States": "USA",
    "Uruguay": "URY",
    "Uzbekistan": "UZB",
    "Venezuela": "VEN",
    "Yemen": "YEM",
    "Zambia": "ZMB"
}

health_fac_popup_table_html = """
<!DOCTYPE html>
<html>
<head>
<style>
table {{
    width:100%;
}}
table, th, td {{
    border: 1px solid black;
    border-collapse: collapse;
}}
th, td {{
    padding: 3px;
    text-align: left;
}}
table#t01 tr:nth-child(odd) {{
    background-color: #f5dfe0;
}}
table#t01 tr:nth-child(even) {{
   background-color:#fff;
}}
</style>
</head>
<body>

<table id="t01">
  <tr>
    <td><strong style="font-size: 12px;">Name</strong></td>
    <td><strong style="font-size: 11px;">{}</strong></td>
  </tr>
  <tr>
    <td><strong style="font-size: 12px;">Amenity</strong></td>
    <td><strong style="font-size: 11px;">{}</strong></td>
  </tr>
  <tr>
    <td><strong style="font-size: 12px;">Address</strong></td>
    <td><strong style="font-size: 11px;">{}</strong></td>
  </tr>
</table>
</body>
</html>
""".format

health_spec_popup_table_html = """
<!DOCTYPE html>
<html>
<head>
<style>
table {{
    width:100%;
}}
table, th, td {{
    border: 1px solid black;
    border-collapse: collapse;
}}
th, td {{
    padding: 3px;
    text-align: left;
}}
table#t01 tr:nth-child(odd) {{
    background-color: #f5dfe0;
}}
table#t01 tr:nth-child(even) {{
   background-color:#fff;
}}
</style>
</head>
<body>

<table id="t01">
  <tr>
    <td><strong style="font-size: 12px;">Name</strong></td>
    <td><strong style="font-size: 11px;">{}</strong></td>
  </tr>
  <tr>
    <td><strong style="font-size: 12px;">Specialization</strong></td>
    <td><strong style="font-size: 11px;">{}</strong></td>
  </tr>
  <tr>
    <td><strong style="font-size: 12px;">Address</strong></td>
    <td><strong style="font-size: 11px;">{}</strong></td>
  </tr>
</table>
</body>
</html>
""".format
