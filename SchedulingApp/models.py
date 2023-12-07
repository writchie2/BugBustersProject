from django.db import models

class MyUser(models.Model):
    email = models.CharField(max_length=30, default="default@uwm.edu", editable=True)
    password = models.CharField(max_length=20, default="defaultpassword", editable=True)
    firstName = models.CharField(max_length=20, default="defaultfirstname", editable=True)
    lastName = models.CharField(max_length=20, default="defaultlastname", editable=True)
    phoneNumber = models.CharField(max_length=20, default="defaultphonenumber", editable=True)
    streetAddress = models.CharField(max_length=100, default="1234 Main st", editable=True)
    city = models.CharField(max_length=20, default="Milwaukee", editable=True)
    state = models.CharField(max_length=2, default="WI", editable=True)
    zipcode = models.CharField(default="53206",max_length=10, editable=True)
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("instructor", "Instructor"),
        ("ta", "TA")
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="ad", editable=True)
    bio = models.TextField(default="No bio added.", max_length=500, editable=True)
    def __str__(self):
        return self.firstName + " " + self.lastName

class Course(models.Model):
    name = models.CharField(max_length=100, default="Default Course Name", editable=True)
    DEPARTMENT_CHOICES = [
        "AMLLC", "ACTSCI", "AD LDSP", "AFAS", "AFRIC", "AIS", "ANTHRO", "ARABIC", "ARCH", "ART", "ART ED", "ARTHIST",
        "ASTRON", "ATM SCI", "ATRAIN", "BIO SCI", "BME", "BMS", "BUS ADM", "BUSMGMT", "CELTIC", "CES", "CGS AIS",
        "CGS ANT", "CGS ART", "CGS AST", "CGS BIO", "CGS BUS", "CGS CHE", "CGS CPS", "CGS CTA", "CGS ECO", "CGS EDU",
        "CGS EGR", "CGS ENG", "CGS ESL", "CGS FRE", "CGS GEO", "CGS GER", "CGS GLG", "CGS GSW", "CGS HES", "CGS HIS",
        "CGS INT", "CGS IST", "CGS ITA", "CGS LEA", "CGS LEC", "CGS MAT", "CGS MLG", "CGS MUA", "CGS MUS", "CGS PHI",
        "CGS PHY", "CGS POL", "CGS PSY", "CGS REL", "CGS SOC", "CGS SPA", "CHEM", "CHINESE", "CHS", "CIV ENG",
        "CLASSIC", "COMMUN", "COMPLIT", "COMPSCI", "COMPST", "COMSDIS", "COUNS", "CRM JST", "CURRINS", "DAC", "DANCE",
        "DMI", "EAP", "EAS", "ECON", "ED POL", "ED PSY", "EDUC", "ELECENG", "ENGLISH", "ETHNIC", "EXCEDUC", "FILM",
        "FILMSTD", "FINEART", "FOODBEV", "FRENCH", "FRSHWTR", "GEO SCI", "GEOG", "GERMAN", "GLOBAL", "GRAD", "GREEK",
        "HCA", "HEBREW", "HI", "HIST", "HMONG", "HONORS", "HS", "IEP", "IND ENG", "IND REL", "INFOST", "INTLST",
        "ITALIAN", "JAMS", "JAPAN", "JEWISH", "KIN", "KOREAN", "L&S HUM", "L&S NS", "L&S SS", "LACS", "LACUSL",
        "LATIN", "LATINX", "LGBT", "LIBRLST", "LINGUIS", "MALLT", "MATH", "MATLENG", "MECHENG", "MIL SCI", "MSP",
        "MTHSTAT", "MUS ED", "MUSIC", "MUSPERF", "NEURO", "NONPROF", "NURS", "NUTR", "OCCTHPY", "PEACEST", "PH",
        "PHILOS", "PHYSICS", "POL SCI", "POLISH", "PORTUGS", "PRPP", "PSYCH", "PT", "PUB ADM", "RELIGST", "RUSSIAN",
        "SCNDVST", "SOC WRK", "SOCIOL", "SPANISH", "SPT&REC", "TCH LRN", "THEATRE", "THERREC", "TRNSLTN", "URB STD",
        "URBPLAN", "UWS NSG", "UWX", "WGS"
    ]
    department = models.CharField(max_length=12, default="LATIN", editable=True)
    courseNumber = models.IntegerField(default=123, editable=True)
    Semester_CHOICES = [
        ("spring", "Spring"),
        ("summer", "Summer"),
        ("fall", "Fall"),
        ("winter", "Winter")
    ]
    semester = models.CharField(max_length=6, choices=Semester_CHOICES, default="Spring", editable=True)
    year = models.IntegerField(default=2023, editable=True)
    assignedUser = models.ManyToManyField(MyUser, blank=True)

    def __str__(self):
        return self.department + " " + str(self.courseNumber) + " " + self.name

class Section(models.Model):
    sectionNumber = models.IntegerField(default=400, editable=True)
    TYPE_CHOICES = [
        ("lecture", "Lecture"),
        ("grader", "Grader"),
        ("lab", "Lab")
    ]
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default="le", editable=True)
    location = models.CharField(max_length=100, default="defaultlocation", editable=True)
    daysMeeting = models.CharField(max_length=7, default="MTWHF", editable=True)
    startTime = models.CharField(max_length=50, default="defaultstarttime", editable=True)
    endTime = models.CharField(max_length=50, default="defaultendtime", editable=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignedUser = models.ForeignKey(MyUser, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.sectionNumber) + " " + self.type.capitalize()
