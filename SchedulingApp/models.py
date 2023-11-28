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
        ("admin", "Admin"),
        ("instructor", "Instructor"),
        ("ta", "TA")
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="ad", editable=True)
    def __str__(self):
        return self.firstName + " " + self.lastName

class Course(models.Model):
    name = models.CharField(max_length=50, default="defaultcoursename", editable=True)
    department = models.CharField(max_length=20, default="defaultdept", editable=True)
    courseNumber = models.IntegerField(default=1234, editable=True)
    Semester_CHOICES = [
        ("spring", "Spring"),
        ("summer", "Summer"),
        ("fall", "Fall"),
        ("winter", "Winter")
    ]
    semester = models.CharField(max_length=6, choices=Semester_CHOICES, default="fa", editable=True)
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
    location = models.CharField(max_length=50, default="defaultlocation", editable=True)
    daysMeeting = models.CharField(max_length=7, default="MTWHF", editable=True)
    startTime = models.CharField(max_length=50, default="defaultstarttime", editable=True)
    endTime = models.CharField(max_length=50, default="defaultendtime", editable=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignedUser = models.ForeignKey(MyUser, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.sectionNumber) + " " + self.type.capitalize()
