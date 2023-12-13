from operator import itemgetter

from SchedulingApp.models import MyUser, Course, Section


def func_CourseCreator(coursename, department, number, semester, year):
    if func_ValidateCourseName(coursename) == False:
        return "Invalid Course Name. Only letters and single spaces are allowed."
    if func_ValidateDepartment(department) == False:
        return "Invalid Department. All Departments come from the UWM course cataloge."
    if func_ValidateCourseNumber(number,department) == False:
        return "Invalid Course Number. Must be between 100 and 999 and unique."
    if func_ValidateSemester(semester) == False:
        return "Invalid Semester. Acceptable values are fall, spring, winter, and summer"
    if func_ValidateYear(year) == False:
        return "Invalid Year. Must be later than 1956 and cannot be greater than 2025"
    newCourse = Course.objects.create(name=coursename, department=department,
                                      courseNumber=number, semester=semester,
                                      year=year)
    newCourse.save()
    return "Course created successfully!"

def func_AssignUserToCourse(user_email, courseID):
    try:
        user = MyUser.objects.get(email=user_email)
    except:
        return "User does not exist!"

    try:
        course = Course.objects.get(id=courseID)
    except:
        return "This course does not exist!"
    if course in user.course_set.all():
        return "User is already in the course!"
    course.assignedUser.add(user)
    course.save()
    return "User added successfully!"

def func_RemoveCourseUser(user_email, courseID):
    try:
        user = MyUser.objects.get(email=user_email)
    except:
        return "User does not exist!"

    try:
        course = Course.objects.get(id=courseID)
    except:
        return "This course does not exist!"
    if not course in user.course_set.all():
        return "User is not in the course!"
    course.assignedUser.remove(user)
    course.save()
    return "User removed successfully!"

def func_UserIsInstructorOfCourse(user_email, courseID):
    try:
        user = MyUser.objects.get(email=user_email)
    except:
        return "User does not exist!"
    try:
        course = Course.objects.get(id=courseID)
    except:
        return "This course does not exist!"
    if user.role == 'instructor' and course in user.course_set.all():
        return "True"
    else:
        return "False"
def func_EditCourseName(coursename, courseID):
    try:
        chosen = Course.objects.get(id=courseID)
    except:
        return "Course does not exist!"
    if func_ValidateCourseName(coursename):
        chosen.name = coursename
        chosen.save()
        return "Course Name edited successfully!"
    else:
        return "Invalid Course Name. Only letters and single spaces are allowed."


def func_EditDepartment(department, courseID):
    try:
        chosen = Course.objects.get(id=courseID)
    except:
        return "Course does not exist!"
    if func_ValidateDepartment(department):
        chosen.department = department
        chosen.save()
        return "Department edited successfully!"
    else:
        return "Invalid Department. All Departments come from the UWM course cataloge."


def func_EditCourseNumber(coursenumber, courseID):
    try:
        chosen = Course.objects.get(id=courseID)
    except:
        return "Course does not exist!"
    if func_ValidateCourseNumber(coursenumber, chosen.department):
        chosen.courseNumber = coursenumber
        chosen.save()
        return "Course Number edited successfully!"
    else:
        return "Invalid Course Number. Must be between 100 and 999 and unique."


def func_EditSemester(semester, courseID):
    try:
        chosen = Course.objects.get(id=courseID)
    except:
        return "Course does not exist!"
    if func_ValidateSemester(semester):
        chosen.semester = semester
        chosen.save()
        return "Semester edited successfully!"
    else:
        return "Invalid Semester. Acceptable values are fall, spring, winter, and summer"

def func_EditYear(year, courseID):
    try:
        chosen = Course.objects.get(id=courseID)
    except:
        return "Course does not exist!"
    if func_ValidateYear(year):
        chosen.year = year
        chosen.save()
        return "Year edited successfully!"
    else:
        return "Invalid Year. Must be later than 1956 and cannot be greater than 2025"

def func_CourseDeleter(courseID):
    try:
        course = Course.objects.get(id=courseID)
    except:
        return "Course does not exist!"
    course.delete()
    return "Course deleted successfully"
"""
Input: string - a name.
Output: True if it is capatalized, has no spaces, and only contains letters. False otherwise.
"""

def func_ValidateCourseName(name):
    if not isinstance(name, str):
        return False
    if name == '':
        return False
    if (all(c.isalpha() or c.isspace() or c == '\'' for c in name)):
        if (name[-1].isspace() or name[0].isspace() or name[0].islower()):
            return False
        else:
            if name.strip().count('  ') + 1 == len(name.split()):
                if name.isalpha():
                    return True
                else:
                    return False
            else:
                return True
    else:
        return False

"""
Input: string - a department.
Output: True if it is one of UWM departments. False otherwise.
"""

def func_ValidateDepartment(department):
    if not isinstance(department, str):
        return False
    dept_list = ['AMLLC', 'ACTSCI', 'AD LDSP', 'AFAS', 'AFRIC', 'AIS', 'ANTHRO', 'ARABIC',
                 'ARCH', 'ART', 'ART ED', 'ARTHIST', 'ASTRON', 'ATM SCI', 'ATRAIN', 'BIO SCI',
                 'BME', 'BMS', 'BUS ADM', 'BUSMGMT', 'CELTIC', 'CES', 'CGS AIS', 'CGS ANT',
                 'CGS ART', 'CGS AST', 'CGS BIO', 'CGS BUS', 'CGS CHE', 'CGS CPS', 'CGS CTA',
                 'CGS ECO', 'CGS EDU', 'CGS EGR', 'CGS ENG', 'CGS ESL', 'CGS FRE', 'CGS GEO',
                 'CGS GER', 'CGS GLG', 'CGS GSW', 'CGS HES', 'CGS HIS', 'CGS INT', 'CGS IST',
                 'CGS ITA', 'CGS LEA', 'CGS LEA', 'CGS LEC', 'CGS MAT', 'CGS MLG', 'CGS MUA',
                 'CGS MUS', 'CGS PHI', 'CGS PHY', 'CGS POL', 'CGS PSY', 'CGS REL', 'CGS SOC',
                 'CGS SPA', 'CHEM', 'CHINESE', 'CHS', 'CIV ENG', 'CLASSIC', 'COMMUN', 'COMPLIT',
                 'COMPSCI', 'COMPST', 'COMSDIS', 'COUNS', 'CRM JST', 'CURRINS', 'DAC', 'DANCE',
                 'DMI', 'EAP', 'EAS', 'ECON', 'ED POL', 'ED PSY', 'EDUC', 'ELECENG', 'ENGLISH',
                 'ETHNIC', 'EXCEDUC', 'FILM', 'FILMSTD', 'FINEART', 'FOODBEV', 'FRENCH',
                 'FRSHWTR', 'GEO SCI', 'GEOG', 'GERMAN', 'GLOBAL', 'GARD', 'GREEK', 'HCA',
                 'HEBREW', 'HI', 'HIST', 'HMONG', 'HONORS', 'HS', 'IEP', 'IND ENG', 'IND REL',
                 'INFOST', 'INTLST', 'ITALIAN', 'JAMS', 'JAPAN', 'JEWISH', 'KIN', 'KOREAN',
                 'L&S HUM', 'L&S NS', 'L&S SS', 'LACS', 'LACUSL', 'LATIN', 'LATINX', 'LGBT',
                 'LIBRLST', 'LINGUIS', 'MALLT', 'MATH', 'MATLENG', 'MECHENG', 'MIL SCI',
                 'MSP', 'MTHSTAT', 'MUS ED', 'MUSIC', 'MUSPERF', 'MEURO', 'NONPROF', 'NURS',
                 'OCCTHPY', 'PEACEST', 'PH', 'PHILOS', 'PHYSICS', 'POL SCI', 'POLISH', 'PORTUGS',
                 'PRPP', 'PSYCH', 'PT', 'PUB ADM', 'RELIGST', 'RUSSIAN', 'SCNDVST', 'SOC WRK',
                 'SOCIOL', 'SPANISH', 'SPT&REC', 'TCH LRN', 'THEATRE', 'THERREC', 'TRNSLTN', 'URB STD',
                 'URBPLAN', 'UWS NSG', 'UWX', 'WGS']
    return department in dept_list

"""
Input: int, string - course number and a department.
Output: True the course number has 3 digits and no other course with 
that number exists in the department. If all conditions met returns True. Otherwise False otherwise.
"""

def func_ValidateCourseNumber(courseNumber, department):

    if isinstance(courseNumber, int) and func_ValidateDepartment(department):
        if courseNumber < 100 or courseNumber > 999:
            return False
        if Course.objects.filter(courseNumber=courseNumber).first() == None:
            return True
        else:
            for course in Course.objects.filter(courseNumber=courseNumber):
                if course.department == department:
                    return False
            return True

    else:
        return False

"""
Input: string - a semester.
Output: True 'fall', 'winter', 'spring' or 'summer'. False otherwise.
"""

def func_ValidateSemester(semester):
    if semester == 'fall' or semester == 'winter' or semester == 'spring' or semester == 'summer':
        return True
    else:
        return False

"""
Input: int - a year.
Output: True if between 1957 and 2025. False otherwise.
"""

def func_ValidateYear(year):
    if isinstance(year, int):
        if year < 1957 or year > 2025:
            return False
        else:
            return True
    else:
        return False

