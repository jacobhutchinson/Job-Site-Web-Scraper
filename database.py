# database.py: contains classes related to storing and managing the MySQL database
import mysql.connector
from mysql.connector import errorcode

""" Class for accessing and modifying the database for this project """
class Database():
    # Initialize the class and database
    def __init__(self, config):
        super(Database, self).__init__()
        self.config = config
        try:
            connection = mysql.connector.connect(user=self.config.mysql_user[0], \
                    password=self.config.mysql_pass[0], database=self.config.mysql_name[0])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect username or password for MySQL database")
                exit(0)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("MySQL database does not exist")
                exit(0)
            else:
                print(err)
                exit(0)
        else:
            self.connection = connection

        def close_connection():
            self.connection.close()
