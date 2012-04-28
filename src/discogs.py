import logging
import urllib
import re
try:
    import discogs_client
    discogs_client.user_agent = 'MusicSorter, BetaVersion'
    discogs_support = True
except ImportError:
    discogs_support = False

def need_discogs_support(f):
    def wrapper(*args, **kwargs):
        if discogs_support:
            f(*args, **kwargs)
        else:
            logging.error("no discogs support")
    return wrapper


@need_discogs_support
def search(string):
    """
    Search for a string in the discogs database
        @param : the query string, unicode encoded
        @return :   a list containing the results as discogs objects
                    None if no result were to be found
    """
    try:
        logging.debug("guessing on directory " + string)
        d = clean_name(string)
        if not d:
            logging.debug("Directory name is empty")
            return
        logging.debug("Looking for " + d)
        search = discogs_client.Search(d)
        logging.debug("Found a perfect result")
        return search.exactresults
    except discogs_client.DiscogsAPIError as e:
        logging.error("Issue on discogs")
        logging.error(e)
        return None
    except KeyError:
            logging.debug("Perfect result not found")
            return search.results

def clean_name(string):
    bracket = re.compile("\[.*?\]")
    parenthesis = re.compile("\(.*?\)")
    string = string.replace("_", " ")
    string = string.replace(".", " ")
    string = re.sub(parenthesis, "", string)
    string = re.sub(bracket, "", string)
    string = string.strip()
    return string
