#!/usr/bin/env python3
# main.py: configure settings, generate URL's, perform scraping, parsing and store results
import argparse
import confparser
import scraper
import parser as pars
import database
from datetime import date, datetime
import views

#######################
# Utility IO Function #
#######################

def term_prompt(db):
    # Get all search terms with most recent search dates
    terms_dates = db.all_search_terms()
    terms = []
    dates = []
    for i in range(len(terms_dates)):
        terms.append(terms_dates[i][0])
        dates.append(terms_dates[i][1])
    # Prompt user for terms to view
    selected_terms = []
    print("Please type which of the following terms you want to search for, " + \
            "or type DONE to finish. \nMore than one term can be selected. Enter " + \
            "a term a second time to remove it from the list.")
    not_done = True
    while not_done:
        print('Terms: ')
        for term in terms:
            if term in selected_terms:
                print('[X] {}'.format(term))
            else:
                print('[ ] {}'.format(term))
        not_selected = True
        while not_selected:
            selected_term = input('Enter a search term or DONE to finish: ')
            if selected_term not in terms and selected_term != 'DONE':
                print('Invalid term, please enter another term')
            elif selected_term == 'DONE':
                if len(selected_terms) == 0:
                    print('Must enter at least one term')
                else:
                    not_done = False
                    not_selected = False
            else:
                if selected_term not in selected_terms:
                    selected_terms.append(selected_term)
                    k = None
                    for j in range(len(terms)):
                        if terms[j] == selected_term:
                            k = j
                    term_date = dates[k]
                    result = datetime.now().date() - term_date
                    if result.days >= 28:
                        print('WARNING: this term has not been updated in 28 days. Job listings may not be accurate.')
                else:
                    selected_terms.remove(selected_term)
                not_selected = False
    return selected_terms

##############################################
# Command Line Arguments and Config Settings #
##############################################

# Deal with parsed arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('--update_db', action = 'store_true', help = 'run the scraper \
        with given configuration settings for all websites and input that information \
        into the database. Can call a viewing option as well afterwards to view the update database.')
parser.add_argument('--view_map', action= 'store_true', help = 'View the most recent data for \
        selected search terms on top of a map. Multiple viewwing options can not be viewed \
        simultaneously.')
parser.add_argument('--view_loc', action = 'store_true', help = 'View the most recent data for \
        selected search terms that are a given distance from a specific location. Multiple \
        viewing options can not be viewed simultaneously.')
parser.add_argument('--view_remote', action = 'store_true', help = 'View the most recent data for \
        remote jobs in selected search terms, printed in console. Multiple viewing options can not \
        be viewed simultaneously.')
parser.add_argument('--config_path', help = 'path to config file, if in current directory \
        and named config.cfg, use \'--config_path config.cfg\'. Must always be specified to \
        update database..')

args = parser.parse_args()
update_db = args.update_db
view_map = args.view_map
view_loc = args.view_loc
view_remote = args.view_remote
config_path = args.config_path

if not config_path:
    print('--config path command must be set, please re-run and enter config file path')
    exit(0)

if sum([view_map, view_loc, view_remote]) > 1:
    print('--view_map, --view_loc and --view_remote commands cannot be set simultaneously,\
             please re-run with only one')
    exit(0)

if not update_db and not view_map and not view_loc and not view_remote:
    print('Cannot be run without commands. Use --help command to see all')

# Parse the config file
config = confparser.parse(config_path)

###################
# Update Database #
###################

if update_db:
    # Initialize database class and connect to MySQL database
    db = database.Database(config)
    # Generate iterable URL's to scrape HTML from
    url_gen = scraper.URL_generator(config)
    indeed_urls, monster_urls, flexjobs_urls = url_gen.all_url_generator()
    # Initialize scraper and scrape all URL's
    scra = scraper.Scraper(10)
    print('Scraping indeed.com...')
    indeed_html = scra.get_html(indeed_urls)
    print('Scraping monster.com...')
    monster_html = scra.get_html(monster_urls)
    print('Scraping flexjobs.com...')
    flexjobs_html = scra.get_html(flexjobs_urls)
    # Initialize parser and parse all HTML
    par = pars.Parser()
    indeed_data, monster_data, flexjobs_data = par.parse(indeed_html, monster_html, flexjobs_html)
    # Store all data in MySQL database
    print("Storing and calculating coordinates for indeed.com data...")
    indeed_jobs_added, indeed_jobs_updated = db.input_data(indeed_data)
    print("Storing and calculating coordinates for monster.com data...")
    monster_jobs_added, monster_jobs_updated = db.input_data(monster_data)
    print("Storing and calculating coordinates for flexjobs.com data...")
    flexjobs_jobs_added, flexjobs_jobs_updated = db.input_data(flexjobs_data)
    print("Database successfully updated\nNew indeed.com jobs: {}\nUpdated indeed.com jobs: {}\
            \nNew monster.com jobs: {}\nUpdated monster.com jobs: {}\nNew flexjobs.com jobs: {}\
            \nUpdated flexjobs.com jobs: {}".format(indeed_jobs_added, indeed_jobs_updated, \
            monster_jobs_added, monster_jobs_updated, flexjobs_jobs_added, flexjobs_jobs_updated))
    # Close database connection
    db.close_connection()

####################
# View Data on Map #
####################

if view_map:
    # Initialize database class and connect to MySQL database
    db = database.Database(config)
    selected_terms = term_prompt(db)
    # Get the most recent data by search term, with correspond
    #    latitude and longitude
    data = db.get_most_recent(selected_terms)
    views = views.Views()
    views.map_view(data)

#########################
# View Data by Location #
#########################

if view_loc:
    # Initialize database class and connect to MySQL database
    db = database.Database(config)
    loc_chosen = False
    while not loc_chosen:
        loc = input('Please input an address: ')
        latlong = db.get_latlong(loc)
        if latlong is not None:
            loc_chosen = True
        else:
            print('Invalid location, please enter another address: ')
    dist_chosen = False
    while not dist_chosen:
        dist = input('Please enter a max distance, in miles: ')
        try:
            dist = float(dist)
            dist_chosen = True
        except ValueError:
            print('Invalid distance value, please enter another: ')
    selected_terms = term_prompt(db)
    data = db.get_most_recent(selected_terms)
    dist_data = db.filter_distance(data, latlong, dist)
    views = views.Views()
    views.map_view(dist_data)

####################
# View Remote Jobs #
####################

if view_remote:
    # Initialize database class and connect to MySQL database
    db = database.Database(config)
    selected_terms = term_prompt(db)
    data = db.get_most_recent(selected_terms)
    remote_data = db.filter_remote(data)
    views = views.Views()
    views.list_jobs(remote_data)
