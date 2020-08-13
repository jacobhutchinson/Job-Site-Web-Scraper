# database.py: contains classes related to storing and managing the MySQL database
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from geopy.geocoders import Nominatim
from tqdm import tqdm

""" Class for accessing and modifying the database for this project """
class Database():
    # Initialize the class and database
    def __init__(self, config):
        super(Database, self).__init__()
        self.config = config
        db_name = self.config.mysql_name[0]
        self.geolocator = Nominatim(user_agent='job_scraper_app')
        self.banned_locs = ['N/A', 'Remote', 'UNAVAILABLE, CA', 'United States']
        # Connect to mysql, create database if not already created
        #   and connect to it
        try:
            self.connection = mysql.connector.connect(user=self.config.mysql_user[0], \
                    password=self.config.mysql_pass[0])
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect username or password for MySQL")
                exit(1)
            else:
                print(err)
                exit(1)
        try:
            self.cursor.execute("USE {}".format(db_name))
        except mysql.connector.Error as err:
            print("Database {} does not exist.".format(db_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                try:
                    self.cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET \
                            'utf8'".format(db_name))
                except mysql.connector.Error as err:
                    print("Failed to create database: {}".format(err))
                    exit(1)
                print("Database {} created successfully".format(db_name))
                self.connection.database = db_name
                self.__create_schema()
            else:
                print(err)
                exit(1)
        print("Connected to MySQL database")

    """ Initialize database schema """
    def __create_schema(self):
        table_schema = (
            "CREATE TABLE `jobs` ("
            "  `source_site` varchar(50) NOT NULL,"
            "  `search_term` varchar(100) NOT NULL,"
            "  `id_var` varchar(100) NOT NULL,"
            "  `job_title` varchar(200) NOT NULL,"
            "  `job_link` varchar(3000) NOT NULL,"
            "  `job_remote` tinyint(1),"
            "  `job_location` varchar(50),"
            "  `job_company` varchar(100),"
            "  `job_summary` varchar(3000),"
            "  `search_date` date NOT NULL,"
            "  `lat` DECIMAL(10, 8),"
            "  `lng` DECIMAL(11, 8),"
            "  PRIMARY KEY (`id_var`)"
            ") ENGINE=InnoDB")
        # Create the schema in the database
        try:
            print("Creating database schema...")
            self.cursor.execute(table_schema)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists...")
            else:
                print(err.msg)
                exit(1)
        else:
            print("Database schema successfully created")

    """ Handles input of new data to database and prints statistics """
    def input_data(self, data):
        new_jobs_added = 0
        old_jobs_updated = 0
        if data is None:
            return 0, 0
        source = data[list(data)[0]][0]
        curr_date = datetime.now().date()
        add_job_listing = ("INSERT INTO jobs "
                          "(source_site, search_term, id_var, job_title, job_link, job_remote, \
                                  job_location, job_company, job_summary, search_date, lat, lng) "
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        update_job_listing = ("UPDATE `jobs`"
                              "SET"
                              "  `job_title` = %s,"
                              "  `job_link` = %s,"
                              "  `job_remote` = %s,"
                              "  `job_location` = %s,"
                              "  `job_company` = %s,"
                              "  `job_summary` = %s,"
                              "  `search_date` = %s,"
                              "  `lat` = %s,"
                              "  `long` = %s"
                              "WHERE"
                              "  `id_var` = %s")
        # Handle data from indeed.com
        if source == 'indeed.com':
            for job_id in tqdm(data):
                job_data = data[job_id]
                remote_data = 1 if job_data[4] == 'Remote' else 0
                for i in range(len(job_data)):
                    if job_data[i] == '' or job_data[i] == 'N/A':
                        job_data[i] = None
                loc = self.get_latlong(job_data[5])
                lat = None if loc == None else loc[0]
                lng = None if loc == None else loc[1]
                new_job = (job_data[0], job_data[8], job_data[1], job_data[2], job_data[3], \
                        remote_data, job_data[5], job_data[6], job_data[7], curr_date, lat, lng)
                try:
                    self.cursor.execute(add_job_listing, new_job)
                except mysql.connector.IntegrityError as err:
                    old_jobs_updated += 1
                    updated_job = (job_data[2], job_data[3], remote_data, job_data[5], \
                            job_data[6], job_data[7], curr_date, lat, lng, job_data[1])
                    try:
                        self.cursor.execute(update_job_listing, updated_job)
                    except Exception as err:
                        print("Unable to update existing job: {}".format(err))
                        exit(1)
                else:
                    new_jobs_added += 1
            self.connection.commit()
        # Handle data from monster.com
        elif source == 'monster.com':
            for job_id in tqdm(data):
                job_data = data[job_id]
                for i in range(len(job_data)):
                    if job_data[i] == '' or job_data[i] == 'N/A':
                        job_data[i] = None
                loc = self.getlatlong(job_data[5])
                lat = None if loc == None else loc[0]
                lng = None if loc == None else loc[1]
                new_job = (job_data[0], job_data[8], job_data[1], job_data[2], job_data[3], \
                        None, job_data[5], job_data[6], None, curr_date, lat, lng)
                try:
                    self.cursor.execute(add_job_listing, new_job)
                except mysql.connector.IntegrityError as err:
                    old_jobs_updated += 1
                    updated_job = (job_data[2], job_data[3], None, job_data[5], job_data[6], \
                            None, curr_date, lat, lng, job_data[1])
                    try:
                        self.cursor.execute(update_job_listing, updated_job)
                    except Exception as err:
                        print("Unable to update existing job: {}".format(err))
                        exit(1)
                else:
                    new_jobs_added += 1
            self.connection.commit()
        # Handle data from flexjobs.com
        elif source == 'flexjobs.com':
            for job_id in tqdm(data):
                job_data = data[job_id]
                remote_data = 1 if job_data[4] == 'Full-Time, 100% Remote Job' else 0
                for i in range(len(job_data)):
                    if job_data[i] == '' or job_data[i] == 'N/A':
                        job_data[i] == None
                loc = self.get_lat_long(job_data[5])
                lat = None if loc == None else loc[0]
                lng = None if loc == None else loc[1]
                new_job = (job_data[0], job_data[8], job_data[1], job_data[2], job_data[3], \
                        remote_data, job_data[5], None, None, curr_date, lat, lng)
                try:
                    self.cursor.execute(add_job_listing, new_job)
                except mysql.connector.IntegrityError as err:
                    old_jobs_updated += 1
                    updated_job = (job_data[2], job_data[3], remote_data, job_data[5], \
                            None, None, curr_date, lat, lng, job_data[1])
                    try:
                        self.cursor.execute(update_job_listing, updated_job)
                    except Exception as err:
                        print("Unable to update existing job: {}".format(err))
                        exit(1)
                else:
                    new_jobs_added += 1
            self.connection.commit()
        else:
            print("Unknown data source, exiting...")
            exit(1)
        return new_jobs_added, old_jobs_updated

    """ Returns all most recent data for given search terms """
    def get_most_recent(self, terms):
        output = {}
        most_recent_search = ("SELECT MAX(`search_date`) FROM jobs "
                 "WHERE `search_term` = %s")
        most_recent_data = ("SELECT * FROM jobs "
                 "WHERE `search_term` = %s AND `search_date` = %s")
        for term in terms:
            self.cursor.execute(most_recent_search, [str(term)])
            most_recent_date = self.cursor.fetchall()
            self.cursor.execute(most_recent_data, [str(term), most_recent_date[0][0]])
            data = self.cursor.fetchall()
            if term not in output:
                output[term] = data
        return output

    """ Returns all the most recent data for given search terms 
        and their respective locations in latitude and longitude """
    def get_latlong(self, loc):
        output = None
        if loc not in self.banned_locs:
            # Calculate lat and long using geopy package
            location = self.geolocator.geocode(loc)
            if location is not None and location.address.find('United States') != -1:
                output = [location.latitude, location.longitude]
        return output

    """ Return all search terms in database """
    def all_search_terms(self):
        output = []
        all_search_terms = ("SELECT DISTINCT `search_term` FROM jobs")
        most_recent_search = ("SELECT MAX(`search_date`) FROM jobs "
                "WHERE `search_term` = %s")
        self.cursor.execute(all_search_terms)
        all_terms = self.cursor.fetchall()
        for term in all_terms:
            self.cursor.execute(most_recent_search, [term[0]])
            most_recent_date = self.cursor.fetchall()
            datapoint = []
            datapoint.append(term[0])
            datapoint.append(most_recent_date[0][0])
            output.append(datapoint)
        return output

    """ Close the connection to the MySQL database """
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
