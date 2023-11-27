from django.shortcuts import render, redirect
from django.views import View
from .models import Course, MyUser, Section
from django.http import HttpResponseRedirect
from operator import itemgetter
import re
"""
Login verifies the user has an account created and all inputs are valid. Adds their username to a session token as well as if they're an admin 
and redirects to the dashboard
Failure returns a render with a failure method    
"""
def func_Login(request):
    noSuchUser = False
    isWrongPassword = False
    isBlank = ("" == request.POST['email']) or ("" == request.POST['password'])
    try:
        user = MyUser.objects.get(email=request.POST['email'])
        isWrongPassword = (user.password != request.POST['password'])

    except:
        noSuchUser = True
    if isBlank:
        return "Fields cannot be blank."
    elif noSuchUser:
        return "That username does not exist."
    elif isWrongPassword:
        return "Incorrect password."
    else:
        return "success."
"""
Logout redirects the page to the login page and flushes the session of any tokens
"""

def func_AlphabeticalMyUserList(user_bin):
    userList = []
    for user in user_bin:
        thisdict = {
            "lastname": user.lastName,
            "fullname": user.__str__(),
            "email": user.email,
            "role": user.role
        }
        userList.append(thisdict)
    alphabetical = sorted(userList, key=itemgetter('lastname'))
    return alphabetical

def func_UserAsDict(userEmail):
    if userEmail is None:
        raise Exception("User does not exist!")
    user = MyUser.objects.filter(email=userEmail).first()
    dict = {
        "id": user.id,
        "email": user.email,
        "firstname": user.firstName,
        "lastname": user.lastName,
        "phonenumber": user.phoneNumber,
        "streetaddress": user.streetAddress,
        "city": user.city,
        "state": user.state,
        "zipcode": user.zipcode,
        "role": user.role,
        "fullname": user.__str__()
    }
    return dict

def func_AlphabeticalCourseList(course_bin):
    courseList = []
    for course in course_bin:
        thisdict = {
            "title": course.__str__(),
            "id": course.id,
            "semester": course.semester,
            "year":course.year
        }
        courseList.append(thisdict)
    alphabetical = sorted(courseList, key=itemgetter('title'))
    return alphabetical

def func_CourseAsDict(courseID):
    if courseID is None:
        raise Exception("Course does not exist!")
    course = Course.objects.filter(id=courseID).first()
    dict = {
        "id": course.id,
        "title": course.__str__(),
        "name": course.name,
        "department": course.department,
        "coursenumber": course.courseNumber,
        "semester": course.semester,
        "year": course.year,
        "users": func_AlphabeticalMyUserList(MyUser.objects.filter(course__id=courseID)),
        "sections": func_AscendingSectionList(Section.objects.filter(course=courseID))
    }
    return dict

def func_AscendingSectionList(section_bin):
    sectionList = []
    for section in section_bin:
        thisdict = {
            "title": section.__str__(),
            "id": section.id,
        }
        sectionList.append(thisdict)
    alphabetical = sorted(sectionList, key=itemgetter('title'))
    return alphabetical

def func_SectionAsDict(sectionID):
    if sectionID is None:
        raise Exception("Section does not exist!")
    section = Section.objects.filter(id=sectionID).first()
    if section.assignedUser != None:
        dict = {
            "id": section.id,
            "sectionnumber": section.sectionNumber,
            "type": section.type,
            "location": section.location,
            "daysmeeting": section.daysMeeting,
            "starttime": section.startTime,
            "endtime": section.endTime,
            "course": func_CourseAsDict(section.course.id),
            "assigneduser": func_UserAsDict(section.assignedUser.email)
        }
    else:
        dict = {
            "id": section.id,
            "sectionnumber": section.sectionNumber,
            "type": section.type,
            "location": section.location,
            "daysmeeting": section.daysMeeting,
            "starttime": section.startTime,
            "endtime": section.endTime,
            "course": func_CourseAsDict(section.course.id)
        }
    return dict

"""
POST Functions. These happen from button presses and form submissions.
Check if all the context variables from request.POST['variable'] are valid using validator functions
and create an object and returns a render of a page with a success message
If a validator function fails then no object is created and a render is returned with a failure method.   
"""
def func_CreateUser(request):
    return redirect("/login")
def func_EditUser(request):
    if 'firstname' in request.POST:
        if func_ValidateFirstName(request.POST['firstname']):
            changeUser = MyUser.objects.filter(email=request.session['selecteduser']).first()
            changeUser.firstName = request.POST['firstname']
            changeUser.save()
            return "First Name changed successfully"
        else:
            return "Invalid First Name"
    if 'lastname' in request.POST:
        if func_ValidateLastName(request.POST['lastname']):
            changeUser = MyUser.objects.filter(email=request.session['selecteduser']).first()
            changeUser.lastName = request.POST['lastname']
            changeUser.save()
            return "Last Name changed successfully"
        else:
            return "Invalid Last Name"
    if 'phonenumber' in request.POST:
        if func_ValidatePhoneNumber(request.POST['phonenumber']):
            changeUser = MyUser.objects.filter(email=request.session['selecteduser']).first()
            changeUser.phoneNumber = request.POST['phonenumber']
            changeUser.save()
            return "Phone Number changed successfully"
        else:
            return "Invalid Phone Number"
    if 'streetaddress' in request.POST:
        if func_ValidateStreetAddress(request.POST['streetaddress']):
            changeUser = MyUser.objects.filter(email=request.session['selecteduser']).first()
            changeUser.streetAddress = request.POST['streetaddress']
            changeUser.save()
            return "Street Address changed successfully"
        else:
            return "Invalid Street Address"
    if 'city' in request.POST:
        if func_ValidateCity(request.POST['city']):
            changeUser = MyUser.objects.filter(email=request.session['selecteduser']).first()
            changeUser.city = request.POST['city']
            changeUser.save()
            return "City changed successfully"
        else:
            return "Invalid City"
    if 'state' in request.POST:
        if func_ValidateState(request.POST['state']):
            changeUser = MyUser.objects.filter(email=request.session['selecteduser']).first()
            changeUser.state = request.POST['state']
            changeUser.save()
            return "State changed successfully"
        else:
            return "Invalid State"
    if 'zipcode' in request.POST:
        if func_ValidateZipCode(request.POST['zipcode']):
            changeUser = MyUser.objects.filter(email=request.session['selecteduser']).first()
            changeUser.zipcode = request.POST['zipcode']
            changeUser.save()
            return "Zipcode changed successfully"
        else:
            return "Invalid Zipcode"
    if 'role' in request.POST:
        if func_ValidateRole(request.POST['role']):
            changeUser = MyUser.objects.filter(email=request.session['selecteduser']).first()
            changeUser.role = request.POST['role']
            changeUser.save()
            return "Role changed successfully"
        else:
            return "Invalid Role"

def func_DeleteUser(request):
    return redirect("/login")
def func_CreateCourse(request):
    return redirect("/login")
def func_EditCourse(request):
    return redirect("/login")
def func_DeleteCourse(request):
    return redirect("/login")
def func_CreateSection(request):
    return redirect("/login")
def func_EditSection(request):
    return redirect("/login")
def func_DeleteSection(request):
    return redirect("/login")
"""
MyUser validator functions used when creating or editing MyUser objects
"""
def func_ValidateEmail(email):
    if re.findall("[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return True
    else:
        return False
def func_ValidatePassword(password,confirmPassword):
    if password != confirmPassword:
        return False
    if len(password) < 8 or len(password) > 20:
        return False

    special = ["@", "#", "$", "%",
               "^", "&", "*", "`",
               "(", ")", "-", "_",
               "+", "=", "{", "}",
               "|", "~", "/", "",
               "<", ">", ",", ".",
               ";", ":", "'", "?",
               "!"]

    if not any(char in special for char in password):
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    return True



def func_ValidateFirstName(firstName):
    if all(c.isalpha or c == '' for c in firstName):
        if firstName[0].isupper():
            return True
        else:
            return False
    else:
        return False
def func_ValidateLastName(lastName):
    if all(c.isalpha or c == '' for c in lastName):
        if lastName[0].isupper():
            return True
        else:
            return False
    else:
        return False
def func_ValidatePhoneNumber(phoneNumber):
    pattern1 = re.compile(r'^\(\d{3}\)\d{3}-\d{4}$')
    pattern2 = re.compile(r'^\d{3}-\d{3}-\d{4}$')
    pattern3 = re.compile(r'^\d{10}$')
    pattern4 = re.compile(r'^\(\d{3}\)\d{7}$')

    match1 = pattern1.match(phoneNumber)
    match2 = pattern2.match(phoneNumber)
    match3 = pattern3.match(phoneNumber)
    match4 = pattern4.match(phoneNumber)

    return bool(match1) or bool(match2) or bool(match3) or bool(match4)

def func_ValidateStreetAddress(streetAddress):
    pattern = re.compile(r'^\d+\s+[a-zA-Z\s]{1,50}$')
    match = pattern.match(streetAddress)
    return bool(match)

def func_ValidateCity(city):
    pattern = re.compile(r'^[a-zA-Z\s]{1,20}$')
    match = pattern.match(city)
    return bool(match)
def func_ValidateState(state):
    valid_state = ["AL", "AK", "AZ", "AR",
                   "CA", "CO", "CT", "DC",
                   "DE", "FL", "GA", "HI",
                   "ID", "IL", "IN", "IA",
                   "KS", "KY", "LA", "ME",
                   "MD", "MA", "MI", "MN",
                   "MS", "MO", "MT", "NE",
                   "NV", "NH", "NJ", "NM",
                   "NY", "NC", "ND", "OH",
                   "OK", "OR", "PA", "RI",
                   "SC", "SD", "TN", "TX",
                   "UT", "VT", "VA", "WA",
                   "WV", "WI", "WY"]

    return state in valid_state

def func_ValidateZipCode(zip):
    pattern = re.compile(r'^\d{5}$')
    return bool(pattern.match(zip))
def func_ValidateRole(role):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("instructor", "Instructor"),
        ("ta", "TA")
    ]
    return role in ROLE_CHOICES
"""
Course validator functions used when creating or editing Course objects
"""
def func_ValidateCourseName(name):
    pass
def func_ValidateDepartment(department):
    pass
def func_ValidateCourseNumber(courseNumber):
    pass
def func_ValidateSemester(Semester):
    pass
def func_ValidateYear(year):
    pass
"""
Section validator functions used when creating or editing Section objects
"""
def func_ValidateSectionNumber(sectionNumber):
    pass
def func_ValidateLocation(location):
    pass
def func_ValidateDaysMeeting(daysMeeting):
    pass
def func_ValidateStartAndEndTime(startTime, endTime):
    pass

