from os import popen
from pydoc_data.topics import topics
from functools import wraps
from click.globals import pop_context

from app import app
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, session, flash, abort

from flask import session
from app.public.public_view import erorpage
from app.user.user_model import UserModel, UserDatabase, check_user_model_connection
from flask import jsonify,abort
from flask_mail import Mail, Message
import os


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'xasaasixasan90@gmail.com'  # Replace with your Gmail address
app.config['MAIL_PASSWORD'] = 'jnxz fosu iici lpjd'  # Replace with your Gmail app password
app.config['MAIL_DEFAULT_SENDER'] = 'xasaasixasan90@gmail.com'  # Replace with your Gmail address


mail = Mail(app)





import pymysql
# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'port': 3307,
    'password': 'x1sana2axuseen',
    'database': 'online_education'
}
import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        port=3307,
        password='x1sana2axuseen',
        database='online_education',
        cursorclass=pymysql.cursors.DictCursor  # Isticmaal DictCursor
    )
def get_user_model():
    # Assume you already have the UserModel class and a database connection.
    db_connection = UserDatabase(host='localhost',port=3307
                                 , user='root', password='x1sana2axuseen', database='online_education')
    db_connection.make_connection()
    return UserModel(db_connection)


@app.route('/')
def home():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('home.html', courses=courses)

@app.route('/login', methods=['GET'])  # This is the route for showing the login page
def getlogin_page():
    return render_template('login.html')


from flask import request, jsonify, make_response, session


@app.route('/getinfo', methods=['POST'])
def getlogin():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        print(f"email and password {email},{password}")
        # Check for missing credentials
        if not email or not password:
            return make_response(jsonify({
                'message': 'Email and password are required',
                'status': 'error',
                'data': {}
            }), 400)

        # Connect to the database
        connection_status, user_model = check_user_model_connection()

        if connection_status:
            # Fetch user from the database
            user = user_model.getting_user_by_email(email)
            print(user)

            if user and user['password'] == password:  # Validate password
                print('sucessfuly user logeed in')
                session['user_id'] = user['id']
                session['email'] = email
                # to print this what i need
                print(f"Session User ID: {session['user_id']}")
                print(f"Session Email: {session['email']}")

                session.permanent = False # Set session to non-permanent (not dependent on browser close)

                if user.get('student_id'):
                    session['student_id'] = user['student_id']
                    print(f'student {session[user]}')
                    session['role'] = 'student'
                elif user.get('admin_id'):
                    session['admin_id'] = user['admin_id']
                    session['role'] = 'admin'
                else:
                    session['role'] = 'user'


                return make_response(jsonify({
                    'message': 'Login successful',
                    'status': 'success',
                    'data': {}
                }), 200)
            else:
                return make_response(jsonify({
                    'message': 'Invalid credentials',
                    'status': 'error',
                    'data': {}
                }), 200)
        else:
            return make_response(jsonify({
                'message': 'Database connection error',
                'status': 'error',
                'data': {}
            }), 500)

    except Exception as e:
        return make_response(jsonify({
            'message': f'Error: {str(e)}',
            'status': 'error',
            'data': {}
        }), 500)


@app.route('/design', methods=['POST'])
def register_open():
    if request.method == 'POST':
        info = request.get_json()  # Get JSON data
        print(info)
        # Validation: Check if all required fields are present
        if (info.get('email') and info.get('name')) and info.get('pass1') and info.get('confirmPassword') and \
                info.get('name2') and info.get('name3') and info.get('gender') and info.get('educationSelect'):

            # Check if the password and confirm password match
            if info.get('pass1') != info.get('confirmPassword'):
                my_response = {
                    'message': 'Passwords do not match.',
                    'status': 'error',
                    'info': {}
                }
                return make_response(jsonify(my_response), 200)

            # Connect to the database
            print('Connecting to the user database...')
            connection_status, user_model = check_user_model_connection()  # Check DB connection

            if connection_status:
                print('You are connected to the user database successfully!')

                # Register the user
                flag, result = user_model.register_user(
                    info.get('email'),  # Extract email directly
                    info.get('pass1'),  # Extract password directly
                    info.get('name'),  # Use full_name directly
                    info.get('name2'),  # Extract mother_name directly
                    info.get('name3'),  # Extract father_name directly
                    info.get('gender'),  # Extract gender directly
                    info.get('educationSelect')
                )

                if flag:
                    print("xogta si saxan baa salxoogeedka loogu xiray")
                    my_response = {
                        'message': 'xogta si saxan baa salxoogeedka loogu xiray',
                        'status': 'success',
                        'info': {}
                    }
                    return make_response(jsonify(my_response), 200)
                else:
                    print("qalad baa dhacay xogta lama xarayn")
                    my_response = {
                        'message': 'qalad baa dhacay xogta lama xarayn',
                        'status': 'error',
                        'info': {}
                    }
                    return make_response(jsonify(my_response), 200)

            else:
                print("qalad baa dhacay kuma xirmi karno salxogeedka")
                my_response = {
                    'message': 'qalad baa dhacay kuma xirmi karno salxogeedka',
                    'status': 'error',
                    'info': {}
                }
                return make_response(jsonify(my_response), 200)

        else:
            print("si sax ah iskuma diiwangelinin kulaabo fadlan!")
            my_response = {
                'message': 'diiwangelinta madhameestirno',
                'status': 'error',
                'info': {}
            }
            return make_response(jsonify(my_response), 200)


@app.route('/admin/login', methods=['GET'])
def login_page():

    return render_template('admin/admin_login.html')


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'xasaasixasan90@gmail.com'
app.config['MAIL_PASSWORD'] = ''  # Use app password if 2FA is enabled
app.config['MAIL_DEFAULT_SENDER'] = 'xasaasixasan90@gmail.com'

mail = Mail(app)



@app.route('/submit_form', methods=['POST'])
def submit_form():


    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if not all([name, email, subject, message]):
        return jsonify({'status': 'error', 'message': 'Fadlan buuxi dhammaan meelaha banaan.'})

    # Send email
    msg = Message(subject=f"Fariin cusub: {subject}",
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=['xasaasixasan90@gmail.com'])  # Replace with your email
    msg.body = f"Magaca: {name}\nEmailka: {email}\n\n{message}"

    try:
        mail.send(msg)
        return jsonify({'status': 'success', 'message': 'Fariintaada waa la diray. Mahadsanid!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'})

@app.route('/admin/login', methods=['POST'])
def login():
    try:
        # Get JSON data from the request
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        db_connection = UserDatabase(host='localhost', port=3307, user='root', password='x1sana2axuseen',
                                     database='online_education')
        db_connection.make_connection()
        user_model = UserModel(db_connection)

        # Fetch user from the database by username
        user = user_model.get_admin(username)
        print(user)
        # Validate username and password
        if user and user['password'] == password:  # Check if password matches
            session['username'] = user['username']
            # Store the correct username in session
            print(user['username'])
            session['role'] = user['role']
            print(user['role'])
            session.permanent = False
            return jsonify({'success': True, 'redirect': '/admin/dashboard'})

        else:

            print("unknow eror")
            return jsonify({"success": False})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


@app.route('/admin/student')
def admin_student():
    logged_in = 'user_id' in session
    if 'username' not in session:


        return redirect(url_for('login'))
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT  student_id, first_name, last_name, status FROM student")
    students = cursor.fetchall()
    print(students)
    cursor.close()
    connection.close()
    return render_template('admin/student.html', students=students,logged_in=logged_in)


@app.route('/admin/course')
def admin_course():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('admin/course.html', courses=courses)
@app.route('/admin/result_portal')
def result_portal():
    cursor.execute("SELECT student_id, CONCAT(first_name, ' ', last_name, ' ',email ) AS name FROM student")
    students = cursor.fetchall()


    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()

    return render_template('admin/result_portal.html', students=students, courses=courses)

# Route to get all courses
@app.route('/api/get-courses', methods=['GET'])
def get_courses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT course_id, course_name FROM course"  # Adjust the query as needed
        cursor.execute(query)
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(courses)  # Return the list of courses as JSON
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to get courses by student ID
@app.route('/api/get-courses-by-student/<int:student_id>', methods=['GET'])
def get_courses_by_student(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT c.course_id, c.course_name
            FROM course c
            JOIN student_course sc ON c.course_id = sc.course_id
            WHERE sc.student_id = %s
        """
        cursor.execute(query, (student_id,))
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(courses)  # Return the list of courses as JSON
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/create_event', methods=['POST'])
def create_event():
    try:
        # Ensure the request has JSON data
        if not request.is_json:
            return jsonify({"success": False, "message": "Request must be JSON"}), 415

        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        date = data.get('date')
        created_by = data.get('created_by', 1)  # Default to admin ID 1 if not provided

        # Validate required fields
        if not title or not description or not date:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Connect to the database using pymysql
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Insert event into the database
        query = """
        INSERT INTO events (title, description, date, created_by)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (title, description, date, created_by))
        connection.commit()

        # Close the database connection
        cursor.close()
        connection.close()

        return jsonify({"success": True}), 200

    except Exception as e:
        print(f"Error creating event: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500






@app.route('/admin/notification')
def admin_notification():
    return render_template('admin/notification.html')



db = pymysql.connect(host='localhost', user='root',port=3307, password='x1sana2axuseen', database='online_education')
cursor = db.cursor()
@app.route('/add_marks', methods=['POST'])
def add_marks():
    student_id = request.form['student']
    course_id = request.form['course']
    marks = int(request.form['marks'])

    cursor.execute("INSERT INTO marks (student_id, course_id, marks) VALUES (%s, %s, %s)",
                   (student_id, course_id, marks))
    db.commit()
    return redirect(url_for('index'))


@app.route('/calculate')
def calculate():
    connection_status, user_model = check_user_model_connection()





    cursor.execute(
        "SELECT students.name, AVG(marks.marks) as avg_marks FROM marks JOIN students ON marks.student_id = students.id GROUP BY student_id ORDER BY avg_marks DESC")
    results = cursor.fetchall()

    rankings = []
    position = 1
    for row in results:
        rankings.append({'name': row[0], 'average': row[1], 'position': position})
        position += 1

    return render_template('user/student_exam.html', rankings=rankings,)


@app.route('/create_notification', methods=['POST'])
def create_notification():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Retrieve form data (e.g., notification text, target role)
    notification_text = request.form['notification_text']
    print(notification_text)
    target_role = request.form['target_role']  # 'student', 'teacher', or 'both'
    student_id = request.form.get('student_id')  # Optional, if targeting a student
    admin_id = request.form.get('admin_id')  # Optional, if targeting a teacher

    # Validate target_role
    if target_role not in ['student', 'teacher', 'both']:
        return "Invalid target role selected. Please choose 'student', 'teacher', or 'both'."

    # Get the database connection
    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    # Insert the new notification into the database
    try:
        cursor.execute("""
            INSERT INTO notification (notification_text, target_role, student_id, admin_id, notification_date) 
            VALUES (%s, %s, %s, %s, NOW())
        """, (notification_text, target_role, student_id, admin_id))

        # Commit the transaction
        db_connection.commit()

        # Redirect to the notifications page
        return redirect(url_for('admin_notification'))

    except Exception as e:
        db_connection.rollback()  # Rollback if there's any error
        print(f"Error occurred: {e}")
        return "An error occurred while creating the notification."

    finally:
        # Close the cursor and connection
        cursor.close()
        db_connection.close()


@app.route('/admin/payment', methods=['GET', 'POST'])
def admin_payment():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        if request.method == 'POST':
            # Handle POST request (payment submission)
            register_id = request.form['register_id']
            course_id = request.form['course_id']
            amount_paid = request.form['amount_paid']
            payment_status = request.form['payment_status']

            # Insert payment into the database
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO payment (register_id, course_id, amount_paid, payment_status, payment_date)
                VALUES (%s, %s, %s, %s, NOW())
            """, (register_id, course_id, amount_paid, payment_status))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('admin_payment'))

        else:
            # Fetch data for GET request
            connection = get_db_connection()
            cursor = connection.cursor()

            # Fetch students
            cursor.execute("SELECT id, name FROM registration")
            students = cursor.fetchall()

            # Fetch courses
            cursor.execute("SELECT course_id, course_name, course_price FROM course")
            courses = cursor.fetchall()

            # Fetch payments
            cursor.execute("""
                SELECT 
                    p.payment_id,  
                    p.register_id, 
                    p.course_id, 
                    p.amount_paid, 
                    p.payment_status, 
                    r.name AS student_name, 
                    c.course_name AS course_name, 
                    p.payment_date
                FROM payment p
                JOIN registration r ON p.register_id = r.id
                JOIN course c ON p.course_id = c.course_id
            """)
            payments = cursor.fetchall()

            cursor.close()
            connection.close()

            # # Debug: Print data to console
            # print(f"Students: {students}")
            # print(f"Courses: {courses}")
            # print(f"Payments: {payments}")

            return render_template('admin/payment.html', students=students, courses=courses, payments=payments)

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred. Please try again later."


# Route for displaying the admin dashboard
@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch total students
            cursor.execute("SELECT COUNT(*) AS total_students FROM student")
            total_students = cursor.fetchone()['total_students']

            # Fetch new students (for the current month)
            cursor.execute(
                "SELECT COUNT(*) AS new_students FROM student WHERE MONTH(created_at) = MONTH(NOW()) AND YEAR(created_at) = YEAR(NOW())")
            new_students = cursor.fetchone()['new_students']

            # Fetch total courses
            cursor.execute("SELECT COUNT(*) AS total_courses FROM course")
            total_courses = cursor.fetchone()['total_courses']

            # Fetch total fees collected
            cursor.execute("SELECT SUM(amount_paid) AS total_fees FROM payment")
            total_fees = cursor.fetchone()['total_fees'] or 0  # Handle NULL values

            # Fetch top 10 courses by sales
            cursor.execute("""
                SELECT p.course_id, COUNT(*) AS sales, c.course_name
                FROM payment p
                JOIN course c ON p.course_id = c.course_id
                GROUP BY p.course_id
                ORDER BY sales DESC
                LIMIT 10
            """)
            top_courses = cursor.fetchall()

            # Fetch monthly sales data for the line chart
            cursor.execute("""
                SELECT DATE_FORMAT(payment_date, '%Y-%m') AS month, SUM(amount_paid) AS total_sales
                FROM payment
                GROUP BY month
                ORDER BY month
            """)
            monthly_sales = cursor.fetchall()

            # Fetch sales by course for the doughnut chart
            cursor.execute("""
                SELECT p.course_id, SUM(p.amount_paid) AS total_sales, c.course_name
                FROM payment p
                JOIN course c ON p.course_id = c.course_id
                GROUP BY p.course_id
            """)
            course_sales = cursor.fetchall()

    finally:
        connection.close()

    # Prepare data for the charts
    line_chart_labels = [sale['month'] for sale in monthly_sales]
    line_chart_data = [sale['total_sales'] for sale in monthly_sales]

    doughnut_chart_labels = [course['course_name'] for course in course_sales]
    doughnut_chart_data = [course['total_sales'] for course in course_sales]

    # Pass data to the template
    return render_template('/admin/admin_dashbaord.html',  # Corrected template name
                          total_students=total_students,
                          new_students=new_students,
                          total_courses=total_courses,
                          total_fees=total_fees,
                          top_courses=top_courses,
                          line_chart_labels=line_chart_labels,
                          line_chart_data=line_chart_data,
                          doughnut_chart_labels=doughnut_chart_labels,
                          doughnut_chart_data=doughnut_chart_data)



@app.route('/get-session-role')
def get_session_role():
    role = session.get('role', None)
    return jsonify({"role": role})


@app.route('/user/logout-on-close', methods=['POST'])
def Stdlogout():
    if 'user_id' in session:
        print(f"Logging out User ID: {session.get('user_id')}")
        session.pop('user_id', None)  # Remove only user ID
        session.pop('role', None)  # Remove role if it exists
    return '', 204  # No content response


@app.route('/logout-on-close', methods=['POST'])
def logout():
    if 'user_id' in session:
        print(f"Logging out User ID: {session.get('user_id')}")
        session.pop('user_id', None)  # Remove only user ID
        session.pop('role', None)  # Remove role if it exists
    return '', 204  # No content response




def update_user_status_to_inactive(email):
    connection = get_db_connection()
    cursor = connection.cursor()
    # cursor.execute('UPDATE users SET status = %s WHERE email = %s', ('inactive', email))
    connection.commit()
    cursor.close()
    connection.close()


# @app.route('/StudentLogout', methods=['GET', 'POST'])
# def Stdlogout():
#     if 'email' in session:
#         email = session['email']
#         print(email)
#
#         if 'student_id' in session:
#             connection = get_db_connection()
#             cursor = connection.cursor()
#             cursor.execute('UPDATE student SET status = %s WHERE email = %s', ('inactive', email))
#             connection.commit()
#             cursor.close()
#             connection.close()
#
#         session.clear()  # Clear session
#         response = redirect(url_for('getlogin_page'))
#         response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"  # Prevent caching
#         response.headers["Pragma"] = "no-cache"
#         response.headers["Expires"] = "0"
#
#         print("Logout request received.")
#         return response
#
#     return render_template('index.html')


import pymysql.cursors


# Assuming you're using pymysql to connect
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        port=3307,
        password="x1sana2axuseen",
        database="online_education",
        cursorclass=pymysql.cursors.DictCursor  # Use DictCursor to return rows as dictionaries
    )


@app.route('/user/user_dashboard')
def open_user_dashboard():
    if 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('getlogin_page'))

    email = session.get('email')
    user_info = {}
    connection_status, user_model = check_user_model_connection()

    if connection_status and email:
        user_info = user_model.getting_user_by_email(email)
        if not user_info:
            flash('User information could not be found.', 'danger')
            return redirect(url_for('getlogin_page'))

        if 'student_id' not in session:
            flash('You are not registered as a student.', 'info')
            return render_template('/user/userdashboard.html', user_info=user_info)

    student_id = session['student_id']
    print(f"wax waali ah socdo {student_id}")
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.course_id, c.course_name, c.course_description, c.image_url
        FROM student_course sc
        JOIN course c ON sc.course_id = c.course_id
        WHERE sc.student_id = %s;
    """
    cursor.execute(query, (student_id,))
    enrolled_courses = cursor.fetchall()

    courses = [
        {
            'course_id': row['course_id'],
            'course_name': row['course_name'],
            'course_description': row['course_description'],
            'image_url': row['image_url']
        }
        for row in enrolled_courses
    ]

    cursor.close()
    conn.close()

    return render_template('/user/userdashboard.html', user_info=user_info, courses=courses)


def fetch_data(query, params=None):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

@app.route('/student_exam')
def student_exam():
    if 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('getlogin_page'))

    email = session.get('email')
    print(email)
    # Fetch user info from the database
    user_info = {}
    print(f"xogta aan helnay waa xogtaan{user_info}")
    connection_status, user_model = check_user_model_connection()
    if connection_status and email:
        user_info = user_model.getting_user_by_email(email)
        print(f"User Info: {user_info}")
        if not user_info:
            flash('User information could not be found.', 'danger')
            return redirect(url_for('getlogin_page'))

    # Check if the user is a student by querying the student table
    student_info = user_model.get_student_by_email(email)

    if not student_info:
        flash('exam view  are only available for students.', 'info')
        return redirect(url_for('open_user_dashboard'))

    # Get the student ID from the session
    student_id = session['student_id']

    # Fetch courses the student has paid for
    paid_courses = fetch_data(
        "SELECT course.course_id, course.course_name "
        "FROM course "
        "JOIN student_course ON course.course_id = student_course.course_id "
        "WHERE student_course.student_id = %s",
        (student_id,)
    )
    print(paid_courses)

    # Fetch exam results for the student
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch marks for the student
    query = """
        SELECT m.marks, c.course_name, c.course_id
        FROM marks m
        JOIN course c ON m.course_id = c.course_id
        WHERE m.student_id = %s
    """
    cursor.execute(query, (student_id,))
    marks = cursor.fetchall()

    # Calculate average marks
    total_marks = sum(mark['marks'] for mark in marks)
    average_marks = total_marks / len(marks) if marks else 0

    # Calculate grades for each course
    for mark in marks:
        mark['grade'] = calculate_grade(mark['marks'])

    # Calculate position for each course
    for mark in marks:
        position_query = """
            SELECT COUNT(*) + 1 AS position
            FROM marks
            WHERE course_id = %s AND marks > %s
        """
        cursor.execute(position_query, (mark['course_id'], mark['marks']))
        position = cursor.fetchone()['position']
        mark['position'] = position

    cursor.close()
    conn.close()

    # Render the template with the fetched data
    return render_template(
        'user/student_exam.html',
        paid_courses=paid_courses,
        marks=marks,
        average_marks=average_marks,
        user_info=user_info
    )

# Helper function to calculate grade
def calculate_grade(marks):
    if marks >= 90:
        return 'A'
    elif marks >= 80:
        return 'B'
    elif marks >= 70:
        return 'C'
    elif marks >= 60:
        return 'D'
    else:
        return 'F'

@app.route('/course/<int:course_id>')
def course_detail1(course_id):
    if 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('getlogin_page'))

    email = session.get('email')
    user_info = {}
    connection_status, user_model = check_user_model_connection()

    if connection_status and email:
        user_info = user_model.getting_user_by_email(email)
        print(f"user info{user_info}")
        if not user_info:
            flash('User information could not be found.', 'danger')
            return redirect(url_for('getlogin_page'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch course details
        cursor.execute("SELECT * FROM course WHERE course_id = %s", (course_id,))
        course = cursor.fetchone()

        if not course:
            return "Course not found", 404

        # Fetch chapters
        cursor.execute("""
            SELECT c.* FROM chapters c
            JOIN course_chapters cc ON c.id = cc.chapter_id
            WHERE cc.course_id = %s
            ORDER BY c.id
        """, (course_id,))
        chapters = cursor.fetchall()

        chapters_list = []
        for chapter in chapters:
            cursor.execute("""
                SELECT t.*, v.video_url
                FROM topics t
                LEFT JOIN videos v ON t.id = v.topic_id
                WHERE t.chapter_id = %s
                ORDER BY t.id
            """, (chapter['id'],))

            topics = cursor.fetchall()
            print(topics)
            chapter['topics'] = topics
            chapters_list.append(chapter)

        # Calculate progress if the user is a student
        progress = None
        overall_progress = 0
        if 'student_id' in session:
            student_id = session['student_id']
            cursor.execute("""
                SELECT COUNT(*) as total_topics,
                       SUM(CASE WHEN p.is_completed = 1 THEN 1 ELSE 0 END) as completed_topics
                FROM topics t
                LEFT JOIN progress p ON t.id = p.topic_id AND p.student_id = %s
                WHERE t.course_id = %s
            """, (student_id, course_id))
            progress = cursor.fetchone()
            overall_progress = (progress['completed_topics'] / progress['total_topics']) * 100 if progress['total_topics'] > 0 else 0

    finally:
        cursor.close()
        conn.close()

    return render_template('user/course_detail.html',
                           course=course,
                           progress=progress,
                           chapters=chapters_list,
                           user_info=user_info,
                           overall_progress=overall_progress)

@app.route('/TeacherLogin', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        print(f"Login attempt with username: {username}")

        # Initialize UserModel
        user_model = get_user_model()

        # Try fetching the user by username
        user = None
        if username:
            user = user_model.get_user_by_username(username)
            print(f"Fetched user: {user}")

        # Double-check fallback (you had this twice unnecessarily)
        if not user and username:
            print("Trying fallback username lookup...")
            user = user_model.get_user_by_username(username)
            print(f"Fallback user fetch result: {user}")

        if user:
            session['user_id'] = user.get('id')
            session['role'] = user.get('role')
            session['name'] = user.get('name')

            print(f"User ID: {session['user_id']}")
            print(f"User role: {session['role']}")
            print(f"User name: {session['name']}")

            if user['role'] == 'teacher':
                print("Redirecting to teacher dashboard...")
                return redirect(url_for('teacher_dashboard'))
            else:
                print(f"User is not a teacher. Role is: {user['role']}")
                flash('You are not authorized as a teacher.', 'danger')
                return redirect(url_for('teacher_login'))
        else:
            print("No user found with that username.")
            flash('Invalid email or username. Please try again.', 'danger')
            return redirect(url_for('teacher_login'))

    return render_template('teacher/teacher_login.html')


@app.route('/dashboard/teacher')
def teacher_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('teacher_login'))  # Redirect to login if not logged in

    user_id = session['user_id']  # Get the logged-in teacher's ID
    user_model = get_user_model()  # Get user model instance
    notifications = user_model.get_notifications_for_role('teacher', user_id)  # Fetch notifications for the teacher
    return render_template('teacher/teacher_dash.html', notifications=notifications)

@app.route('/logoutTeacher', methods=['POST', 'GET'])
def Teacherlogout():
    session.clear()  # Clear all session data
    return redirect(url_for('teacher_login'))


@app.route('/dashboard/teacher/notifications')
def teacher_notifications():
    user_id = session['user_id']  # Get the logged-in teacher's ID
    success, user_model = check_user_model_connection()  # Establish DB connection
    if not success:
        return "Error connecting to the database"

    # Fetch notifications for the teacher
    notifications = user_model.get_notifications_for_role('teacher', user_id)

    # print(notifications)  # Print to check the structure of notifications

    # Return the rendered template with notifications
    return render_template('teacher/T_Notif.html', notifications=notifications, role='Teacher')


@app.route('/send_email')
def test_route():
    return "This is a test route"

@app.route('/create_event_', methods=['GET', 'POST'])
def create_event_():
    if 'username' not in session:
        return redirect('/admin/login')  # Redirect to login if not authenticated

    # Retrieve the user role from the session
    user_role = session.get('role')

    # Get the date parameter from the URL
    date = request.args.get('date')


    return render_template('admin/event.html', date=date, user_role=user_role)

# Mock user roles (replace with your authentication logic)
USER_ROLES = {
    "admin": "admin",
    "student": "student"
}

# # Decorator to restrict access to admins
# def admin_only(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#
#         role=session.get('role')
#         # Get user role from session
#         print(role)
#         if role != role["admin"]:
#             abort(403)  # Forbidden
#         return f(*args, **kwargs)
#     return decorated_function
@app.route('/user/events')
def get_events():
    if 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('getlogin_page'))

    email = session.get('email')

    # Fetch user info from the database
    user_info = {}
    connection_status, user_model = check_user_model_connection()
    if connection_status and email:
        user_info = user_model.getting_user_by_email(email)
        print(f"User Info: {user_info}")
        if not user_info:
            flash('User information could not be found.', 'danger')
            return redirect(url_for('getlogin_page'))

    # Check if the user is a student by querying the student table
    student_info = user_model.get_student_by_email(email)

    if not student_info:
        flash('events  are only available for students.', 'info')
        return redirect(url_for('open_user_dashboard'))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM events ORDER BY date ASC"
            cursor.execute(sql)
            events = cursor.fetchall()  # Fetch all events as a list of dictionaries
    finally:
        connection.close()

    return render_template('user/student_event.html', events=events,user_info=user_info)
@app.route('/user/notifications')
def user_notifications():
    # Check if the user is logged in
    if 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('getlogin_page'))

    email = session.get('email')

    # Fetch user info from the database
    user_info = {}
    connection_status, user_model = check_user_model_connection()
    if connection_status and email:
        user_info = user_model.getting_user_by_email(email)
        print(f"User Info: {user_info}")
        if not user_info:
            flash('User information could not be found.', 'danger')
            return redirect(url_for('getlogin_page'))

    # Check if the user is a student by querying the student table
    student_info = user_model.get_student_by_email(email)

    if not student_info:
        flash('Notifications are only available for students.', 'info')
        return redirect(url_for('open_user_dashboard'))

    # Assuming student_info is a tuple and the id is the first element
    student_id = student_info[0]  # Access the first element of the tuple

    # Fetch notifications for the student
    notifications = user_model.get_notifications_for_role('student', student_id)

    print(f"Notifications: {notifications}")

    return render_template('user/s_Notif.html', notifications=notifications, role='User', user_info=user_info)


# @app.route('/api/add-topic', methods=['POST'])
# def add_topic():
#     try:
#         # Get data from the request
#         data = request.get_json()
#         course_id = data.get('course_id')
#         chapter_name = data.get('chapter_name')
#         topic_name = data.get('topic_name')
#         video_url = data.get('video_url')
#
#         # Print received data for debugging
#         print("Received data:")
#         print(f"course_id: {course_id}")
#         print(f"chapter_name: {chapter_name}")
#         print(f"topic_name: {topic_name}")
#         print(f"video_url: {video_url}")
#
#         # Validate the data
#         if not course_id or not chapter_name or not topic_name or not video_url:
#             print("Validation failed: All fields are required")
#             return jsonify({'success': False, 'message': 'All fields are required'}), 400
#
#         # Connect to the database
#         conn = get_db_connection()
#         cursor = conn.cursor()
#
#         # Step 1: Fetch chapter_id based on chapter_name
#         print("Fetching chapter_id for chapter_name:", chapter_name)
#         cursor.execute("SELECT id FROM chapters WHERE name = %s", (chapter_name,))
#         chapter = cursor.fetchone()
#         if not chapter:
#             print("Chapter not found:", chapter_name)
#             cursor.close()
#             conn.close()
#             return jsonify({'success': False, 'message': 'Chapter not found'}), 404
#         chapter_id = chapter[0]
#         print("Fetched chapter_id:", chapter_id)
#
#         # Step 2: Insert into topics table
#         print("Inserting into topics table:")
#         print(f"course_id: {course_id}, chapter_id: {chapter_id}, name: {topic_name}, chapter_name: {chapter_name}")
#         cursor.execute(
#             "INSERT INTO topics (course_id, chapter_id, name, chapter_name) VALUES (%s, %s, %s, %s)",
#             (course_id, chapter_id, topic_name, chapter_name)
#         )
#         topic_id = cursor.lastrowid  # Get the auto-generated topic_id
#         print("Inserted topic_id:", topic_id)
#
#         # Step 3: Insert into videos table
#         print("Inserting into videos table:")
#         print(f"topic_id: {topic_id}, video_url: {video_url}")
#         cursor.execute(
#             "INSERT INTO videos (topic_id, video_url) VALUES (%s, %s)",
#             (topic_id, video_url)
#         )
#         print("Inserted video successfully")
#
#         # Commit the transaction
#         conn.commit()
#         cursor.close()
#         conn.close()
#
#         print("Topic and video added successfully")
#         return jsonify({'success': True, 'message': 'Topic added successfully'})
#     except Exception as e:
#         print(f"Error adding topic: {str(e)}")  # Log the error
#         return jsonify({'success': False, 'message': str(e)}), 500
from flask import render_template
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'port': 3307,
    'password': 'x1sana2axuseen',
    'db': 'course_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)


@app.route('/api/add-course', methods=['POST'])
def add_course():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    img_url = data.get('img_url')

    if not name or not description or not img_url:
        return jsonify({'success': False, 'message': 'All fields are required!'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = 'INSERT INTO chapters (name, lesson_count) VALUES (%s, %s)'
        cursor.execute(sql, (name, 0))  # Default lesson_count is 0
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Course added successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/add-topic', methods=['POST'])
def add_topic():
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        chapter_name = data.get('chapter_name')
        topic_name = data.get('topic_name')
        video_url = data.get('video_url')

        # Validate input data
        if not course_id or not chapter_name or not topic_name or not video_url:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch or create chapter_id
        cursor.execute("SELECT id FROM chapters WHERE name = %s AND course_id = %s", (chapter_name, course_id))
        chapter = cursor.fetchone()

        if not chapter:
            # If the chapter doesn't exist, create it
            cursor.execute("INSERT INTO chapters (name, course_id, lesson_count) VALUES (%s, %s, %s)",
                           (chapter_name, course_id, 0))
            conn.commit()
            chapter_id = cursor.lastrowid  # Get the ID of the newly created chapter
        else:
            chapter_id = chapter['id']

        # Insert the topic
        cursor.execute("INSERT INTO topics (chapter_id, name, course_id, chapter_name) VALUES (%s, %s, %s, %s)",
                       (chapter_id, topic_name, course_id, chapter_name))
        conn.commit()

        # Get the ID of the newly inserted topic
        topic_id = cursor.lastrowid

        # Insert the video URL
        cursor.execute("INSERT INTO videos (topic_id, video_url) VALUES (%s, %s)",
                       (topic_id, video_url))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Topic added successfully'})
    except Exception as e:
        print(f"Error adding topic: {e}")  # Log the error for debugging
        return jsonify({'success': False, 'message': str(e)}), 500
@app.route('/api/get-topics/<int:course_id>', methods=['GET'])
def get_topics(course_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Failed to connect to the database'}), 500

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT t.name AS topic_name, v.video_url
                FROM topics t
                JOIN videos v ON t.id = v.topic_id
                WHERE t.course_id = %s
            """, (course_id,))
            topics = cursor.fetchall()
        conn.close()
        return jsonify(topics)
    except Exception as e:
        print(f"Error fetching topics: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
@app.route('/user/my_courses')
def my_courses():
    if 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('getlogin_page'))

    email = session.get('email')

    # Fetch user info from the database
    user_info = {}
    connection_status, user_model = check_user_model_connection()
    if connection_status and email:
        user_info = user_model.getting_user_by_email(email)
        print(f"User Info: {user_info}")
        if not user_info:
            flash('User information could not be found.', 'danger')
            return redirect(url_for('getlogin_page'))

    # Check if the user is a student by querying the student table
    student_info = user_model.get_student_by_email(email)

    if not student_info:
        flash('order course are only available for students.', 'info')
        return redirect(url_for('open_user_dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch enrolled courses if the user is a student
        courses = []
        if 'student_id' in session:
            student_id = session['student_id']
            query = """
                SELECT c.course_id, c.course_name, c.course_description, c.image_url
                FROM student_course sc
                JOIN course c ON sc.course_id = c.course_id
                WHERE sc.student_id = %s;
            """
            cursor.execute(query, (student_id,))
            enrolled_courses = cursor.fetchall()

            # Convert tuple results to dictionaries
            courses = [
                {
                    'course_id': row['course_id'],
                    'course_name': row['course_name'],
                    'course_description': row['course_description'],
                    'image_url': row['image_url']
                }
                for row in enrolled_courses
            ]
        else:
           print("no ednroledcourse")

    finally:
        cursor.close()
        conn.close()

    return render_template('user/my_courses.html', courses=courses, user_info=user_info)


# @app.route('/my_courses')
# def my_courses():
#     email = session.get('email')
#     user_info = {}
#     # Get student ID from session (replace with your session logic)
#     student_id = session.get('student_id')
#     if not student_id:
#         return redirect('/login')  # Redirect to login if student is not logged in
#
#     # Connect to the database
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     # Query to fetch enrolled courses for the student
#     query = """
#         SELECT c.course_id, c.course_name, c.course_description, c.image_url
#         FROM student_course sc
#         JOIN course c ON sc.course_id = c.course_id
#         WHERE sc.student_id = %s;
#     """
#     cursor.execute(query, (student_id,))
#     enrolled_courses = cursor.fetchall()  # Fetch all enrolled courses
#
#     # Close the database connection
#     cursor.close()
#     conn.close()
#
#     # Convert the result to a list of dictionaries for easier access in the template
#     courses = [
#         {
#             'course_id': row[0],
#             'course_name': row[1],
#             'course_description': row[2],
#             'image_url': row[3]
#         }
#         for row in enrolled_courses
#     ]
#
#     # Render the my_courses template with the enrolled courses data
#     return render_template('user/my_courses.html', courses=courses,user_info=user_info)

def row_to_dict(cursor, row):
    return {column[0]: value for column, value in zip(cursor.description, row)}


@app.route('/video')
def video_page():
    if 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('getlogin_page'))

    email = session.get('email')
    print(f'email was getting as session{email}')
    user_info = {}
    connection_status, user_model = check_user_model_connection()

    if connection_status and email:
        user_info = user_model.getting_user_by_email(email)
        print(f"user_info{user_info}")
        if not user_info:
            flash('User information could not be found.', 'danger')
            return redirect(url_for('getlogin_page'))
        if 'student_id' not in session:
            flash('You are not registered as a student.', 'info')
            return render_template('user/userdashboard.html', user_info=user_info)

    video_url = request.args.get('video_url', '')
    print(f"user {video_url}")
    if not video_url:
        flash("Invalid video URL!", "danger")
        return redirect(url_for('my_courses'))

    return render_template('user/video.html', video_url=video_url,user_info=user_info)





@app.route('/user/student_assignment')
def student_assignment():
    if 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('getlogin_page'))

    email = session.get('email')

    # Fetch user info from the database
    user_info = {}
    connection_status, user_model = check_user_model_connection()
    if connection_status and email:
        user_info = user_model.getting_user_by_email(email)
        print(f"User Info: {user_info}")
        if not user_info:
            flash('User information could not be found.', 'danger')
            return redirect(url_for('getlogin_page'))

    # Check if the user is a student by querying the student table
    student_info = user_model.get_student_by_email(email)

    if not student_info:
        flash('assignment are only available for students.', 'info')
        return redirect(url_for('open_user_dashboard'))

        student_id = session['student_id']

    # Fetch user info from the database
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_info = cursor.fetchone()
            print(f'email{user_info}')
    finally:
        connection.close()

    if not user_info:
        flash('User information could not be found.', 'danger')
        return redirect(url_for('getlogin_page'))

    # Fetch assignments from the database
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT assignments.*, course.course_name 
                            FROM assignments 
                            JOIN course ON assignments.course_id = course.course_id
                        """)
            assignments = cursor.fetchall()
    finally:
        connection.close()

    # Pass both user_info and assignments to the template
    return render_template('user/assignment.html', user_info=user_info, assignments=assignments)
# Route to view a specific assignment
@app.route('/user/view_assignment/<int:assignment_id>')
def view_assignment(assignment_id):
    if 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('getlogin_page'))

    email = session.get('email')
    user_info = {}
    connection_status, user_model = check_user_model_connection()

    if connection_status and email:
        user_info = user_model.getting_user_by_email(email)
        if not user_info:
            flash('User information could not be found.', 'danger')
            return redirect(url_for('getlogin_page'))

        if 'student_id' not in session:
            flash('You are not registered as a student.', 'info')
            return render_template('/user/userdashboard.html', user_info=user_info)

    # Fetch the assignment from the database
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:  # Use DictCursor here
            cursor.execute("""
                SELECT a.*, c.course_name 
                FROM assignments a
                LEFT JOIN course c ON a.course_id = c.course_id
                WHERE a.id = %s
            """, (assignment_id,))
            assignment = cursor.fetchone()
            print(f"assignment {assignment}")
            # Check for submission
            cursor.execute("""
                SELECT * FROM submissions 
                WHERE assignment_id = %s AND student_id = %s
            """, (assignment_id, session['student_id']))
            submission = cursor.fetchone()

    finally:
        connection.close()

    if not assignment:
        flash('Assignment not found.', 'danger')
        return redirect(url_for('student_assignment'))

    # Convert date objects to strings if needed
    if assignment and 'due_date' in assignment and assignment['due_date']:
        assignment['due_date_str'] = assignment['due_date'].strftime('%B %d, %Y')

    if submission and 'submitted_at' in submission:
        submission['submitted_at_str'] = submission['submitted_at'].strftime('%B %d, %Y at %I:%M %p')

    return render_template(
        'user/view_assignment.html',
        assignment=assignment,
        user_info=user_info,
        submission=submission,
        submission_exists=submission is not None
    )


@app.route('/submit_assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    if 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('getlogin_page'))

    email = session.get('email')
    user_info = {}
    connection_status, user_model = check_user_model_connection()

    if connection_status and email:
        user_info = user_model.getting_user_by_email(email)
        if not user_info:
            flash('User information could not be found.', 'danger')
            return redirect(url_for('getlogin_page'))

        if 'student_id' not in session:
            flash('You are not registered as a student.', 'info')
            return render_template('/user/userdashboard.html', user_info=user_info)

    # Get Student ID
    cursor.execute("SELECT student_id, first_name FROM student WHERE email = %s", (email,))
    student = cursor.fetchone()
    print(f'STUDENT is {student}')
    if not student:
        flash('You are not registered as a student.', 'danger')
        return redirect(url_for('getlogin_page'))

    student_id, student_name = student

    # Check if assignment exists

    cursor.execute("SELECT title FROM assignments WHERE id = %s", (assignment_id,))
    assignment = cursor.fetchone()
    print(f"the assignments is {assignment}")
    if not assignment:
        flash('Assignment not found.', 'danger')
        return redirect(url_for('student_dashboard'))

    assignment_name = assignment[0]

    # Check if already submitted
    cursor.execute("SELECT * FROM submissions WHERE student_id = %s AND assignment_id = %s",
                  (student_id, assignment_id))
    existing_submission = cursor.fetchone()
    print(f"already sent this assignment {existing_submission}")
    if existing_submission:
        flash("You have already submitted this assignment.", "danger")
        return redirect(url_for('student_dashboard'))

    if request.method == 'POST':
        assignment_link = request.form['assignment_link']
        cursor.execute("SELECT student_id FROM student WHERE email = %s", (email,))
        student = cursor.fetchone()
        print(f"student id {student}")
        if not student:
            flash("You are not registered as a student.", "danger")
            return redirect(url_for('student_dashboard'))

        student_id = student[0]
        # Save to database
        cursor.execute(
            "INSERT INTO submissions (student_id, assignment_id, assignment_link) VALUES (%s, %s, %s)",
            (student_id, assignment_id, assignment_link)
        )
        print(f"the submission successfully ")
        db.commit()

        try:
            # Send email notification - only on successful submission
            msg = Message("New Assignment Submission",
                         sender="xasaasixasan90@gmail.com",
                         recipients=["xasaasixasan90@gmail.com"])
            msg.body = f"Student: {student_name}\nEmail: {email}\nAssignment: {assignment_name}\nLink: {assignment_link}"
            mail.send(msg)
            flash("Assignment submitted successfully! Notification email sent.", "success")
        except Exception as e:
            flash(f"Assignment submitted but email notification failed: {str(e)}", "warning")

        return redirect(url_for('student_dashboard'))

    return render_template('user/submit_assign.html',
                         assignment_id=assignment_id,
                         student_name=student_name,
                         user_info=user_info)




import os
@app.route('/send_assignment', methods=['GET', 'POST'])
def send_assignment():
    if request.method == 'POST':
        course_id = request.form['course_id']
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        file = request.files['file']
            #upload
        uploads_dir = os.path.join(app.static_folder, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)  # Create the directory if it doesn't exist

        # Save the file
        file_path = os.path.join(uploads_dir, file.filename)
        file.save(file_path)

        # Save assignment to the database
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO assignments (course_id, title, description, due_date, file_path) VALUES (%s, %s, %s, %s, %s)",
                    (course_id, title, description, due_date, file_path)
                )
                connection.commit()
            flash('Assignment sent successfully!', 'success')
        finally:
            connection.close()

        return redirect(url_for('send_assignment'))

    # Fetch courses for the dropdown
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT course_id, course_name FROM course")
            courses = cursor.fetchall()
            print(f"mycourses {courses}")
    finally:
        connection.close()

    return render_template('admin/assigment.html', courses=courses)
