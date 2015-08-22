import webapp2
import jinja2
import os
import logging
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)

class Thesis(ndb.Model):
    app_user = ndb.StringProperty(indexed=True)
    app_user_id = ndb.StringProperty(indexed=True)
    thesis_title = ndb.StringProperty(indexed=True)
    thesis_adviser = ndb.StringProperty(indexed=True)
    thesis_abstract = ndb.StringProperty(indexed=True)
    yearlist = ndb.IntegerProperty()
    section = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
class MainPage(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'

        template_data = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext
        }
        if user:
            template = JINJA_ENVIRONMENT.get_template('create.html')
            self.response.write(template.render(template_data))
        else:
            self.redirect(users.create_login_url(self.request.uri))
         

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
                'section':thes.section,
                'app_user':thes.app_user
                })

        response = {
            'result':'OK',
            'data':thesis_list
        }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        user = users.get_current_user()
        thesis = Thesis()
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.thesis_abstract = self.request.get('thesis_abstract')
        thesis.thesis_adviser = self.request.get('thesis_adviser')
        thesis.yearlist = int(self.request.get('yearlist'))
        thesis.section = int(self.request.get('section'))
        thesis.app_user = user.nickname()
        thesis.app_user_id = user.user_id()
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
                'app_user':thesis.app_user
            }
        }
        self.response.out.write(json.dumps(response))

class  ThesisEdit(webapp2.RequestHandler):
    def get(self,th_id):
        s = Thesis.get_by_id(int(th_id))
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        template_data = {
            'thesis': s,
            'user': user,
            'url': url,
            'url_linktext': url_linktext
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

# class Guestbook(webapp2.RequestHandler):

#     def post(self):
#         # We set the same parent key on the 'Greeting' to ensure each
#         # Greeting is in the same entity group. Queries across the
#         # single entity group will be consistent. However, the write
#         # rate to a single entity group should be limited to
#         # ~1/second.
#         guestbook_name = self.request.get('guestbook_name',
#                                           DEFAULT_GUESTBOOK_NAME)
#         greeting = Greeting(parent=guestbook_key(guestbook_name))

#         if users.get_current_user():
#             greeting.author = Author(
#                     identity=users.get_current_user().user_id(),
#                     email=users.get_current_user().email())

#         greeting.content = self.request.get('thesis_title')
#         greeting.put()

#         query_params = {'guestbook_name': guestbook_name}
#         self.redirect('/?' + urllib.urlencode(query_params))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/handler', APIHandlerPage),
    ('/thesis/delete/(.*)', DeleteThesis),
    ('/thesis/edit/(.*)', ThesisEdit),
    # ('/sign', Guestbook),
], debug=True)