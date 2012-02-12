from os.path import join
from google.appengine.api import images, memcache
from google.appengine.ext import webapp
from google.appengine.ext.db import GqlQuery, to_dict
from scripts.main import BaseHandler
from scripts.gaesettings import gaesettings
from scripts.database_models import HomepageSlide

class ManageHomePageSlidesHandler(BaseHandler):
    def get(self):
      slides = GqlQuery("SELECT * FROM HomepageSlide").fetch(20);
      slideDicts = []
      for slide in slides:
        d = to_dict(slide)
        d['id'] = slide.key()
        slideDicts.append(d)

      self.render_template(join("manage", "homepage_slides", "homepage_slides.html"), { 'title':"Homepage Slides", 'slides':slideDicts, })

class ManageNewSlideHandler(BaseHandler):
    def get(self):
      self.render_template(join("manage", "homepage_slides", "new_slide.html"), { 'title':"New Homepage Slide", 'MaxHomepageSlides':gaesettings.MaxHomepageSlides})
    def post(self):
      # TODO: add cgi escape
      # TODO: add html handling stuff
      # TODO: add error checking
      enabled = self.request.get("enabled")
      slideImage = images.resize(self.request.get("image"), 400, 300)
      link = self.request.get("link")

      newSlide = HomepageSlide(Enabled=bool(enabled), Link=link, Image=slideImage)
      newSlide.put()

      if enabled:
        memcache.delete("homepageSlides")
      self.redirect(self.request.path)

application = webapp.WSGIApplication([
  ('/manage/homepage_slides/new_slide.*', ManageNewSlideHandler),
  ('/manage/homepage_slides.*', ManageHomePageSlidesHandler),
  ], debug=True)
