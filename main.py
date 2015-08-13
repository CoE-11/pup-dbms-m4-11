import webapp2
import jinja2
import os
import logging
import urllib
from google.appengine.ext import ndb
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Student(ndb.Model):
    thesis_title = ndb.StringProperty(indexed=True)
    thesis_adviser = ndb.StringProperty(indexed=True)
    thesis_abstract = ndb.StringProperty(indexed=True)
    yearlist = ndb.IntegerProperty()
    section = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('create.html')
        self.response.write(template.render())

class  DeleteStudent(webapp2.RequestHandler):
    def get(self,stud_id):
        d = Student.get_by_id(int(stud_id))
        d.key.delete()
        self.redirect('/')

class APIHandlerPage(webapp2.RequestHandler):
    def get(self):
        students = Student.query().order(-Student.date).fetch()
        student_list = []

        for student in students:
            student_list.append({
                'self_id':student.key.id(),
                'thesis_title':student.thesis_title,
                'thesis_adviser':student.thesis_adviser,
                'thesis_abstract':student.thesis_abstract,
                'yearlist':student.yearlist,
                'section':student.section
                })

        response = {
            'result':'OK',
            'data':student_list
        }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        student = Student()
        student.thesis_title = self.request.get('thesis_title')
        student.thesis_abstract = self.request.get('thesis_abstract')
        student.thesis_adviser = self.request.get('thesis_adviser')
        student.yearlist = int(self.request.get('yearlist'))
        student.section = int(self.request.get('section'))
        student.put()
        
        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result':'OK',
            'data':{
                'self_id':student.key.id(),
                'thesis_title':student.thesis_title,
                # 'thesis_adviser':student.thesis_adviser,
                # 'thesis_abstract':student.thesis_abstract,
                'yearlist':student.yearlist,
                # 'section':student.section
            }
        }
        self.response.out.write(json.dumps(response))

class  StudentEdit(webapp2.RequestHandler):
    def get(self,stud_id):
        s = Student.get_by_id(int(stud_id))
        template_data = {
            'student': s
        }
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_data))
    def post(self,stud_id):
        student = Student()
        student.thesis_title = self.request.get('thesis_title')
        student.thesis_abstract = self.request.get('thesis_abstract')
        student.thesis_adviser = self.request.get('thesis_adviser')
        student.yearlist = int(self.request.get('yearlist'))
        student.section = int(self.request.get('section'))
        student.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/handler', APIHandlerPage),
    ('/student/delete/(.*)', DeleteStudent),
    ('/student/edit/(.*)', StudentEdit)
], debug=True)