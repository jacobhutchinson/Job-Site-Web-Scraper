# database.py: contains classes related to storing and managing the MySQL database
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime

""" Class for accessing and modifying the database for this project """
class Database():
    # Initialize the class and database
    def __init__(self, config):
        super(Database, self).__init__()
        self.config = config
        db_name = self.config.mysql_name[0]
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
        source = data[list(data)[0]][0]
        curr_date = datetime.now().date()
        add_job_listing = ("INSERT INTO jobs "
                          "(source_site, search_term, id_var, job_title, job_link, job_remote, \
                                  job_location, job_company, job_summary, search_date) "
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        update_job_listing = ("UPDATE `jobs`"
                              "SET"
                              "  `job_title` = %s,"
                              "  `job_link` = %s,"
                              "  `job_remote` = %s,"
                              "  `job_location` = %s,"
                              "  `job_company` = %s,"
                              "  `job_summary` = %s,"
                              "  `search_date` = %s"
                              "WHERE"
                              "  `id_var` = %s")
        # Handle data from indeed.com
        if source == 'indeed.com':
            for job_id in data:
                job_data = data[job_id]
                remote_data = 1 if job_data[4] == 'Remote' else 0
                for i in range(len(job_data)):
                    if job_data[i] == '' or job_data[i] == 'N/A':
                        job_data[i] = None
                new_job = (job_data[0], job_data[8], job_data[1], job_data[2], job_data[3], \
                        remote_data, job_data[5], job_data[6], job_data[7], curr_date)
                try:
                    self.cursor.execute(add_job_listing, new_job)
                except mysql.connector.IntegrityError as err:
                    old_jobs_updated += 1
                    updated_job = (job_data[2], job_data[3], remote_data, job_data[5], \
                            job_data[6], job_data[7], curr_date, job_data[1])
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
            for job_id in data:
                job_data = data[job_id]
                for i in range(len(job_data)):
                    if job_data[i] == '' or job_data[i] == 'N/A':
                        job_data[i] = None
                new_job = (job_data[0], job_data[8], job_data[1], job_data[2], job_data[3], \
                        None, job_data[5], job_data[6], None, curr_date)
                try:
                    self.cursor.execute(add_job_listing, new_job)
                except mysql.connector.IntegrityError as err:
                    old_jobs_updated += 1
                    updated_job = (job_data[2], job_data[3], None, job_data[5], job_data[6], \
                            None, curr_date, job_data[1])
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
            for job_id in data:
                job_data = data[job_id]
                remote_data = 1 if job_data[4] == 'Full-Time, 100% Remote Job' else 0
                for i in range(len(job_data)):
                    if job_data[i] == '' or job_data[i] == 'N/A':
                        job_data[i] == None
                new_job = (job_data[0], job_data[8], job_data[1], job_data[2], job_data[3], \
                        remote_data, job_data[5], None, None, curr_date)
                try:
                    self.cursor.execute(add_job_listing, new_job)
                except mysql.connector.IntegrityError as err:
                    old_jobs_updated += 1
                    updated_job = (job_data[2], job_data[3], remote_data, job_data[5], \
                            None, None, curr_date, job_data[1])
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

    """ Close the connection to the MySQL database """
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
