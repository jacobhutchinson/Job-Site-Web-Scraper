# configparser.py: parses the config file and returns configuration settings for use in the web scraper
from os import path
import configparser

""" Class for holding configuration file information """
class Config:
    def __init__(self):
        """ Initialize configuration file class """

""" Parses the config file and returns configuration settings """
def parse(config_file):
    config = Config()
    parser = configparser.ConfigParser()
    if not path.exists(config_file):
        print('Config file does not exist')
        exit(0)
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

    # Monster config settings
    config.monster_terms = [str(x) for x in parser.get("monster", "monster_terms").split(",")]
    config.monster_job_type = [str(parser.get("monster", "monster_job_type"))]
    if config.monster_job_type[0] not in ['full_time', 'part_time']:
        print("Invalid monster_job_type config")
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

    # MySQL Database config settings
    config.mysql_name = [str(parser.get("mysql", "mysql_name"))]
    if config.mysql_name == '' or not config.mysql_name:
        print("Must enter MySQL database name in config file")
        exit(0)
    config.mysql_user = [str(parser.get("mysql", "mysql_user"))]
    if config.mysql_user == '' or not config.mysql_user:
        print("Must enter MySQL database username in config file")
        exit(0)
    config.mysql_pass = [str(parser.get("mysql", "mysql_pass"))]
    if config.mysql_pass == '' or not config.mysql_pass:
        print("Must enter MySQL database password in config file")
        exit(0)

    return config
