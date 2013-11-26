import datetime

from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty
from ext.wtforms import validators, fields
from ext.wtforms.form import Form


def get_semester_text_from_index(index):
    semester_epoch = 2010  # index of 0 is Spring 2010
    semesters = ["Spring", "Summer", "Fall"]

    semester = semesters[index % 3]
    year = semester_epoch + index // 3

    return "{semester} {year}".format(semester=semester, year=year)


def get_index_from_semester_text(text):
    semester_epoch = 2010  # index of 0 is Spring 2010
    year = int(text[-4:])
    semester = text[:-5]
    index = (year - semester_epoch) * 3
    if semester == "Spring":
        return index + 0
    elif semester == "Summer":
        return index + 1
    elif semester == "Fall":
        return index + 2


def get_current_semester_index():
    # Jan - May (1 - 5) = Spring Semester
    # May - Aug (6 - 8) = Summer Semester
    # Aug - Dec (9 - 12) = Fall Semester
    semester_epoch = 2010  # index of 0 is Spring 2010
    utc_now = datetime.datetime.utcnow()
    year = utc_now.year
    month = utc_now.month

    index = (year - semester_epoch) * 3
    if 1 <= month <= 5:
        return index + 0
    elif 6 <= month <= 8:
        return index + 1
    elif 8 <= month <= 12:
        return index + 2


class HousingApplication_Form(Form):
    FullName = fields.TextField(
        label=u"Full Name",
        validators=[validators.required()],
    )

    EmailAddress = fields.TextField(
        label=u"Email Address",
        validators=[validators.required()],
    )
    PhoneNumber = fields.TextField(
        label=u"Phone Number",
        validators=[validators.required()],
    )
    DateOfBirth = fields.DateField(
        label=u"Date of Birth (yyyy-mm-dd)",
        validators=[validators.required()],
    )
    SplitHomeAddress = fields.TextField(
        label=u"Home Address",
        validators=[validators.required()],
    )
    SplitHomeCity = fields.TextField(
        label=u"City",
        validators=[validators.required()],
    )
    SplitHomeState = fields.SelectField(
        label=u"State",
        choices=[
            ("", ""),
            ('AK', 'Alaska'),
            ('AL', 'Alabama'),
            ('AR', 'Arkansas'),
            ('AZ', 'Arizona'),
            ('CA', 'California'),
            ('CO', 'Colorado'),
            ('CT', 'Connecticut'),
            ('DC', 'District of Columbia'),
            ('DE', 'Delaware'),
            ('FL', 'Florida'),
            ('GA', 'Georgia'),
            ('GU', 'Guam'),
            ('HI', 'Hawaii'),
            ('IA', 'Iowa'),
            ('ID', 'Idaho'),
            ('IL', 'Illinois'),
            ('IN', 'Indiana'),
            ('KS', 'Kansas'),
            ('KY', 'Kentucky'),
            ('LA', 'Louisiana'),
            ('MA', 'Massachusetts'),
            ('MD', 'Maryland'),
            ('ME', 'Maine'),
            ('MI', 'Michigan'),
            ('MN', 'Minnesota'),
            ('MO', 'Missouri'),
            ('MS', 'Mississippi'),
            ('MT', 'Montana'),
            ('NA', 'National'),
            ('NC', 'North Carolina'),
            ('ND', 'North Dakota'),
            ('NE', 'Nebraska'),
            ('NH', 'New Hampshire'),
            ('NJ', 'New Jersey'),
            ('NM', 'New Mexico'),
            ('NV', 'Nevada'),
            ('NY', 'New York'),
            ('OH', 'Ohio'),
            ('OK', 'Oklahoma'),
            ('OR', 'Oregon'),
            ('PA', 'Pennsylvania'),
            ('RI', 'Rhode Island'),
            ('SC', 'South Carolina'),
            ('SD', 'South Dakota'),
            ('TN', 'Tennessee'),
            ('TX', 'Texas'),
            ('UT', 'Utah'),
            ('VA', 'Virginia'),
            ('VT', 'Vermont'),
            ('WA', 'Washington'),
            ('WI', 'Wisconsin'),
            ('WV', 'West Virginia'),
            ('WY', 'Wyoming'),
            ('Other', 'Other'),
        ],
        validators=[validators.required()],
    )
    SplitHomeZip = fields.TextField(
        label=u"Zip Code",
        validators=[validators.required()],
    )
    CurrentGradeLevel = fields.SelectField(
        label=u"Current Grade Level",
        choices=[
            ("", ""),
            ("High School Junior", "High School Junior"),
            ("High School Senior", "High School Senior"),
            ("College Freshman", "College Freshman"),
            ("College Sophomore", "College Sophomore"),
            ("College Junior", "College Junior"),
            ("College Senior", "College Senior"),
            ("Graduate Student", "Graduate Student"),
        ],
        validators=[validators.required()],
    )
    ProposedDegree = fields.SelectField(
        label=u"Proposed Degree",
        choices=[
            ("", ""),
            ("Aerospace Engineering", "Aerospace Engineering"),
            ("Applied Mathematics", "Applied Mathematics"),
            ("Architectural Engineering", "Architectural Engineering"),
            ("Biological Sciences", "Biological Sciences"),
            ("Business & Management Systems", "Business & Management Systems"),
            ("Ceramic Engineering", "Ceramic Engineering"),
            ("Chemical Engineering", "Chemical Engineering"),
            ("Chemistry", "Chemistry"),
            ("Civil Engineering", "Civil Engineering"),
            ("Computer Engineering", "Computer Engineering"),
            ("Computer Science", "Computer Science"),
            ("Economics", "Economics"),
            ("Electrical Engineering", "Electrical Engineering"),
            ("Engineering Management", "Engineering Management"),
            ("English", "English"),
            ("Environmental Engineering", "Environmental Engineering"),
            ("Geological Engineering", "Geological Engineering"),
            ("Geology & Geophysics", "Geology & Geophysics"),
            ("History", "History"),
            ("Information Science & Technology", "Information Science & Technology"),
            ("Mechanical Engineering", "Mechanical Engineering"),
            ("Metallurgical Engineering", "Metallurgical Engineering"),
            ("Mining Engineering", "Mining Engineering"),
            ("Nuclear Engineering", "Nuclear Engineering"),
            ("Petroleum Engineering", "Petroleum Engineering"),
            ("Philosophy", "Philosophy"),
            ("Physics", "Physics"),
            ("Pre-Law", "Pre-Law"),
            ("Pre-Med", "Pre-Med"),
            ("Pre-Nursing", "Pre-Nursing"),
            ("Pre-Veterinary", "Pre-Veterinary"),
            ("Psychology", "Psychology"),
            ("Teacher Certifications", "Teacher Certifications"),
            ("Technical Communication", "Technical Communication"),
            ("Undecided Engineering", "Undecided Engineering"),
            ("Undecided", "Undecided"),
            ("Other", "Other"),
        ],
        validators=[validators.required()],
    )
    House = fields.RadioField(
        label=u"House",
        choices=[
            ("Men's Christian Campus House", "Men's Christian Campus House"),
            ("Women's Christian Campus House", "Women's Christian Campus House"),
        ],
        validators=[validators.required()],
    )
    SemesterToBegin = fields.SelectField(
        label=u"Semester for which you seek to begin residence",
        choices=[('', '')] + [(str(x), get_semester_text_from_index(x)) for x in
                              range(get_current_semester_index() + 1, get_current_semester_index() + 7)],
        validators=[validators.required()],
    )
    HowAndWhy = fields.TextAreaField(
        label=u"Briefly state how you found out about the Campus House and why you are seeking housing with us?",
        validators=[validators.required()],
    )
    LeadershipRoles = fields.TextAreaField(
        label=u"List any leadership roles in which you have served.",
        validators=[validators.required()],
    )
    TalentsAndInterests = fields.TextAreaField(
        label=u"What talents and interests do you have that you desire to explore while you are a resident?",
        validators=[validators.required()],
    )

    ParentNames = fields.TextField(
        label=u"Your Parents' Names",
        validators=[validators.required()],
    )
    ParentPhoneNumber = fields.TextField(
        label=u"Phone Number",
        validators=[validators.required()],
    )
    ParentEmail = fields.TextField(
        label=u"Email",
    )

    HomeChurchName = fields.TextField(
        label="Name of your home church",
        validators=[validators.required()],
    )
    HomeChurchMinisterName = fields.TextField(
        label="Name of the staff member",
        validators=[validators.required()],
    )
    HomeChurchPhoneNumber = fields.TextField(
        label="Phone Number",
        validators=[validators.required()],
    )
    HomeChurchEmail = fields.TextField(
        label="Email",
    )

    OtherReferenceRelation = fields.TextField(
        label="Relation to you (e.g. teacher, coach, employer)",
        validators=[validators.required()],
    )
    OtherReferenceName = fields.TextField(
        label="Name",
        validators=[validators.required()],
    )
    OtherReferencePhoneNumber = fields.TextField(
        label="Phone Number",
        validators=[validators.required()],
    )
    OtherReferenceEmail = fields.TextField(
        label="Email",
    )

    CriminalActivity = fields.TextAreaField(
        label="Have you ever been convicted of a crime? If yes, please explain.",
        validators=[validators.required()],
    )

    MedicalAllergies = fields.TextAreaField(
        label="List any medical conditions or allergies.",
    )
    Medications = fields.TextAreaField(
        label="List any medications you take on a regular basis.",
    )


class HousingApplication(NdbBaseModel):
    Archived = ndb.BooleanProperty(default=False)
    TimeSubmitted = NdbUtcDateTimeProperty(
        verbose_name="Time Submitted",
        auto_now_add=True,
    )

    Acknowledged = ndb.BooleanProperty(default=False)
    TimeAcknowledged = NdbUtcDateTimeProperty(
        verbose_name="Time Acknowledged",
    )
    AcknowledgedBy = ndb.UserProperty(
        verbose_name="Acknowledged By"
    )

    FullName = ndb.StringProperty(
        verbose_name="Full Name",
        required=True,
    )
    EmailAddress = ndb.StringProperty(
        verbose_name="Email Address",
        required=True,
    )
    PhoneNumber = ndb.StringProperty(
        verbose_name="Phone Number",
        required=True,
    )
    DateOfBirth = ndb.DateProperty(
        verbose_name="Date of Birth (yyyy-mm-dd)",
        required=True,
    )
    HomeAddress = ndb.StringProperty(
        verbose_name="Home Address (Street, City, State)",
        required=True,
    )
    CurrentGradeLevel = ndb.StringProperty(
        verbose_name="Current Grade Level",
        required=True,
        choices=[
            "High School Junior",
            "High School Senior",
            "College Freshman",
            "College Sophomore",
            "College Junior",
            "College Senior",
            "Graduate Student",
        ]
    )
    ProposedDegree = ndb.StringProperty(
        verbose_name="Proposed Degree",
        required=True,
        choices=[
            "Aerospace Engineering",
            "Applied Mathematics",
            "Architectural Engineering",
            "Biological Sciences",
            "Business & Management Systems",
            "Ceramic Engineering",
            "Chemical Engineering",
            "Chemistry",
            "Civil Engineering",
            "Computer Engineering",
            "Computer Science",
            "Economics",
            "Electrical Engineering",
            "Engineering Management",
            "English",
            "Environmental Engineering",
            "Geological Engineering",
            "Geology & Geophysics",
            "History",
            "Information Science & Technology",
            "Mechanical Engineering",
            "Metallurgical Engineering",
            "Mining Engineering",
            "Nuclear Engineering",
            "Petroleum Engineering",
            "Philosophy",
            "Physics",
            "Pre-Law",
            "Pre-Med",
            "Pre-Nursing",
            "Pre-Veterinary",
            "Psychology",
            "Teacher Certifications",
            "Technical Communication",
            "Undecided Engineering",
            "Undecided",
            "Other",
        ]
    )
    House = ndb.StringProperty(
        verbose_name="House",
        required=True,
        choices=[
            "Men's Christian Campus House",
            "Women's Christian Campus House",
        ]
    )
    SemesterToBeginIndex = ndb.IntegerProperty(
        verbose_name="Semester for which you seek to begin residence",
        required=True,
    )

    @property
    def SemesterToBegin(self):
        return get_semester_text_from_index(self.SemesterToBeginIndex)

    HowAndWhy = ndb.TextProperty(
        verbose_name="Briefly state how you found out about the Campus House and why you are seeking housing with us?",
        required=True,
    )
    LeadershipRoles = ndb.TextProperty(
        verbose_name="List any leadership roles in which you have served.",
        required=True,
    )
    TalentsAndInterests = ndb.TextProperty(
        verbose_name="What talents and interests do you have that you desire to explore while you are a resident?",
        required=True,
    )

    ParentNames = ndb.StringProperty(
        verbose_name="Your Parents' Names",
        required=True,
    )
    ParentPhoneNumber = ndb.StringProperty(
        verbose_name="Phone Number",
        required=True,
    )
    ParentEmail = ndb.StringProperty(
        verbose_name="Email",
    )

    HomeChurchName = ndb.StringProperty(
        verbose_name="Name of your home church",
        required=True,
    )
    HomeChurchMinisterName = ndb.StringProperty(
        verbose_name="Name of the staff member",
        required=True,
    )
    HomeChurchPhoneNumber = ndb.StringProperty(
        verbose_name="Phone Number",
        required=True,
    )
    HomeChurchEmail = ndb.StringProperty(
        verbose_name="Email",
    )

    OtherReferenceRelation = ndb.StringProperty(
        verbose_name="Relation to you (e.g. teacher, coach, employer)",
        required=True,
    )
    OtherReferenceName = ndb.StringProperty(
        verbose_name="Name",
        required=True,
    )
    OtherReferencePhoneNumber = ndb.StringProperty(
        verbose_name="Phone Number",
        required=True,
    )
    OtherReferenceEmail = ndb.StringProperty(
        verbose_name="Email",
    )

    CriminalActivity = ndb.TextProperty(
        verbose_name="Have you ever been convicted of a crime? If yes, please explain.",
        required=True,
    )

    MedicalAllergies = ndb.TextProperty(
        verbose_name="List any medical conditions or allergies.",
    )
    Medications = ndb.TextProperty(
        verbose_name="List any medications you take on a regular basis.",
    )

    # TODO: convert notes to use this?
    #Notes = ndb.KeyProperty(
    #    kind=HousingApplicationNote,
    #    repeated=True,
    #)

    def generateHtmlMailMessageBody(self):
        url = "www.rollaccf.org/manage/housing_applications/view/%s" % self.key.urlsafe()
        return """<p>A new application has been submitted to %s.</p>
              <p><a href="%s">%s</a></p>""" % (self.House, url, url)

    def generatePlainTextMailMessageBody(self):
        url = "www.rollaccf.org/manage/housing_applications/view/%s" % self.key.urlsafe()
        return """A new application has been submitted to %s.\n
              %s""" % (self.House, url)


class HousingApplicationNote_Form(Form):
    Content = fields.TextAreaField(
        label=u"Content",
        validators=[validators.required()],
    )


class HousingApplicationNote(NdbBaseModel):
    Createdby = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)

    Content = ndb.TextProperty(
        required=True,
    )
    Application = ndb.KeyProperty(
        kind=HousingApplication,
    )
