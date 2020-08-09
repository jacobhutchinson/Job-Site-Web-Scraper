# configparser.py: parses the config file and returns configuration settings for use in the web scraper

import configparser

""" Class for holding configuration file information """
class Config:
    def __init__(self):
        """ Initialize configuration file class """

""" Parses the config file and returns configuration settings """
def parse(config_file):
    config = Config()
    parser = configparser.ConfigParser()
    parser.read(config_file)
    # Set config options from configuration file
    config.all_site_terms = [str(x) for x in parser.get("DEFAULT", "all_site_terms").split(",")]

    # Indeed config settings
    config.indeed_terms = [str(x) for x in parser.get("indeed", "indeed_terms").split(",")]
    config.indeed_remote = [str(parser.get("indeed", "indeed_remote"))]
    if config.indeed_remote[0] not in ['remote', 'not-remote']:
        print("Invalid indeed_remote config")
        print(config.indeed_remote)
        exit(0)
    config.indeed_job_type = [str(parser.get("indeed", "indeed_job_type"))]
    if config.indeed_job_type[0] not in ['full_time', 'part_time']:
        print("Invalid indeed_job_type config")
        exit(0)
    config.indeed_exp_level = [str(parser.get("indeed", "indeed_exp_level"))]
    if config.indeed_exp_level[0] not in ['entry_level', 'mid_level', 'senior_level']:
        print("Invalid indeed_exp_level config")
        exit(0)
    config.indeed_radius = [int(parser.get("indeed", "indeed_radius"))]
    if config.indeed_radius[0] not in [5, 25, 50, 100]:
        print("Invalid indeed_radius config")
        exit(0)

    # Monster config settings
    config.monster_terms = [str(x) for x in parser.get("monster", "monster_terms").split(",")]
    config.monster_job_type = [str(parser.get("monster", "monster_job_type"))]
    if config.monster_job_type[0] not in ['full_time', 'part_time']:
        print("Invalid monster_job_type config")
        exit(0)
    config.monster_radius = [int(parser.get("monster", "monster_radius"))]
    if config.monster_radius[0] not in [5, 25, 50, 100, 200]:
        print("Invalid monster_radius config")
        exit(0)

    # Glassdoor config settings
    config.glassdoor_terms = [str(x) for x in parser.get("glassdoor", "glassdoor_terms").split(",")]
    config.glassdoor_job_type = [str(parser.get("glassdoor", "glassdoor_job_type"))]
    if config.glassdoor_job_type[0] not in ['full_time', 'part_time']:
        print("Invalid glassdoor_job_type config")
        exit(0)
    config.glassdoor_radius = [int(parser.get("glassdoor", "glassdoor_radius"))]
    if config.glassdoor_radius[0] not in [5, 25, 50, 100]:
        print("Invalid glassdoor_radius config")
        exit(0)

    # Flexjobs config settings
    config.flexjobs_terms = [str(x) for x in parser.get("flexjobs", "flexjobs_terms").split(",")]
    config.flexjobs_remote = [str(parser.get("flexjobs", "flexjobs_remote"))]
    if config.flexjobs_remote[0] not in ['remote', 'option']:
        print("Invalid flexjobs_remote config")
        exit(0)
    config.flexjobs_schedule = [str(parser.get("flexjobs", "flexjobs_schedule"))]
    if config.flexjobs_schedule[0] not in ['full_time', 'part_time']:
        print("Invalid flexjobs_schedule config")
        exit(0)
    config.flexjobs_exp_level = [str(parser.get("flexjobs", "flexjobs_exp_level"))]
    if config.flexjobs_exp_level[0] not in ['entry_level', 'experienced']:
        print("Invalid flexjobs_exp_level config")
        exit(0)
    config.flexjobs_travel = [str(parser.get("flexjobs", "flexjobs_travel"))]
    if config.flexjobs_travel[0] not in ['yes', 'no']:
        print("Invalid flexjobs_travel config")
        exit(0)

    return config
