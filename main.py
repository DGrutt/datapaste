#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
import datetime
from datetime import datetime, timedelta


from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
  
class Content(db.Model):
    content = db.TextProperty(required = True)
    password = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
	
class MainPage(Handler):
    def render_front(self, content="", error="", password="", created="", timestamp=""):
        contents=db.GqlQuery("SELECT * FROM Content ORDER BY created ASC")
        self.render("front.html", password=password, content=content, error=error, contents=contents, created=created, timestamp=timestamp)
        
    def get(self):
        self.render_front()
        
    def post(self):
        content = self.request.get("content")
        password = self.request.get("password")
        timestamp = self.request.get("timestamp")
		
        if content and password=="x":
            a = Content(content=content, password=password, timestamp=datetime)
            a.put()
            
            self.redirect("/")
        else:
            error = "We need content and the password!"
            self.render_front(content, error)
               

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)