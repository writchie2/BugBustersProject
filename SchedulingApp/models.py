from django.db import models

class MyUser(models.Model):
    email = models.CharField(max_length=20, default="default@uwm.edu", editable=True)
    password = models.CharField(max_length=20, default="defaultpassword", editable=True)
    firstName = models.CharField(max_length=20, default="defaultfirstname", editable=True)
    lastName = models.CharField(max_length=20, default="defaultlastname", editable=True)
    phoneNumber = models.CharField(max_length=20, default="defaultphonenumber", editable=True)
    streetAddress = models.CharField(max_length=50, default="1234 Main st", editable=True)
    city = models.CharField(max_length=20, default="Milwaukee", editable=True)
    state = models.CharField(max_length=2, default="WI", editable=True)
    zipcode = models.IntegerField(default=53206, editable=True)
    ROLE_CHOICES = [
        ("ad", "Admin"),
        ("in", "Instructor"),
        ("ta", "TA")
    ]
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default="ad", editable=True)

class Course(models.Model):
    name = models.CharField(max_length=50, default="defaultcoursename", editable=True)
    department = models.CharField(max_length=20, default="defaultdept", editable=True)
    courseNumber = models.IntegerField(default=1234, editable=True)
    Semester_CHOICES = [
        ("sp", "Spring"),
        ("su", "Summer"),
        ("fa", "Fall"),
        ("wi", "Winter")
    ]
    semester = models.CharField(max_length=2, choices=Semester_CHOICES, default="fa", editable=True)
    year = models.IntegerField(default=2023, editable=True)
    assignedUser = models.ManyToManyField(MyUser,  null=True)

class Section(models.Model):
    sectionNumber = models.IntegerField(default=400, editable=True)
    TYPE_CHOICES = [
        ("le", "Lecture"),
        ("gr", "Grader"),
        ("se", "Section")
    ]
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default="le", editable=True)
    location = models.CharField(max_length=50, default="defaultlocation", editable=True)
    daysMeeting = models.CharField(max_length=7, default="MWTHF", editable=True)
    startTime = models.CharField(max_length=50, default="defaultstarttime", editable=True)
    endTime = models.CharField(max_length=50, default="defaultendtime", editable=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignedUser = models.ForeignKey(MyUser, on_delete=models.PROTECT, null=True)
