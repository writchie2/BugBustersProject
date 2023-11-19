from django.db import models

class MyUser(models.Model):
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    role = models.CharField(max_length=20)

class Course(models.Model):
    name = models.CharField(max_length=20)
    department = models.CharField(max_length=20)
    courseNumber = models.IntegerField()
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    assignedUser = models.ManyToManyField(MyUser,  null=True,)

class Section(models.Model):
    sectionNumber = models.IntegerField()
    type = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    daysMeeting = models.CharField(max_length=7)
    startTime = models.CharField(max_length=50)
    endTime = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignedUser = models.ForeignKey(MyUser, on_delete=models.PROTECT, null=True)
