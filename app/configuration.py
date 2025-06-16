import pymysql

class UserDbConfiguration:
    DB_HOSTNAME = 'localhost'       # Database hostname (localhost or an IP address)
    DB_PORT = 3307            # MySQL port (default is 3306, but changed to 3307 for this example)
    DB_USERNAME = 'root'            # MySQL username
    DB_PASSWORD = 'x1sana2axuseen'  # MySQL password
    DB_NAME = 'online_education'    # Database name

    @staticmethod
    def get_db_connection():
        """
        Establish and return a connection to the MySQL database.
        :return: pymysql.connect object
        """
        # Creating the connection using the class variables
        connection = pymysql.connect(
            host=UserDbConfiguration.DB_HOSTNAME,
            user=UserDbConfiguration.DB_USERNAME,
            password=UserDbConfiguration.DB_PASSWORD,
            database=UserDbConfiguration.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor  # This ensures that query results are returned as dictionaries
        )
        return connection
