
#--------------------  Imports  --------------------
import os
import json

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import current_app as app
from flask import make_response

from flask_restful import Resource
from flask_restful import Api
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from flask_sqlalchemy import SQLAlchemy

from werkzeug.exceptions import HTTPException

#--------------------  Initialization  --------------------
db = SQLAlchemy()

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
    
db.init_app(app)
api = Api(app)
app.app_context().push()

#Error code and Message dict format:error_class=(error_code, error_msg)
error_dict = {
"C1e" : ("COURSE001", "Course Name is required and should be string."),
"C2e" :("COURSE002", "Course Code is required and should be string."),
"C3e" : ("COURSE003", "Course Description should be string."),
"S1e" : ("STUDENT001", "Roll Number required and should be String"),
"S2e" : ("STUDENT002", "First Name is required and should be String"),
"S3e" : ("STUDENT003", "Last Name is String"),
"E1e" : ("ENROLLMENT001", "Course does not exist"),
"E2e" : ("ENROLLMENT002", "Student does not exist."),
"E3e" : ("ENROLLMENT003", "Course Code is required and should be string.")
} 
 
#--------------------  DB Model Classes  --------------------
class Student(db.Model):
    __tablename__ =  'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    courses = db.relationship("Course", secondary="enrollment" , back_populates="students")
    
class Course(db.Model):
    __tablename__ =  'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)
    students = db.relationship("Student", secondary="enrollment" , back_populates="courses")
    
class Enrollment(db.Model):
    __tablename__ =  'enrollment'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)
        
#--------------------  Course Error Classes  --------------------
class Success(HTTPException):
    def __init__(self, status_code, error_msg):
        #self.response = make_response(error_msg, status_code)
        self.response = make_response('', status_code, {"Content-Type": "application/json"})
        
class CourseNotFound(HTTPException):
    def __init__(self, status_code, error_msg):
        self.response = make_response('', status_code, {"Content-Type": "application/json"})
        
class CourseCodeExists(HTTPException):
    def __init__(self, status_code, error_msg):
        #self.response = make_response(error_msg, status_code)
        self.response = make_response('', status_code, {"Content-Type": "application/json"})
        
class C1e(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})
		
class C2e(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class C3e(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

#--------------------  Student Error Classes  --------------------
class StudentNotFound(HTTPException):
    def __init__(self, status_code, error_msg):
        #self.response = make_response(error_msg, status_code)
        self.response = make_response('', status_code, {"Content-Type": "application/json"})
        
class StudentRollExists(HTTPException):
    def __init__(self, status_code, error_msg):
        #self.response = make_response(error_msg, status_code)
        self.response = make_response('', status_code, {"Content-Type": "application/json"})
        
class S1e(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})
		
class S2e(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class S3e(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})


#--------------------  Enrollment Error Classes  --------------------	

class StudentNotEnrolled(HTTPException):
    def __init__(self, status_code, error_msg):
        #self.response = make_response(error_msg, status_code)
        self.response = make_response('', status_code, {"Content-Type": "application/json"})
        
class E1e(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})
		
class E2e(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class E3e(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})
		
    
#--------------------  Course API  --------------------
course_op = {
  "course_id": fields.Integer,
  "course_name": fields.String,
  "course_code": fields.String,
  "course_description": fields.String
}

create_course_parser = reqparse.RequestParser()
create_course_parser.add_argument("course_name")
create_course_parser.add_argument("course_code")
create_course_parser.add_argument("course_description")

update_course_parser = reqparse.RequestParser()
update_course_parser.add_argument("course_name")
update_course_parser.add_argument("course_code")
update_course_parser.add_argument("course_description")


class CourseAPI(Resource):
    @marshal_with(course_op)
    def get(self, course_id):
        ID = course_id
        course = Course.query.filter_by(course_id=ID).first()
        if course:
            # course_id is present
            return course, 200
        else:
            raise CourseNotFound(status_code=404, error_msg='Course not found')
        
    @marshal_with(course_op)
    def put(self, course_id):
        ID = course_id
        course = Course.query.filter_by(course_id=ID).first()
        if course:
            # course_id is present
            args = update_course_parser.parse_args()
            name = args.get("course_name", None)
            code = args.get("course_code", None)
            description = args.get("course_description", None)
            
            if (type(name) is str) and (name is not None):
                if (type(code) is str) and (code is not None) :
                    if (description is None)or(type(description) is str):
                        course.course_name = name
                        course.course_code = code
                        if description:
                            course.course_description = description
                        db.session.commit()
                        course = Course.query.filter_by(course_id=ID).first()
                        return course, 200
                    else:
                        raise C3e(status_code=400, error_code=error_dict['C3e'][0], error_msg=error_dict['C3e'][1])
                else:
                    raise C2e(status_code=400, error_code=error_dict['C2e'][0], error_msg=error_dict['C2e'][1])
            else:
                raise C1e(status_code=400, error_code=error_dict['C1e'][0], error_msg=error_dict['C1e'][1])
        else:
            raise CourseNotFound(status_code=404, error_msg='Course not found')
            
    @marshal_with(course_op)          
    def post(self):
        #print(update_course_parser.parse_args())
        #print(create_course_parser.parse_args())
        
        args = create_course_parser.parse_args()
        name = args.get("course_name", None)
        code = args.get("course_code", None)
        description = args.get("course_description", None)
        
        if (type(name) is str) and (name is not None):
            if (type(code) is str) and (code is not None) :
                if (description is None) or (type(description) is str):
                    course = Course.query.filter_by(course_code=code).first()
                    #print(course)
                    if course:
                        # course code already exists
                        raise CourseCodeExists(status_code=409, error_msg='course_code already exist')
                    else:   
                        course = Course(course_name = name, course_code = code, course_description = description )
                        db.session.add(course)
                        db.session.commit()
                        course = Course.query.filter_by(course_code=code).first()
                        return course, 201
                else:
                    raise C3e(status_code=400, error_code=error_dict['C3e'][0], error_msg=error_dict['C3e'][1])
            else:
                raise C2e(status_code=400, error_code=error_dict['C2e'][0], error_msg=error_dict['C2e'][1])
        else:
            raise C1e(status_code=400, error_code=error_dict['C1e'][0], error_msg=error_dict['C1e'][1])
        
        
    def delete(self, course_id):
        ID = course_id
        course = Course.query.filter_by(course_id=ID).first()
        if course:
            # delete all entries of course in enrollment table
            enrolls = Enrollment.query.filter_by(course_id=ID).all()
            if len(enrolls)>0:
                for enroll in enrolls:
                    db.session.delete(enroll)
                db.session.commit()
            
            # course_id is present
            db.session.delete(course)
            db.session.commit()
            raise Success(status_code=200, error_msg='')
        else:
            raise CourseNotFound(status_code=404, error_msg='Course not found')

#--------------------  Student API  --------------------
student_op = {
  "student_id": fields.Integer,
  "first_name": fields.String,
  "last_name": fields.String,
  "roll_number": fields.String
}

create_student_parser = reqparse.RequestParser()
create_student_parser.add_argument("first_name")
create_student_parser.add_argument("last_name")
create_student_parser.add_argument("roll_number")

update_student_parser = reqparse.RequestParser()
update_student_parser.add_argument("first_name")
update_student_parser.add_argument("last_name")
update_student_parser.add_argument("roll_number")
       
class StudentAPI(Resource):
    @marshal_with(student_op)
    def get(self, student_id):
        ID = student_id
        student = Student.query.filter_by(student_id=ID).first()
        #print(student)
        if student:
            # student_id is present
            return student, 200
        else:
            raise StudentNotFound(status_code=404, error_msg='Student not found')
            
    @marshal_with(student_op)
    def put(self, student_id):
        ID = student_id
        student = Student.query.filter_by(student_id=ID).first()
        if student:
            # student_id is present
            args = update_student_parser.parse_args()
            fname = args.get("first_name", None)
            lname = args.get("last_name", None)
            roll = args.get("roll_number", None)
            
            if (type(roll) is str) and (roll is not None):
                if (type(fname) is str) and (fname is not None) :
                    if (lname is None)or(type(lname) is str):
                        student.first_name = fname
                        student.roll_number = roll
                        if lname:
                            student.last_name = lname
                        db.session.commit()
                        student = Student.query.filter_by(student_id=ID).first()
                        return student, 200
                    else:
                        raise S3e(status_code=400, error_code=error_dict['S3e'][0], error_msg=error_dict['S3e'][1])
                else:
                    raise S2e(status_code=400, error_code=error_dict['S2e'][0], error_msg=error_dict['S2e'][1])
            else:
                raise S1e(status_code=400, error_code=error_dict['S1e'][0], error_msg=error_dict['S1e'][1])
        else:
            raise StudentNotFound(status_code=404, error_msg='Course not found')
            
    @marshal_with(student_op)
    def post(self):
        args = create_student_parser.parse_args()
        fname = args.get("first_name", None)
        lname = args.get("last_name", None)
        roll = args.get("roll_number", None)
        
        if (type(roll) is str) and (roll is not None):
            if (type(fname) is str) and (fname is not None) :
                if (lname is None)or(type(lname) is str):
                    student = Student.query.filter_by(roll_number=roll).first()
                    print(student)
                    if student:
                        # student already exists
                        raise StudentRollExists(status_code=409, error_msg='course_code already exist')
                    else:   
                        student = Student(roll_number = roll, first_name = fname, last_name = lname)
                        db.session.add(student)
                        db.session.commit()
                        student = Student.query.filter_by(roll_number=roll).first()
                        return student, 201
                else:
                    raise S3e(status_code=400, error_code=error_dict['S3e'][0], error_msg=error_dict['S3e'][1])
            else:
                raise S2e(status_code=400, error_code=error_dict['S2e'][0], error_msg=error_dict['S2e'][1])
        else:
            raise S1e(status_code=400, error_code=error_dict['S1e'][0], error_msg=error_dict['S1e'][1])
        
    def delete(self, student_id):
        ID = student_id
        student = Student.query.filter_by(student_id=ID).first()
        if student:
            # course_id is present
            db.session.delete(student)
            db.session.commit()
            
            # delete all entries of course in enrollment table
            enrolls = Enrollment.query.filter_by(student_id=ID).all()
            for enroll in enrolls:
                db.session.delete(enroll)
            db.session.commit()
            raise Success(status_code=200, error_msg='')
        else:
            raise StudentNotFound(status_code=404, error_msg='Course not found')

#--------------------  Enrollment API  --------------------
create_student_enroll_parser = reqparse.RequestParser()
create_student_enroll_parser.add_argument("course_id")

       
class EnrollmentAPI(Resource):
    def get(self, student_id):
        ID = student_id
        student = Student.query.filter_by(student_id=ID).first()
        if student:
            enrolls = Enrollment.query.filter_by(student_id=ID).all()
            if len(enrolls)>0:
                data = []
                for i,enroll in enumerate(enrolls):
                    d = {
                        "enrollment_id": enroll.enrollment_id,
                        "student_id": enroll.student_id,
                        "course_id": enroll.course_id
                        }
                    data.append(d)
                return data, 200
            else:
                #Student is not enrolled
                raise StudentNotEnrolled(status_code=404, error_msg='Student is not enrolled in any course')
        else:
            # Invalid student id
            raise E2e(status_code=400, error_code=error_dict['E2e'][0], error_msg=error_dict['E2e'][1])
        
        
    def post(self, student_id):
        args = create_student_enroll_parser.parse_args()
        c_id = args.get("course_id", None)
        #print(type(c_id), c_id)
        ID = student_id
        student = Student.query.filter_by(student_id=ID).first()
        if student:
            if c_id is not None and type(c_id) is str and c_id.isnumeric(): #all args are string
                c_id = int(c_id)
                course = Course.query.filter_by(course_id=c_id).first()
                if course:
                    enroll = Enrollment(student_id = ID, course_id=c_id)
                    db.session.add(enroll)
                    db.session.commit()
                    enrolls = Enrollment.query.filter_by(student_id=ID).all()
                    data = []
                    for i,enroll in enumerate(enrolls):
                        d = {
                            "enrollment_id": enroll.enrollment_id,
                            "student_id": enroll.student_id,
                            "course_id": enroll.course_id
                            }
                        data.append(d)
                    return data, 201 
                else:
                    raise E1e(status_code=400, error_code=error_dict['E1e'][0], error_msg=error_dict['E1e'][1])
            else: #doubt about this 'else'
                raise E1e(status_code=400, error_code=error_dict['E1e'][0], error_msg=error_dict['E1e'][1])  
        else:
            # Invalid student id
            raise StudentNotFound(status_code=404, error_msg='Student not found')
         
    def delete(self, student_id, course_id):
        s_id = student_id
        c_id = course_id
        student = Student.query.filter_by(student_id=s_id).first()
        course = Course.query.filter_by(course_id=c_id).first()
        #print(student, course)
        if student:
            enrolls = Enrollment.query.filter_by(student_id=s_id).all()
            if len(enrolls)<1:
                raise StudentNotEnrolled(status_code=404, error_msg='Enrollment for the student not found')
            if course:
                enroll = Enrollment.query.filter_by(student_id = s_id, course_id=c_id).first()
                db.session.delete(enroll)
                db.session.commit()
                raise Success(status_code=200, error_msg='')
            else:
                raise E1e(status_code=400, error_code=error_dict['E1e'][0], error_msg=error_dict['E1e'][1]) 
        else:
            raise E2e(status_code=400, error_code=error_dict['E2e'][0], error_msg=error_dict['E2e'][1])  
                
        
        
#--------------------  Add Resource  --------------------
api.add_resource(CourseAPI, "/api/course", "/api/course/<int:course_id>")
api.add_resource(StudentAPI, "/api/student", "/api/student/<int:student_id>")
api.add_resource(EnrollmentAPI, "/api/student/<int:student_id>/course", "/api/student/<int:student_id>/course/<int:course_id>")

#--------------------  Main  --------------------
if __name__ == '__main__':
    app.debug = True
    app.host = '127.0.0.1'
    app.port = 5000
    app.run()

#--------------------  End  --------------------