from google.appengine.ext import webapp
from webapp2_extras import jinja2

class BaseHandler(webapp.RequestHandler):
  @webapp.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def render_template(self, filename, template_args):
    self.response.out.write(self.jinja2.render_template(filename, **template_args))


#TODO: move this into its own file (with the event link handler)
from google.appengine.api import memcache
from google.appengine.ext.db import GqlQuery
from scripts.database_models import HomepageSlide
from scripts.gaesettings import gaesettings
class HomePageHandler(BaseHandler):
  def get(self):
    slides = memcache.get('homepageSlides')
    if slides == None:
      slides = GqlQuery("SELECT * FROM HomepageSlide WHERE Enabled = True ORDER BY DisplayOrder ASC").fetch(gaesettings.MaxHomepageSlides);
      if slides != []:
        memcache.set('homepageSlides', slides)

    self.render_template("index.html",
    { 'title':"Christian Campus Fellowship, Rolla Missouri",
      'slides':slides,
      'HomepageSlideRotationDelay':gaesettings.HomepageSlideRotationDelay,
    })


application = webapp.WSGIApplication([
  ('/', HomePageHandler),
  ], debug=True)

