# parser.py: contains classes related to parsing scraped HTML for various data
from bs4 import BeautifulSoup
from tqdm import tqdm

""" Class for parsing HTML from various sites to get data """
class Parser():
    # Initialize the class
    def __init__(self):
        super(Parser, self).__init__()

    """ Parsing for indeed.com HTML """
    def parse_indeed(self, html):
        print('Parsing indeed.com HTML...')
        data = {}
        for search_term in html:
            term = html[search_term]
            page_num = 1
            for page in term:
                soup = BeautifulSoup(page.content, 'html.parser')
                job_elems = soup.find_all("div", class_="jobsearch-SerpJobCard unifiedRow row result")
                for job_elem in job_elems:
                    title_class_a = job_elem.find('h2', class_='title').find('a')
                    div_sjcl = job_elem.find('div', class_='sjcl')
                    div_summary = job_elem.find('div', class_='summary')
                    id_data = job_elem['data-jk']
                    title_data = title_class_a['title']
                    link_data = 'https://www.indeed.com' + title_class_a['href']
                    remote_data = div_sjcl.find('span', class_= 'remote')
                    if remote_data:
                        remote_data = remote_data.text.replace('\n', '')
                    location_data = div_sjcl.find('div', class_ = 'recJobLoc')['data-rc-loc']
                    company_data = div_sjcl.find('span', class_='company').text.replace('\n', '')
                    summary_data = div_summary.find('ul')
                    if summary_data:
                        summary_data = summary_data.text.replace('\n', '')
                    job_data = []
                    job_data.append('indeed.com')
                    job_data.append(id_data)
                    job_data.append(title_data)
                    job_data.append(link_data)
                    job_data.append(remote_data)
                    job_data.append(location_data)
                    job_data.append(company_data)
                    job_data.append(summary_data)
                    job_data.append(str(search_term))
                    if id_data not in data:
                        data[id_data] = job_data
                page_num += 1
        return data

    """ Parsing for monster.com HTML """
    def parse_monster(self, html):
        print('Parsing monster.com HTML...')
        data = {}
        for search_term in html:
            term = html[search_term]
            start_num = None
            page_num = 1
            done = False
            for page in term:
                if not done:
                    soup = BeautifulSoup(page.content, 'html.parser')
                    results = soup.find(id='ResultsContainer')
                    if results is None:
                        print('Blocked form scraping monster.com :(')
                        return None
                    job_elems = results.find_all('section', class_='card-content')
                    if page_num == 1:
                        start_num = len(job_elems)
                    else:
                        if len(job_elems) <= start_num:
                            done = True
                            last_page_num = page_num - 2
                            last_page = term[last_page_num]
                            soup = BeautifulSoup(last_page.content, 'html.parser')
                            results = soup.find(id='ResultsContainer')
                            job_elems = results.find_all('section', class_='card-content')
                            for job_elem in job_elems:
                                title_elem = job_elem.find('h2', class_='title')
                                if title_elem:
                                    source_data = 'monster.com'
                                    try:
                                        id_data = job_elem['data-postingid']
                                    except KeyError:
                                        id_data = job_elem['data-jobid']
                                    link_data = title_elem.find('a')['href']
                                    title_data = title_elem.text.replace('\n', '')
                                    company_data = job_elem.find('div', class_='company').text.replace('\n', '')
                                    location_data = job_elem.find('div', class_='location').text.replace('\n', '')
                                    new_data = []
                                    new_data.append(source_data)
                                    new_data.append(id_data)
                                    new_data.append(title_data)
                                    new_data.append(link_data)
                                    # Sadly, monster.com does not collect info on whether a
                                    # job posting is remote or not
                                    new_data.append('N/A')
                                    new_data.append(location_data)
                                    new_data.append(company_data)
                                    # monster.com's summaries for jobs are hidden behind another request
                                    # for each job, and so to not accidentally DDOS monster.com for 10,000
                                    # job summaries, I decided to not collect that information
                                    new_data.append('N/A')
                                    new_data.append(str(search_term))
                                    if title_data not in data:
                                        data[title_data] = new_data
                    page_num += 1
        return data

    """ Parsing for flexjobs.com HTML """
    def parse_flexjobs(self, html):
        print('Parsing flexjobs.com HTML...')
        data = {}
        for search_term in html:
            term = html[search_term]
            page_num = 1
            done = False
            for page in term:
                if not done:
                    soup = BeautifulSoup(page.content, 'html.parser')
                    ul_titleheader = soup.find('ul', id='titleheader')
                    if ul_titleheader:
                        job_elems = soup.find_all('li', class_='list-group-item job')
                        for job_elem in job_elems:
                            source_data = 'flexjobs.com'
                            id_data = job_elem['data-job']
                            div_col10 = job_elem.find('div', class_='col-10 jt-title').find('a')
                            title_data = div_col10.text.replace('\n', '')
                            link_data = 'flexjobs.com' + div_col10['href'].replace('\n', '')
                            remote_data = job_elem.find('span', class_='text-danger').text.replace('\n', '')
                            div_cols = job_elem.find_all('div', class_='col')
                            if remote_data != 'Full-Time, 100% Remote Job':
                                location_data = div_cols[1].text.replace('\n', '')
                            else:
                                location_data = 'N/A'
                            # flexjobs sadly doesn't let you see company info without a paid account
                            company_data = 'N/A'
                            # flexjobs sadly doesn't send descriptions over HTML when using grequests package
                            summary_data = 'N/A'
                            new_data = []
                            new_data.append(source_data)
                            new_data.append(id_data)
                            new_data.append(title_data)
                            new_data.append(link_data)
                            new_data.append(remote_data)
                            new_data.append(location_data)
                            new_data.append(company_data)
                            new_data.append(summary_data)
                            new_data.append(str(search_term))
                            if id_data not in data:
                                data[id_data] = new_data
                    else:
                        done = True
                page_num += 1
        return data

    """ Parsing HTML for all websites """
    def parse(self, indeed_html, monster_html, flexjobs_html):
        indeed_data = self.parse_indeed(indeed_html)
        monster_data = self.parse_monster(monster_html)
        flexjobs_data = self.parse_flexjobs(flexjobs_html)
        return indeed_data, monster_data, flexjobs_data
