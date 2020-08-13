# scraper.py: contains classes related to scraping HTML of various sites
# import csv
import grequests
from tqdm import tqdm

### NOTE: decided against using zipcodes for the time being, may re-incorporate later
#""" Parses the zipcode file given and returns correspond zipcodes, lat, long, city, state id and state """
#def load_zips_csv(zips_file):
#    with open(zips_file, newline='') as f:
#        reader = csv.reader(f)
#        output = []
#        for row in reader:
#            r = []
#            for i in range(0,6):
#                r.append(row[i])
#            output.append(r)
#        return output

""" Class for handling URL generation for scraping various sites """
class URL_generator():
    # Initialize the class
    def __init__(self, config):
        super(URL_generator, self).__init__()
        self.config = config

    # Return an iterable of all indeed.com url's for the given config
    def indeed_url_generator(self):
        base = 'https://www.indeed.com/jobs?q='
        output = {}
        all_terms = self.config.all_site_terms + self.config.indeed_terms
        if '' in all_terms:
            all_terms.remove('')
        for search_term in all_terms:
            term_output = []
            words = search_term.split(" ")
            # Search first 100 pages of results
            for a in range(1, 101):
                url = base
                # Add term to url
                for i in range(len(words)):
                    word = words[i]
                    if i != (len(words) - 1):
                        url += str(word) + '+'
                    else:
                        url += str(word)
                # Add job type to url
                job_type = 'fulltime' if self.config.indeed_job_type[0] == 'full_time' else 'parttime'
                url += '&jt=' + job_type
                # Add experience level to url
                exp_level = str(self.config.indeed_exp_level[0])
                url += '&explvl=' + exp_level
                # Add remote preferences
                if self.config.indeed_remote[0] == 'remote':
                    # This string is hardcoded into the url for some reason
                    url+='&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11'
                # Add page number to url
                url += '&start=' + str((a-1)*10)
                term_output.append(url)
            output[search_term] = term_output
        return output

    # Return an iterable of all monster.com url's for the given config
    def monster_url_generator(self):
        base = 'https://www.monster.com/jobs/search/'
        output = {}
        all_terms = self.config.all_site_terms + self.config.monster_terms
        if '' in all_terms:
            all_terms.remove('')
        for search_term in all_terms:
            term_output = []
            words = search_term.split(' ')
            # Search first 100 pages of results
            for a in range(1, 11):
                url = base
                # Add job type to url
                if self.config.monster_job_type[0] == 'full_time':
                    job_type = 'Full-Time_8?'
                else:
                    job_type = 'Part-Time_8?'
                url += job_type
                # Add term to url
                url += 'q='
                for i in range(len(words)):
                    word = words[i]
                    if i != (len(words) - 1):
                        url += str(word) + '-'
                    else:
                        url += str(word)
                # Add page number to url
                url += '&stpage=1&page=' + str(a)
                term_output.append(url)
            output[search_term] = term_output
        return output

    # Return an iterable of all flexjobs.com url's for the given config
    def flexjobs_url_generator(self):
        base = 'https://www.flexjobs.com/search?'
        output = {}
        all_terms = self.config.all_site_terms + self.config.flexjobs_terms
        if '' in all_terms:
            all_terms.remove('')
        for search_term in all_terms:
            term_output = []
            words = search_term.split(' ')
            # Search the first 100 pages of results (or less if less pages have results)
            for a in range(1, 101):
                url = base
                # Add experience level to url
                if self.config.flexjobs_exp_level[0] == 'entry_level':
                    url += 'career_level[]=Entry-Level'
                else:
                    url += 'career_level[]=Experienced'
                # Add job type to url (set to employee by default)
                url += '&jobtypes[]=Employee'
                # Don't add location to url
                url += '&location='
                # Add page number to url
                url += '&page=' + str(a)
                # Add schedule to url
                if self.config.flexjobs_schedule[0] == 'full_time':
                    url += '&schedule[]=Full-Time'
                else:
                    url += '&schedule[]=Part-Time'
                # Add terms to url
                url += '&search='
                for i in range(len(words)):
                    word = words[i]
                    if i != (len(words) - 1):
                        url += str(word) + '+'
                    else:
                        url += str(word)
                # Add remote amount to url
                if self.config.flexjobs_remote[0] == 'remote':
                    url += '&tele_level[]=All+Telecommuting'
                else:
                    url += '&tele_level[]=Option+for+Telecommuting'
                # Add travel preference to url
                if self.config.flexjobs_travel[0] == 'no':
                    url += '&will_travel[]=No'
                else:
                    url += '&will_travel[]=Yes%2C+a+bit'
                term_output.append(url)
            output[search_term] = term_output
        return output

    # Return iterables for url's of all websites in current config
    def all_url_generator(self):
        indeed_urls = self.indeed_url_generator()
        monster_urls = self.monster_url_generator()
        flexjobs_urls = self.flexjobs_url_generator()
        return indeed_urls, monster_urls, flexjobs_urls


""" Class for scraping HTML from given URL's using multithreading w/ grequests package """
class Scraper():
    # Initialize the class
    def __init__(self, n):
        super(Scraper, self).__init__()
        # n: number of requests to send simultaneously
        self.n = n

    """ Exception handling for the class """
    def exception(self, request, exception):
        print('Exception: {}: {}'.format(request.url, exception))
        exit(0)

    """ Simultaneously sends HTML requests for all given URL's """
    def async_requests(self, urls):
        html_results = grequests.map((grequests.get(u) for u in urls), exception_handler=self.exception)
        return html_results

    def get_html(self, urls):
        new_urls = {}
        for s_term in urls:
            row = urls[s_term]
            new_urls[s_term] = [row[i:i + self.n] for i in range(0, len(row), self.n)]
        output = {}
        for search_term in new_urls:
            term = new_urls[search_term]
            term_output = []
            print('Scraping for term \'' + str(search_term) + '\'...')
            for a in tqdm(range(len(term))):
                row = term[a]
                term_output += self.async_requests(row)
            output[search_term] = term_output
        return output




