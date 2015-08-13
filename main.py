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

class Thesis(ndb.Model):
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

class  DeleteThesis(webapp2.RequestHandler):
    def get(self,th_id):
        d = Thesis.get_by_id(int(th_id))
        d.key.delete()
        self.redirect('/')

class APIHandlerPage(webapp2.RequestHandler):
    def get(self):
        thesis = Thesis.query().order(-Thesis.date).fetch()
        thesis_list = []

        for thes in thesis:
            thesis_list.append({
                'self_id':thes.key.id(),
                'thesis_title':thes.thesis_title,
                'thesis_adviser':thes.thesis_adviser,
                'thesis_abstract':thes.thesis_abstract,
                'yearlist':thes.yearlist,
                'section':thes.section
                })

        response = {
            'result':'OK',
            'data':thesis_list
        }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        thesis = Thesis()
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.thesis_abstract = self.request.get('thesis_abstract')
        thesis.thesis_adviser = self.request.get('thesis_adviser')
        thesis.yearlist = int(self.request.get('yearlist'))
        thesis.section = int(self.request.get('section'))
        thesis.put()
        
        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result':'OK',
            'data':{
                'self_id':thesis.key.id(),
                'thesis_title':thesis.thesis_title,
                # 'thesis_adviser':student.thesis_adviser,
                # 'thesis_abstract':student.thesis_abstract,
                'yearlist':thesis.yearlist,
                # 'section':student.section
            }
        }
        self.response.out.write(json.dumps(response))

class  ThesisEdit(webapp2.RequestHandler):
    def get(self,th_id):
        s = Thesis.get_by_id(int(th_id))
        template_data = {
            'thesis': s
        }
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_data))
    def post(self,th_id):
        thesis = Thesis.get_by_id(int(th_id))
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.thesis_abstract = self.request.get('thesis_abstract')
        thesis.thesis_adviser = self.request.get('thesis_adviser')
        thesis.yearlist = int(self.request.get('yearlist'))
        thesis.section = int(self.request.get('section'))
        thesis.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/handler', APIHandlerPage),
    ('/thesis/delete/(.*)', DeleteThesis),
    ('/thesis/edit/(.*)', ThesisEdit)
], debug=True)