# scraper.py: contains classes related to scraping HTML of various sites

""" Class for handling URL generation for scraping various sites """
class URL_generator(config):
    # Initialize the class
    def __init__(self):
        super(URL_generator, self).__init__()
        self.config = config

    # Return an iterable of all indeed.com url's for the given config
    def indeed_url_generator():

        return

    # Return an iterable of all monster.com url's for the given config
    def monster_url_generator():
        return

    # Return an iterable of all glassdoor.com url's for the given config
    def glassdoor_url_generator():
        return

    # Return an iterable of all flexjobs.com url's for the given config
    def flexjobs_url_generator():
        return

    # Return iterables for url's of all websites in current config
    def all_url_generator:
        indeed_urls = indeed_url_generator()
        monster_urls = monster_url_generator()
        glassdoor_urls = glassdoor_url_generator()
        flexjobs_urls = flexjobs_url_generator()
        return indeed_urls, monster_urls, glassdoor_urls, flexjobs_urls

