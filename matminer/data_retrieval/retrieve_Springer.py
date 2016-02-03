import requests
import os
from lxml import html
from pymatgen.io.cif import CifParser
from pymatgen.matproj.snl import StructureNL

i = 0
j = 1402650

while i <= 0:
    try:
        sim_user_token = os.environ['SPRINGER_KEY']
        page = requests.get('http://materials.springer.com/isp/crystallographic/docs/sd_' + str(j),
                            cookies={'sim-user-token': sim_user_token})
        if page.raise_for_status() is None:  # Check if getting data from above was successful or now
            print 'Success at getting sd_' + str(j)
            i += 1
            parsed_body = html.fromstring(page.content)
            for a_link in parsed_body.xpath('//a/@href'):
                if '.cif' in a_link:
                    cif_link = a_link
                    res = requests.get('http://materials.springer.com' + cif_link,
                                       cookies={'sim-user-token': sim_user_token})
                    with open('ciffile.txt', 'w') as cif_file:
                        cif_file.write(res.content)
                    a = CifParser.from_string(res.content).get_structures()[0]
                    print StructureNL(a, authors=[])
    except Exception as e:
        print e
    j += 1


# print page.status_code == requests.codes.ok      # Check if getting data from above was successful or now

# labels = parsed_body.xpath('//*[@id="general_information"]/div[1]/div/div/ul/li[1]/strong/text()')
# print labels

# Grab links to all images
# images = parsed_body.xpath('//img/@src')
# if not images:
#     sys.exit("Found No Images")
# Convert any relative urls to absolute urls
# images = [urlparse.urljoin(page.url, url) for url in images]
# print 'Found %s images' % len(images)