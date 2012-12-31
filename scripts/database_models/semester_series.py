from cgi import FieldStorage
from google.appengine.ext import ndb
from wtforms import validators
from wtforms.form import Form
from wtforms.fields import *


class WeekInfo_Form(Form):
    Date = TextField()
    Speaker = TextField()
    Topic = TextField()
    Location = TextField()

class SemesterSeries_Form(Form):
    Image = FileField(u'Image')
    Title = TextField(u'Title', validators=[validators.Required()])
    Description = TextAreaField(u'Description', validators=[validators.Required(), validators.length(max=500)])
    Weeks = FieldList(FormField(WeekInfo_Form))

    def validate_Image(form, field):
        # validators.DateRequired or validators.InputRequired will not work 
        # since a FieldStorage instance does not return true in an if statement
        if not isinstance(field.data, FieldStorage):
            raise validators.ValidationError("An Image is required.")


class WeekInfo(ndb.Model):
    Date = ndb.StringProperty(
      required=True,
    )
    Speaker = ndb.StringProperty()
    Topic = ndb.StringProperty()
    Location = ndb.StringProperty()

class SemesterSeries(ndb.Model):
    Createdby = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = ndb.DateTimeProperty(auto_now_add=True)

    Image = ndb.BlobProperty(
      required=True,
    )
    Title = ndb.StringProperty(
      required=True,
    )
    Description = ndb.TextProperty(
      required=True,
    )
    Weeks = ndb.LocalStructuredProperty(
      WeekInfo, 
      repeated=True,
    )

