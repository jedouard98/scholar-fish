import jinja2
import os
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class BasicInfo(ndb.Model):
    first_name = ndb.StringProperty(required="true")
    last_name = ndb.StringProperty(required="true")
    birthday = ndb.StringProperty(required="true")
    grade_level = ndb.StringProperty(required="true")
    high_school_grad = ndb.StringProperty(required="true")
    address = ndb.StringProperty(required="true")
    city = ndb.StringProperty(required="true")
    state = ndb.StringProperty(required="true")
    zip_code = ndb.StringProperty(required="true")
    email_address = ndb.StringProperty(required="true")
    home_phone_number = ndb.StringProperty(required="true")
    cell_phone_number = ndb.StringProperty(required="true")
    religious_preference = ndb.StringProperty(required="true")
    us_armed_forces_status = ndb.StringProperty(required="true")
    race = ndb.StringProperty(required="true")
    citizenship = ndb.StringProperty(required="true")

class CompanyInfo(ndb.Model):
    comapny_name = ndb.StringProperty(required="true")
    grade_level = ndb.StringProperty(required="true")
    due_date = ndb.StringProperty(required="true")
    gpa = ndb.StringProperty(required="true")
    address = ndb.StringProperty(required="true")
    city = ndb.StringProperty(required="true")
    state = ndb.StringProperty(required="true")
    zip_code = ndb.StringProperty(required="true")
    student_status = ndb.StringProperty(required="true")
    religious_preference = ndb.StringProperty(required="true")
    us_armed_forces_status = ndb.StringProperty(required="true")
    race = ndb.StringProperty(required="true")
    citizenship = ndb.StringProperty(required="true")
    diploma = ndb.StringProperty(required="true")
    student_status = ndb.StringProperty(required="true")

class GuppyUser(ndb.Model):
    email_user_id = ndb.StringProperty(required="true")
    isStudent = ndb.StringProperty(required="true")
    basic_info = ndb.KeyProperty(BasicInfo)
    company_info = ndb.KeyProperty(CompanyInfo)
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
                self.redirect('/student-or-scholar')
            #if the user is totally already in the database....
            else:
                #changes the greeting on the homepage
                greeting = ('<a href="%s">Sign out!</a>.' %
                    users.create_login_url('/'))
        else:
            greeting = ('<a href="%s">Sign in with your gmail account!</a>.' %
                users.create_login_url('/'))

        template_vars = {'login' : greeting}
        template = jinja_environment.get_template('templates/homepage.html')
        self.response.write(template.render(template_vars))

class StudentHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/student-or-scholar.html')
        self.response.write(template.render())
    def post(self):
        userChoice = self.request.get('student-or-scholar-option')
        guppyuser = GuppyUser(email_user_id=users.get_current_user().user_id(), isStudent=userChoice)
        guppyuser.put()
        if userChoice == 'True':
            self.redirect('/basic-info')
        else:
            self.redirect('/companyinfo')

class BasicInfoHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/basic-info.html')
        self.response.write(template.render())

    def post(self):
        basic_info = BasicInfo(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),

            birthday=self.request.get('birthday'),
            grade_level=self.request.get('grade_level'),
            high_school_grad=self.request.get('graduation_year'),
            address=self.request.get('address'),
            city=self.request.get('city'),
            state=self.request.get('states'),
            zip_code= self.request.get('zipcode'),
            email_address = self.request.get('email'),
            home_phone_number = self.request.get('homephone'),
            cell_phone_number =self.request.get('cellphone'),
            religious_preference = self.request.get('religion'),
            us_armed_forces_status = self.request.get('military'),
            race = self.request.get('race'),
            citizenship= self.request.get('citizenship'))
        info_key = basic_info.put()


        self.redirect('/')

class CompanyInfoHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/companyinfo.html')
        self.response.write(template.render())

    def post(self):
        company_info = CompanyInfo(
            comapny_name=self.request.get('comapny_name'),
            grade_level=self.request.get('grade_level'),
            due_date=self.request.get('due_date'),
            address=self.request.get('address'),
            city=self.request.get('city'),
            state=self.request.get('states'),
            zip_code= self.request.get('zipcode'),
            student_status = self.request.get('student_status'),
            gpa= self.request.get('gpa'),
            diploma =self.request.get('diploma'),
            religious_preference = self.request.get('religion'),
            us_armed_forces_status = self.request.get('millitary'),
            race = self.request.get('race'),
            citizenship= self.request.get('citizenship'))
        info_key = company_info.put()
        self.redirect('/')

class ScholarListHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/scholar-list.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/student-or-scholar', StudentHandler),
  ('/basic-info', BasicInfoHandler),
  ('/companyinfo', CompanyInfoHandler),
  ('/scholar-list', ScholarListHandler),
], debug=True)
