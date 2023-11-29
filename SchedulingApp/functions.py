from django.shortcuts import render, redirect
from django.views import View
from .models import Course, MyUser, Section
from django.http import HttpResponseRedirect
from operator import itemgetter
import re, time
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
            "role": user.role.capitalize()
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
        "role": user.role.capitalize(),
        "fullname": user.__str__()
    }
    return dict

def func_AlphabeticalCourseList(course_bin):
    courseList = []
    for course in course_bin:
        thisdict = {
            "title": course.__str__(),
            "id": course.id,
            "semester": course.semester.capitalize(),
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
    start_t = time.strptime(section.startTime, "%H:%M")
    end_t = time.strptime(section.endTime, "%H:%M")
    start_12hour = time.strftime("%I:%M %p", start_t)
    end_12hour = time.strftime("%I:%M %p", end_t)
    daysMeetingFormat = section.daysMeeting
    if daysMeetingFormat == 'A':
        daysMeetingFormat = "No Meeting Pattern"
    if section.assignedUser != None:
        dict = {
            "id": section.id,
            "sectionnumber": section.sectionNumber,
            "type": section.type.capitalize(),
            "location": section.location,
            "daysmeeting": daysMeetingFormat,
            "starttime": start_12hour,
            "endtime": end_12hour,
            "course": func_CourseAsDict(section.course.id),
            "assigneduser": func_UserAsDict(section.assignedUser.email)
        }
    else:
        dict = {
            "id": section.id,
            "sectionnumber": section.sectionNumber,
            "type": section.type.capitalize(),
            "location": section.location,
            "daysmeeting": daysMeetingFormat,
            "starttime": start_12hour,
            "endtime": end_12hour,
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
    if(
        'email' not in request.POST or 'password' not in request.POST or
        'confirmpassword' not in request.POST or 'firstname' not in request.POST or
        'lastname' not in request.POST or 'phonenumber' not in request.POST or
        'streetaddress' not in request.POST or 'city' not in request.POST or
        'state' not in request.POST or 'zipcode' not in request.POST or
        'role' not in request.POST
    ):
        return "Please fill out all fields!"
    email = request.POST["email"]
    pw = request.POST["password"]
    pwc = request.POST["confirmpassword"]
    first = request.POST["firstname"]
    last = request.POST["lastname"]
    phone = request.POST["phonenumber"]
    street = request.POST["streetaddress"]
    city = request.POST["city"]
    state = request.POST["state"]
    zip = int(request.POST["zipcode"])
    role = request.POST["role"]

    if (not func_ValidateEmail(email)) or (MyUser.objects.filter(email=email).exists()):
        return "Non-unique username. Please try again."
    if not func_ValidatePassword(pw, pwc):
        return "Passwords do not match. Please try again."
    if not func_ValidateFirstName(first):
        return "Invalid first name. Must start with a capital and have no spaces. Please try again."
    if not func_ValidateLastName(last):
        return "Invalid last name. Must start with a capital and have no spaces. Please try again."
    if not func_ValidatePhoneNumber(phone):
        return "Invalid phone number. Must be 9 numbers 0-9. Please try again."
    if not func_ValidateStreetAddress(street):
        return "Invalid street address. Please try again."
    if not func_ValidateCity(city):
        return "Invalid city. Please try again."
    if not func_ValidateState(state):
        return "Invalid state. Please try again."
    if not func_ValidateZipCode(zip):
        return "Invalid zipcode. Please try again."
    if not func_ValidateRole(role):
        return "Invalid role. Please try again."

    user = MyUser.objects.create(email=email, password=pw,
                                 firstName=first, lastName=last,
                                 phoneNumber=phone, streetAddress=street,
                                 city=city, state=state,
                                 zipcode=zip, role=role)
    user.save()
    return "User created successfully!"

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
    MyUser.objects.filter(id=request.session['selecteduser']).first().delete()
def func_CreateCourse(request):
    if ('coursename' not in request.POST or 'department' not in request.POST or
            'coursenumber' not in request.POST
            or 'semester' not in request.POST or 'year' not in request.POST):
        return "Please fill out all fields!"
    newCourseName = request.POST['coursename']
    newCourseDepartment = request.POST['department']
    newCourseNumber = int(request.POST['coursenumber'])
    newCourseSemester = request.POST['semester']
    newCourseYear = int(request.POST['year'])
    if func_ValidateCourseName(newCourseName) == False:
        return "Invalid Course Name. Only letters and single spaces are allowed."
    if func_ValidateDepartment(newCourseDepartment) == False:
        return "Invalid Department. All Departments come from the UWM course cataloge."
    if func_ValidateCourseNumber(newCourseNumber, newCourseDepartment) == False:
        return "Invalid Course Number. Must be between 100 and 999 and unique."
    if func_ValidateSemester(newCourseSemester) == False:
        return "Invalid semester. Acceptable values are fall, spring, winter, and summer"
    if func_ValidateYear(newCourseYear) == False:
        return "Invalid Year. Must be later than 1956 and cannot be greater than 2025"
    newCourse = Course.objects.create(name=newCourseName, department=newCourseDepartment,
                                      courseNumber=newCourseNumber, semester=newCourseSemester,
                                      year=newCourseYear)
    newCourse.save()
    return "Course created successfully!"

def func_EditCourse(request):
    chosen = Course.objects.filter(id=request.session['selectedcourse']).first()
    if 'coursename' in request.POST:
        newCourseName = request.POST["coursename"]
        if func_ValidateCourseName(newCourseName) == False:
            return "Invalid Course Name. Only letters and single spaces are allowed."
        else:
            chosen = Course.objects.filter(id=request.session['selectedcourse']).first()
            chosen.name = newCourseName
            chosen.save()
            return "Course Name edited successfully!"

    if 'department' in request.POST:
        newDepartment = request.POST["department"]
        if func_ValidateDepartment(newDepartment) == False:
            return "Invalid Department. All Departments come from the UWM course cataloge."
        else:
            chosen = Course.objects.filter(id=request.session['selectedcourse']).first()
            chosen.department = newDepartment
            chosen.save()
            return "Department edited successfully!"

    if 'coursenumber' in request.POST:
        newCourseNumber = int(request.POST["coursenumber"])
        chosen = Course.objects.filter(id=request.session['selectedcourse']).first()
        if func_ValidateCourseNumber(newCourseNumber, chosen.department) == False:
            return "Invalid Course Number. Must be between 100 and 999 and unique."
        else:
            chosen = Course.objects.filter(id=request.session['selectedcourse']).first()
            chosen.courseNumber = newCourseNumber
            chosen.save()
            return "Course Number edited successfully!"

    if 'semester' in request.POST:
        newSemester = request.POST["semester"]
        if func_ValidateSemester(newSemester) == False:
            return "Invalid semester. Acceptable values are fall, spring, winter, and summer"
        else:
            chosen = Course.objects.filter(id=request.session['selectedcourse']).first()
            chosen.semester = newSemester
            chosen.save()
            return "Semester edited successfully!"

    if 'year' in request.POST:
        newYear = int(request.POST["year"])
        if func_ValidateYear(newYear) == False:
            return "Invalid Year. Must be later than 1956 and cannot be greater than 2025"
        else:
            chosen = Course.objects.filter(id=request.session['selectedcourse']).first()
            chosen.year = newYear
            chosen.save()
            return "Year edited successfully!"


def func_DeleteCourse(request):
    Course.objects.filter(id=request.session['selectedcourse']).first().delete()
def func_CreateSection(request):
    if ('sectionnumber' not in request.POST or 'location' not in request.POST or
            'starttime' not in request.POST
            or'endtime' not in request.POST or 'type' not in request.POST):
        return "Please fill out all fields!"
    newSectionNumber = int(request.POST["sectionnumber"])
    newLocation = request.POST["location"]
    newDaysMeeting = ''
    for days in request.POST.getlist('daysmeeting'):
        newDaysMeeting += days
    newStartTime = request.POST["starttime"]
    newEndTime = request.POST["endtime"]
    newType = request.POST['type']
    if func_ValidateSectionNumber(newSectionNumber, request.session['selectedcourse']) == False:
        return "Invalid Section Number. Must be between 100 and 999 and unique!"
    if func_ValidateDaysMeeting(newDaysMeeting) == False:
        return "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days."
    if func_ValidateLocation(newLocation) == False:
        return "Invalid Location. Format: Room# Building Name"
    if func_ValidateSectionType(newType) == False:
        return "Invalid Type. Must be lecture, section, or grader."
    if func_ValidateStartAndEndTime(newStartTime,newEndTime) == False:
        return "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end."

    newSection = Section.objects.create(sectionNumber=newSectionNumber, type=newType,
                                        location=newLocation, daysMeeting=newDaysMeeting,
                                        startTime=newStartTime, endTime=newEndTime,
                                        course= Course.objects.filter(id=request.session['selectedcourse']).first())
    newSection.save()
    return "Section created successfully!"


def func_EditSection(request):
    chosen = Section.objects.filter(id=request.session['selectedsection']).first()
    if 'sectionnumber' in request.POST:
        newSectionNumber = int(request.POST["sectionnumber"])
        if func_ValidateSectionNumber(newSectionNumber, request.session['selectedcourse']) == False:
            return "Invalid Section Number. Must be between 100 and 999 and unique!"
        else:
            chosen = Section.objects.filter(id=request.session['selectedsection']).first()
            chosen.sectionNumber = newSectionNumber
            chosen.save()
            return "Section Number edited successfully!"

    if 'location' in request.POST:
        newLocation = request.POST["location"]
        if func_ValidateLocation(newLocation) == False:
            return "Invalid Location. Format: Room# Building Name"
        else:
            chosen = Section.objects.filter(id=request.session['selectedsection']).first()
            chosen.location = newLocation
            chosen.save()
            return "Location edited successfully!"

    if 'daysmeeting' in request.POST:
        newDaysMeeting = ''
        for days in request.POST.getlist('daysmeeting'):
            newDaysMeeting += days
        if func_ValidateDaysMeeting(newDaysMeeting) == False:
            return "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days."
        else:
            chosen = Section.objects.filter(id=request.session['selectedsection']).first()
            chosen.daysMeeting= newDaysMeeting
            chosen.save()
            return "Days Meeting edited successfully!"

    if 'starttime' in request.POST:
        newStartTime = request.POST["starttime"]
        if func_ValidateStartAndEndTime(newStartTime, chosen.endTime) == False:
            return "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end."
        else:
            chosen = Section.objects.filter(id=request.session['selectedsection']).first()
            chosen.startTime= newStartTime
            chosen.save()
            return "Start Time edited successfully!"

    if 'endtime' in request.POST:
        newEndTime = request.POST["endtime"]
        if func_ValidateStartAndEndTime(chosen.startTime, newEndTime) == False:
            return "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end."
        else:
            chosen = Section.objects.filter(id=request.session['selectedsection']).first()
            chosen.endTime= newEndTime
            chosen.save()
            return "End Time edited successfully!"

    if 'type' in request.POST:
        newType = request.POST['type']
        if func_ValidateSectionType(newType) == False:
            return "Invalid Type. Must be lecture, section, or grader."
        else:
            chosen = Section.objects.filter(id=request.session['selectedsection']).first()
            chosen.type= newType
            chosen.save()
            return "Type edited successfully!"

def func_DeleteSection(request):
    Section.objects.filter(id=request.session['selectedsection']).first().delete()
"""
MyUser validator functions used when creating or editing MyUser objects
"""
def func_ValidateEmail(email):
    return bool(re.fullmatch(r"[^@\s.]{1,12}@uwm\.edu", email))

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
    s = streetAddress.split()

    if len(s) < 3 or len(streetAddress) > 50:
        return False
    else:
        return True

def func_ValidateCity(city):
    if not city[0].isupper():
        return False
    pattern = re.compile(r'^[a-zA-Z\s]{2,20}$')
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
    return isinstance(zip, int) and 10000 <= zip <= 99999
def func_ValidateRole(role):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("instructor", "Instructor"),
        ("ta", "TA")
    ]
    return any(role in choice for choice in ROLE_CHOICES)
"""
Course validator functions used when creating or editing Course objects
"""
def func_ValidateCourseName(name):
    if not isinstance(name, str):
        return False
    if name == '':
        return False
    if (all(c.isalpha() or c.isspace() for c in name)):
        if (name[-1].isspace() or name[0].isspace()):
            return False
        else:
            if name.strip().count('  ')+1 == len(name.split()):
                if name.isalpha():
                    return True
                else:
                    return False
            else:
                return True
    else:
        return False
def func_ValidateDepartment(department):
    if not isinstance(department, str):
        return False
    if department == '':
        return False
    if (all(c.isalpha() or c.isspace() for c in department)):
        if (department[-1].isspace() or department[0].isspace()):
            return False
        else:
            if department.strip().count('  ') + 1 == len(department.split()):
                if department.isupper():
                    return True
                else:
                    return False
            else:
                return True
    else:
        return False
def func_ValidateCourseNumber(courseNumber, department):
    if isinstance(courseNumber, int):
        if courseNumber < 99 or courseNumber > 999:
            return False
        if (Course.objects.filter(courseNumber=courseNumber).first() == None):
            return True
        else:
            for course in Course.objects.filter(courseNumber=courseNumber):
                if course.department == department:
                    return False
            return True

    else:
        return False
def func_ValidateSemester(semester):
    if semester == 'fall' or semester == 'winter' or semester == 'spring' or semester == 'summer':
        return True
    else:
        return False
def func_ValidateYear(year):
    if isinstance(year, int):
        if year < 1955 or year > 2026:
            return False
        else:
            return True
    else:
        return False
"""
Section validator functions used when creating or editing Section objects
"""
def func_ValidateSectionNumber(sectionNumber, courseID):
    if isinstance(sectionNumber, int):
        if sectionNumber < 99 or sectionNumber > 999:
            return False
        if(Section.objects.filter(sectionNumber=sectionNumber).first() == None):
            return True
        else:
            for section in Section.objects.filter(sectionNumber=sectionNumber):
                if section.course == Course.objects.get(id=courseID):
                    return False
            return True

    else:
        return False
def func_ValidateLocation(location):
    if not isinstance(location, str):
        return False
    location_pattern = "^([A-Z]?)(\\d{1,})([A-Z]?) [a-zA-Z0-9\\s]"
    match = re.match(location_pattern, location)
    if (match != None):
        if (location[-1].isspace()  ):
            return False
        else:
            if location.count('  ')==0:
                return True
            else:
                return False
    else:
        if location == "Online":
            return True
        else:
            return False
def func_ValidateDaysMeeting(daysMeeting):
    order = {
        'M':0,
        'T': 1,
        'W': 2,
        'H': 3,
        'F': 4,
        'S': 5,
        'U': 6,
        'A': -1,
    }
    if not isinstance(daysMeeting, str):
        return False
    if daysMeeting == "A":
        return True
    else:
        if daysMeeting == '':
            return False
        else:
            for index in range(0, len(daysMeeting)):
                current = order.get(daysMeeting[index])
                if index+1 == len(daysMeeting):
                    return True
                next = order.get(daysMeeting[index+1])
                if next <= current:
                    return False

def func_ValidateStartAndEndTime(startTime, endTime):
    if not isinstance(startTime, str) or not isinstance(endTime,str):
        return False
    if startTime == endTime:
        return False
    time_pattern = "([01]?[0-9]|2[0-3]):[0-5][0-9]"
    matchStart = re.match(time_pattern, startTime)
    matchEnd = re.match(time_pattern, endTime)
    if matchStart != None and matchEnd != None:
        startSplit = startTime.split(':')
        endSplit = endTime.split(':')
        startHour = int(startSplit[0])
        startMin = int(startSplit[1])
        endHour = int(endSplit[0])
        endMin = int(endSplit[1])
        if startHour < 8:
            return False
        if startHour > 17:
            return False
        if endHour > 19:
            return False
        if startHour > endHour:
            return False
        if startHour == endHour:
            if endMin < startMin:
                return False
        return True
    else:
        return False

def func_ValidateSectionType(type):
    if type == 'lecture' or type == 'grader' or type == 'lab':
        return True
    else:
        return False
