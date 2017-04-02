""" Scrape all of the tunes from tunearch.org, storing their metadata and abc notation """

from urllib import parse
import json
import requests
from lxml import html
from unidecode import unidecode

# pylint: disable=line-too-long
ORIGINAL_SCRAPE_URL = "http://tunearch.org/w/index.php?title=Special%3AAsk&q=%5B%5BCategory%3ATune%5D%5D&po=%3FIs+also+known+as%3DAlso+known+as%0D%0A%3FTheme+code+index%3DTheme+Code+Index%0D%0A%3FWas+composed+by%3DArranger%2FComposer%0D%0A%3FIt+comes+from%3DCountry%0D%0A%3FHas+genre%3DGenre%0D%0A%3FHas+rhythm%3DRhythm%0D%0A%3FIs+in+the+key+of%3DKey%0D%0A%3FHas+historical+geographical+allegiances%3DHistory%0D%0A&eq=yes&p%5Bformat%5D=json&sort%5B0%5D=Theme_code_index&order%5B0%5D=ASC&sort_num=&order_num=ASC&p%5Blimit%5D=20&p%5Boffset%5D=20&p%5Blink%5D=all&p%5Bsort%5D=Theme_code_index&p%5Bheaders%5D=show&p%5Bmainlabel%5D=Tune&p%5Bintro%5D=&p%5Boutro%5D=&p%5Bsearchlabel%5D=JSON&p%5Bdefault%5D=&eq=yes"
# pylint: enable=line-too-long

def scrape_abc_notation(url):
    """ Gets the abc notation from the provided tunearch tune url """
    response = requests.get(url)
    if response.status_code is not 200:
        response.raise_for_status()

    tree = html.fromstring(response.content)
    content = tree.xpath('//pre/text()')
    # just take the first pre element contents for now
    return unidecode(content[0])

def format_tune_entry(tune):
    """ Format a tune entry for archival """
    abc_transcription = scrape_abc_notation(tune['fullurl'])
    return {
        'name': tune['fulltext'],
        'url': tune['fullurl'],
        'abc': abc_transcription
    }

def request_tunes(page, num_tunes=100):
    """ Download a page of tunes from tunearch as json """
    args = {
        'order_num': ['ASC'],
        'title': ['Special:Ask'],
        'sort[0]': ['Theme_code_index'],
        'order[0]': ['ASC'],
        'p[format]': ['json'],
        'q': ['[[Category:Tune]]'],
        'p[offset]': [str(page*num_tunes)],
        'p[searchlabel]': ['JSON'],
        'p[limit]': [str(num_tunes)]
    }
    query = parse.urlencode(args, doseq=True)
    target_url = "http://tunearch.org/w/index.php?{}".format(query)
    response = requests.get(target_url)
    if response.status_code is not 200:
        response.raise_for_status()

    tunes_dict = response.json()['results']

    return [format_tune_entry(tune) for tune in tunes_dict.values()]

def transcription_is_empty(abc):
    """ Check if an abc transcription is empty """
    return ("No Score" or
            "REPLACE THIS LINE WITH THE ABC CODE OF THIS TUNE") in abc

def request_all_tunes():
    """ Get all tunes in the tune archive, page by page """
    all_tunes = []
    page = 0
    while True:
        page_of_tunes = request_tunes(page)
        filtered_page = [tune for tune in page_of_tunes
                         if not transcription_is_empty(tune['abc'])]
        all_tunes.extend(filtered_page)
        print("Got {} more tunes, ".format(len(filtered_page)) +
              "writing {} tunes to file...".format(len(all_tunes)))
        with open("tunes.json", "w") as outfile:
            outfile.writelines(json.dumps(all_tunes))
        if len(page_of_tunes < 100):
            print("Presuming that page of {} tunes ".format(len(page_of_tunes)) +
                  "is the last page, quitting.")
            break

def main():
    """ The main executable """
    request_all_tunes()

if __name__ == '__main__':
    main()
