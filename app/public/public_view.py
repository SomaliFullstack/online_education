from app import  app
from flask import render_template, request, make_response, jsonify, session

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
@app.errorhandler(404)
def erorpage(e):
    return render_template('eror.html'),404
@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/log_in')
def log_in():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/course-detail.html')
def course_detail():
    course_id = request.args.get('courseId', type=int)
    
    return render_template('course_detail.html',)
    