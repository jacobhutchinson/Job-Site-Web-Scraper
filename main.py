#!/usr/bin/env python3
# main.py: configure settings, generate URL's, perform scraping, parsing and store results
import requests
from bs4 import BeautifulSoup
import argparse
import confparser

##############################################
# Command Line Arguments and Config Settings #
##############################################

# Deal with parsed arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('--update_db', action = 'store_true', help = 'run the scraper \
        with given configuration settings for all websites and input that information \
        into the database. Can call a viewing option as well afterwards to view the update database.')
parser.add_argument('--all', action = 'store_true', help = 'run the scraper with \
        given configuration settings for all websites. Does not store results in \
        database. Must be run with viewing option.')
parser.add_argument('--indeed', action = 'store_true', help = 'run the scraper on \
        indeed.com job site using given configuartion settings, not compatible with \
        --all command. Does not store result in database. Must be run with viewing option.')
parser.add_argument('--monster', action = 'store_true', help = 'run the scraper on \
        monster.com job site using given configuration settings, not compatible with \
        --all command. Does not store result in database. Must be run with viewing option.')
parser.add_argument('--glassdoor', action = 'store_true', help = 'run the scraper on \
        glassdoor.com job site using given configuration settings, not compatible with \
        --all command. Does not store result in database. Must be run with viewing option.')
parser.add_argument('--flexjobs', action = 'store_true', help = 'run the scraper on \
        flexjobs.com job site using given configuration settings, not compatible with \
        --all command. Does not store result in database. Must be run with viewing option.')
parser.add_argument('--view', help = 'placeholder for viewing options, stores various \
        values for different viewing types, replace later')
args = parser.parse_args()
update_db = args.update_db
all_sites = args.all
indeed = args.indeed
monster = args.monster
glassdoor = args.glassdoor
flexjobs = args.flexjobs
view = args.view

sites = []
if all_sites: sites.append('--all')
if indeed: sites.append('--indeed')
if monster: sites.append('--monster')
if glassdoor: sites.append('--glassdoor')
if flexjobs: sites.append('--flexjobs')

# Logic for parsed arguments
if update_db and sites:
    print("--update_db command cannot be run with the " + ', '.join(sites) + ' command(s).')
    exit(0)

if all_sites and len(sites) > 1:
    sites_not_all = sites.copy()
    sites_not_all.remove('--all')
    print('--all command cannot be run with ' + ', '.join(sites_not_all) + ' command(s)')
    exit(0)

if sites and not view:
    print(', '.join(sites) + ' command(s) cannot be run without a viewing option.')
    exit(0)

# Parse the config file
config = confparser.parse('config.cfg')

###################
# Update Database #
###################

if update_db:
    # Generate iterable URL's to scrape HTML from
   URL_gen = URL_generator()

