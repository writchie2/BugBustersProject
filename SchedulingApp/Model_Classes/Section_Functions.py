import time
import re
from operator import itemgetter


from SchedulingApp.models import Course, Section, MyUser


def func_SectionCreator(number, courseID, days, location, type, starttime, endtime):
    if func_ValidateSectionNumber(number, courseID) == False:
        return "Invalid Section Number. Must be between 100 and 999 and unique!"
    if func_ValidateDaysMeeting(days) == False:
        return "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days."
    if func_ValidateLocation(location) == False:
        return "Invalid Location. Format: Room# Building Name"
    if func_ValidateSectionType(type) == False:
        return "Invalid Type. Must be lecture, lab, or grader."
    if func_ValidateStartAndEndTime(starttime, endtime) == False:
        return "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end."
    try:
        course = Course.objects.get(id=courseID)
    except:
        return "Course does not exist!"
    newSection = Section.objects.create(sectionNumber=number, type=type,
                                        location=location, daysMeeting=days,
                                        startTime=starttime, endTime=endtime,
                                        course=course)
    newSection.save()
    return "Section created successfully!"

def func_AssignUserToSection(email, sectionID):
    try:
        user_added = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    try:
        section = Section.objects.get(id=sectionID)
    except:
        return "Section does not exist!"
    if user_added not in section.course.assignedUser.all():
        return "That user is not in this course!"
    if section.assignedUser == user_added:
        return "User is already assigned to the section!"
    if section.assignedUser != None:
        return "There is already someone assigned to the section!"
    section.assignedUser = user_added
    section.save()
    return "User added successfully!"

def func_RemoveSectionUser(email, sectionID):
    try:
        user_removed = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    try:
        section = Section.objects.get(id=sectionID)
    except:
        return "Section does not exist!"
    if section.assignedUser != user_removed:
        return "User is not assigned to the section!"
    if section.assignedUser == None:
        return "There is nobody assigned to the section!"
    section.assignedUser = None
    section.save()
    return "User removed successfully!"
def func_EditSectionNumber(number, sectionID):
    try:
        chosen = Section.objects.get(id=sectionID)
    except:
        return "Section does not exist!"
    if func_ValidateSectionNumber(number, chosen.course) == False:
        return "Invalid Section Number. Must be between 100 and 999 and unique!"
    else:
        chosen = Section.objects.filter(id=sectionID).first()
        chosen.sectionNumber = number
        chosen.save()
        return "Section Number edited successfully!"


def func_EditLocation(location, sectionID):
    try:
        chosen = Section.objects.get(id=sectionID)
    except:
        return "Section does not exist!"
    if func_ValidateLocation(location):
        chosen.location = location
        chosen.save()
        return "Location edited successfully!"
    else:
        return "Invalid Location. Format: Room# Building Name"


def func_EditDaysMeeting(days, sectionID):
    try:
        chosen = Section.objects.get(id=sectionID)
    except:
        return "Section does not exist!"
    if func_ValidateDaysMeeting(days):
        chosen.daysMeeting = days
        chosen.save()
        return "Days Meeting edited successfully!"
    else:
        return "Invalid Days Meeting. Must be in order MTWHFSU, 'No Meeting Pattern' cannot be selected with other days."


def func_EditStartTime(starttime, sectionID):
    try:
        chosen = Section.objects.get(id=sectionID)
    except:
        return "Section does not exist!"
    if func_ValidateStartAndEndTime(starttime, chosen.endTime):
        chosen.startTime = starttime
        chosen.save()
        return "Start Time edited successfully!"
    else:
        return "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end."


def func_EditEndTime(endtime, sectionID):
    try:
        chosen = Section.objects.get(id=sectionID)
    except:
        return "Section does not exist!"
    if func_ValidateStartAndEndTime(chosen.startTime, endtime):
        chosen.endTime = endtime
        chosen.save()
        return "End Time edited successfully!"
    else:
        return "Invalid Start/End Time. Sections cannot start before 8am, cannot start after 6pm, and must end by 9pm. They also must start earlier than they end."


def func_EditType(type, sectionID):
    try:
        chosen = Section.objects.get(id=sectionID)
    except:
        return "Section does not exist!"
    if func_ValidateSectionType(type):
        chosen.type = type
        chosen.save()
        return "Type edited successfully!"
    else:
        return "Invalid Type. Must be lecture, lab, or grader."


def func_SectionDeleter(sectionID):
    try:
        section = Section.objects.get(id=sectionID)
    except:
        return "Section does not exist!"
    section.delete()
    return "Section deleted successfully"
"""
Input: int, int - section number and course id.
Output: True the section number has 3 digits and no other section with 
that number exists in the course. If all conditions met returns True. Otherwise False otherwise.
"""

def func_ValidateSectionNumber(sectionNumber, courseID):
    if isinstance(sectionNumber, int):
        if sectionNumber < 100 or sectionNumber > 999:
            return False
        if (Section.objects.filter(sectionNumber=sectionNumber).first() == None):
            return True
        else:
            for section in Section.objects.filter(sectionNumber=sectionNumber):
                if section.course == Course.objects.get(id=courseID):
                    return False
            return True

    else:
        return False

"""
Input: string - a location.
Output: True in the format #### Building Name. Room numbers need to be at least 1 digit and can
 start or end with a letter (i.e. S195). If all conditions met returns True. Otherwise False otherwise.
"""

def func_ValidateLocation(location):
    if not isinstance(location, str):
        return False
    location_pattern = "^([A-Z]?)(\\d{1,})([A-Z]?) [a-zA-Z0-9\\s]"
    match = re.match(location_pattern, location)
    if (match != None):
        if (location[-1].isspace()):
            return False
        else:
            if location.count('  ') == 0:
                return True
            else:
                return False
    else:
        if location == "Online":
            return True
        else:
            return False

"""
Input: string - Days the section meet.
Output: True if in chronological order (i.e. M before T).
'A' represent Asynchronous and cannot be in a string with any other days.
If all conditions met returns True. Otherwise False otherwise.
"""

def func_ValidateDaysMeeting(daysMeeting):
    order = {
        'M': 0,
        'T': 1,
        'W': 2,
        'H': 3,
        'F': 4,
        'S': 5,
        'U': 6,
        'A': -1,
    }
    valid = ['M', 'T', 'W', 'H', 'F', 'S', 'U', 'A']
    if not isinstance(daysMeeting, str):
        return False
    if daysMeeting == "A":
        return True
    else:
        if daysMeeting == '':
            return False
        else:
            for index in range(0, len(daysMeeting)):
                if not daysMeeting[index] in valid:
                    return False
                current = order.get(daysMeeting[index])
                if index + 1 == len(daysMeeting):
                    return True
                next = order.get(daysMeeting[index + 1])
                if next <= current:
                    return False

"""
Input: string, string - Start time and End Time for section.
Output: Start must be before end. Start must not be earlier than '08:00' and cannot be
later than '17:59' (5:59pm). End time cannot be later than '19:59' (7:59pm). If all 
conditions met returns True. Otherwise returns False.
"""

def func_ValidateStartAndEndTime(startTime, endTime):
    if not isinstance(startTime, str) or not isinstance(endTime, str):
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

"""
Input: string - a section type.
Output: True 'lecture', 'grader',or  'lab'. False otherwise.
"""

def func_ValidateSectionType(type):
    if type == 'lecture' or type == 'grader' or type == 'lab':
        return True
    else:
        return False

