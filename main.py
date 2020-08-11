#!/usr/bin/env python3
# main.py: configure settings, generate URL's, perform scraping, parsing and store results
import argparse
import confparser
import scraper
import parser as pars
import database

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
parser.add_argument('--flexjobs', action = 'store_true', help = 'run the scraper on \
        flexjobs.com job site using given configuration settings, not compatible with \
        --all command. Does not store result in database. Must be run with viewing option.')
parser.add_argument('--view', help = 'placeholder for viewing options, stores various \
        values for different viewing types, replace later')
parser.add_argument('--config_path', help = 'path to config file, if in current directory \
        and named config.cfg, use \'--config_path config.cfg\'. Must always be specified.')
args = parser.parse_args()
update_db = args.update_db
all_sites = args.all
indeed = args.indeed
monster = args.monster
flexjobs = args.flexjobs
view = args.view
config_path = args.config_path

sites = []
if all_sites: sites.append('--all')
if indeed: sites.append('--indeed')
if monster: sites.append('--monster')
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

if not config_path:
    print('--config path command must be set, please re-run and enter config file path')
    exit(0)

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
    # NOTE: DO STUFF HERE

    # NOTE: REMEMBER TO CLOSE DATABASE


