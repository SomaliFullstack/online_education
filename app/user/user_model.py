import pymysql
print(f"PyMySQL version: {pymysql.__version__}")
print(f"MySQL client version: {pymysql.get_client_info()}")
from app.configuration import UserDbConfiguration


# Database connection
class UserDatabase:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def make_connection(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            self.cursor = self.connection.cursor()
            print('Database connection established.')
        except Exception as e:
            print(f'Connection failed: {e}')

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection: #ui :
            self.connection.close()
            print('Database connection closed.')


class UserModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.cursor = db_connection.cursor  # Ensure cursor is initialized properly

    def getting_user_by_email(self, email):
        try:
            # First, try to fetch user from the student table
            sql = """
                SELECT r.id, s.student_id, r.email, r.pass1, r.name 
                FROM registration r
                JOIN student s ON r.email = s.email
                WHERE r.email = %s
            """
            self.cursor.execute(sql, (email,))
            result = self.cursor.fetchone()

            if result:
                # If user is found in the student table
                user = {
                    'id': result[0],  # registration id
                    'student_id': result[1],  # student table student_id
                    'email': result[2],
                    'password': result[3],
                    'name': result[4],
                }
                return user
            else:
                # If user is not found in the student table, fetch from the users table
                sql = """
                    SELECT id, email, name, password 
                    FROM users 
                    WHERE email = %s
                """
                self.cursor.execute(sql, (email,))
                result = self.cursor.fetchone()

                if result:
                    # If user is found in the users table
                    user = {
                        'id': result[0],  # users table id
                        'student_id': None,  # No student_id for non-student users
                        'email': result[1],
                        'password': result[3],
                        'name': result[2],
                    }
                    return user

            return None  # Return None if no user is found

        except Exception as e:
            print(f'Error fetching user by email: {e}')
            return None

    def teacher_info(self, email):
        try:
            sql = """SELECT * FROM teachers WHERE email = %s"""  # Add WHERE clause to filter by email
            self.cursor.execute(sql, (email,))
            result = self.cursor.fetchone()

            if result:
                user = {
                    'id': result[0],
                    'name': result[1],  # Teacher name
                    'email': result[2],
                    'phone': result[3],
                    'created_at': result[4],
                    'username': result[5],
                    'role': result[6]
                }
                return user

            else:
                return None
        except Exception as e:
            print(f"Error fetching teacher info: {e}")
            return None

    def store_user_in_users(self, user):
        print(f"Received user name: {user.get('name')}")
        """Store user data in users table after registration."""
        try:
            # Ensure that 'name' is available in the user dictionary
            if not user.get('name'):
                raise ValueError("User name is required and cannot be empty.")


            # Ensure to insert values for all required columns (email, password, name, role, status)
            sql = """
                INSERT INTO users (email, password, name, role, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            # Add 'role' and 'status' explicitly or use default if not provided
            role = user.get('role', 'regular')  # Default to 'regular' if not provided
            status = user.get('status', 'pending')  # Default to 'pending' if not provided

            self.cursor.execute(sql, (user['email'], user['password'], user['name'], role, status))
            self.db_connection.connection.commit()  # Make sure to commit the changes
            print('User successfully stored in users table.')
            return True, 'User successfully stored in users table.'
        except Exception as e:
            print(f'Error storing user in users table: {e}')
            return False, f'Error: {e}'

    def register_user(self, email, pass1, name, name2, name3, gender, educationSelect):
        """Register a new user."""
        sql = """
            INSERT INTO registration(Email, pass1,role, name, name2, name3, Gender, educationSelect,status)
            VALUES(%s, %s, %s, %s, %s, %s, %s,%s,%s)
        """
        try:
            self.cursor.execute(sql, (email, pass1, 'regular', name, name2, name3, gender, educationSelect, 'pending'))
            self.db_connection.connection.commit()  # Commit the changes to registration table
            print('User registered successfully!')

            # After registration, store the user into the users table
            # Pass the name to the store_user_in_users method as well
            user = {'email': email, 'password': pass1, 'name': name}  # Include name here
            success, message = self.store_user_in_users(user)  # Store the user in users table

            if success:
                return True, 'User registered and stored successfully in users table!'
            else:
                return False, message
        except Exception as e:
            print('Failed to register user.')
            print(f'Error: {e}')
            return False, f'Error: {e}'

    def get_student_by_email(self, email):
        query = "SELECT * FROM student WHERE email = %s"
        try:
            self.db_connection.cursor.execute(query, (email,))
            student = self.db_connection.cursor.fetchone()
            return student
        except Exception as e:
            print(f"Error fetching student data: {e}")
            return None

    def get_admin(self, username):
        try:
            # Query by username
            sql = "SELECT username, password, role FROM admin WHERE username = %s"
            self.cursor.execute(sql, (username,))
            result = self.cursor.fetchone()

            # Log result for debugging
            print(f"Query result: {result}")
            # btn - success.show

            if result:
                user = {
                    'username': result[0],
                    'password': result[1],
                    'role': result[2],
                }
                return user
            else:
                print(f"No user found with username: {username}")
                return None
        except Exception as e:
            print(f"Error occurred while retrieving user data: {e}")
            return None


    def get_notifications_for_role(self, role, user_id):
        query = """
        SELECT notification_text AS message, notification_date AS created_at
        FROM notification
        WHERE (target_role = %s OR target_role = 'both') 
          AND (student_id = %s OR student_id IS NULL)
        ORDER BY notification_date DESC
        """
        try:
            self.db_connection.cursor.execute(query, (role, user_id))  # Execute query
            notifications = self.db_connection.cursor.fetchall()
            print(f"Fetched Notifications: {notifications}")  # Debug print
            return notifications
        except Exception as e:
            print(f"Error fetching notifications: {e}")
            return []

    def get_user_by_email(self,email):
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                port=3307,
                password='x1sana2axuseen',
                database='online_education'
            )
            cursor = connection.cursor()

            query = "SELECT id, email,name, role,password FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                user = {
                    'id': result[0],
                    'email': result[1],
                    'name': result[2],
                    'role': result[3],
                    'password':result[4]
                }
                return user
            return None

        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None


    def get_user_by_username(self,name):
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                port=3307,
                password='x1sana2axuseen',
                database='online_education'
            )
            cursor = connection.cursor()

            query = "SELECT id, email, name, role FROM users WHERE username = %s"
            cursor.execute(query, (name,))
            result = cursor.fetchone()

            if result:
                user = {
                    'id': result[0],
                    'email': result[1],
                    'name': result[2],
                    'role': result[3]
                }
                return user
            return None

        except Exception as e:
            print(f"Error fetching user by username: {e}")
            return None


def check_user_model_connection():
    try:
        user_configuration = UserDbConfiguration()
        mysql_connect = UserDatabase(
            host=user_configuration.DB_HOSTNAME,
            port=3307,
            user=user_configuration.DB_USERNAME,
            password=user_configuration.DB_PASSWORD,
            database=user_configuration.DB_NAME
        )
        mysql_connect.make_connection()
        user_model = UserModel(mysql_connect)
        return True, user_model
    except Exception as e:
        print(f'Error connecting to database: {e}')
        return False, None