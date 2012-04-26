from google.appengine.ext import webapp
from google.appengine.ext.db import GqlQuery
from scripts.main import BaseHandler
from scripts.database_models import HomepageSlide

class SlideHandler(BaseHandler):
    def get(self):
      dbSlide = GqlQuery("SELECT * FROM HomepageSlide WHERE CompleteURL = :1", self.request.path).get()
      # TODO: add error checking
      if dbSlide == None:
        pass
      elif dbSlide.Enabled == True:
        self.render_template("slide.html",
          { 'title':dbSlide.Title,
            'slide':dbSlide,
          })


application = webapp.WSGIApplication([
  ('/slide.*', SlideHandler),
  ], debug=True)
