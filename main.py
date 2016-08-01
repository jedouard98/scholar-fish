import jinja2
import os
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2



jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class GuppyUser(ndb.Model):
    email_user_id = ndb.StringProperty(required="true")
    #
    #   totally add later
    # basic_info = ndb.KeyProperty()
    # scholarship_organizations = ndb.KeyProperty()
    #   totally add later

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        greeting = ''
        if user:
            user_id = user.user_id()

            #looks for user in database
            user_identification = GuppyUser.query().filter(GuppyUser.email_user_id == user_id)

            #if the user is not in the database after logging in.....
            if not user_identification.get():
                #...logs you in and redirects you to basic info where you can create your instance in the database
                self.redirect('/basic-info')
            #if the user is totally already in the database....
            else:
                #changes the greeting on the homepage
                logging.info("I totally worked. Be proud of me mom.")
                greeting = ('<a href="%s">Sign out!</a>.' %
                    users.create_login_url('/'))
        else:
            greeting = ('<a href="%s">Sign in with your gmail account!</a>.' %
                users.create_login_url('/basic-info'))

        template_vars = {'login' : greeting}
        template = jinja_environment.get_template('templates/homepage.html')
        self.response.write(template.render(template_vars))

class BasicInfoHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/basic-info.html')
        self.response.write(template.render())
    def post(self):
        self.redirect('/scholar-list')
        guppyuser = GuppyUser(email_user_id=users.get_current_user().user_id())
        guppyuser.put()

class ScholarListHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/scholar-list.html')
        self.response.write(template.render())



app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/basic-info', BasicInfoHandler),
  ('/scholar-list', ScholarListHandler),
], debug=True)
