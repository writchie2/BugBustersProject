import time
from operator import itemgetter

from SchedulingApp.models import Course, Section, MyUser


def func_CourseAsDict(courseID):
    if courseID is None or Course.objects.filter(id=courseID).first() is None:
        raise Exception("Course does not exist!")
    course = Course.objects.filter(id=courseID).first()
    dict = {
        "id": course.id,
        "title": course.__str__(),
        "name": course.name,
        "department": course.department,
        "coursenumber": course.courseNumber,
        "semester": course.semester.capitalize(),
        "year": course.year,
        "users": func_AlphabeticalMyUserList(MyUser.objects.filter(course__id=courseID)),
        "sections": func_AscendingSectionList(Section.objects.filter(course=courseID))
    }
    return dict

def func_SectionAsDict(sectionID):
    if sectionID is None or Section.objects.filter(id=sectionID).first() is None:
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
def func_UserAsDict(userEmail):
    if userEmail is None or MyUser.objects.filter(email=userEmail).first() is None:
        raise Exception("User does not exist!")
    user = MyUser.objects.filter(email=userEmail).first()

    my_courses = func_AlphabeticalCourseList(Course.objects.filter(assignedUser=user))
    if not my_courses:
        my_courses = None

    my_sections = func_AscendingSectionList(Section.objects.filter(assignedUser=user))
    if not my_sections:
        my_sections = None

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
        "fullname": user.__str__(),
        "bio": user.bio,
        "courses": my_courses,
        "sections": my_sections
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

def func_AlphabeticalCourseList(course_bin):
    courseList = []
    for course in course_bin:
        thisdict = {
            "title": course.__str__(),
            "id": course.id,
            "semester": course.semester.capitalize(),
            "year": course.year
        }
        courseList.append(thisdict)
    alphabetical = sorted(courseList, key=itemgetter('title'))
    return alphabetical
