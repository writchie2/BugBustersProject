from django.shortcuts import render, redirect
from django.views import View

from .Model_Classes.Course_Functions import func_CourseCreator, func_EditCourseName, func_EditDepartment, \
    func_EditCourseNumber, \
    func_EditSemester, func_EditYear, func_CourseDeleter, func_AssignUserToCourse, func_RemoveCourseUser, \
    func_UserIsInstructorOfCourse
from .Model_Classes.MyUser_Functions import func_MyUserCreator, func_EditFirstName, func_EditLastName, \
    func_EditPhoneNumber, \
    func_EditStreetAddress, func_EditCity, func_EditState, func_EditZipcode, func_EditRole, func_MyUserDeleter, \
    func_SaveBio
from .Model_Classes.Section_Functions import func_SectionCreator, func_EditSectionNumber, func_EditLocation, \
    func_EditDaysMeeting, func_EditStartTime, func_EditEndTime, func_EditType, func_SectionDeleter, \
    func_AssignUserToSection, func_RemoveSectionUser

from SchedulingApp.Model_Classes.Template_Dicts_Functions import func_UserAsDict, func_AlphabeticalMyUserList, func_AscendingSectionList, func_AlphabeticalCourseList, func_SectionAsDict, func_CourseAsDict
from .models import Section, MyUser, Course





class Login(View):
    def get(self, request):
        if "email" and "role" in request.session:
            return redirect('/dashboard/')
        else:
            request.session.flush()
        return render(request, "login.html")

    def post(self, request):
        if "email" and "password" in request.POST:
            message = self.login(request)
            if message == "success":
                return redirect("/dashboard/")
            else:
                return render(request, "login.html", {"message": message})

    def login(self, request):
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
            request.session["email"] = user.email
            request.session["role"] = user.role
            return "success"


class Dashboard(View):
    def get(self, request):
        if "email" and "role" in request.session:
            return render(request, "dashboard.html", {"user":func_UserAsDict(request.session['email'])})
        else:
            return redirect("/")

    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')

        if request.POST['navigation'] == "logout":
            request.session.flush()
            return redirect("/")
        if request.POST['navigation'] == "viewself":
            request.session["selecteduser"] = request.session["email"]
            return redirect("/userpage/")
        if request.POST['navigation'] == "courselist":
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            return redirect("/directory/")
        if request.POST['navigation'] == "dashboard":
            return redirect("/dashboard/")


class Directory(View):
    def get(self, request):
        if "email" and "role" in request.session:
            sortedUsers = func_AlphabeticalMyUserList(MyUser.objects.all())
            return render(request, "directory.html", {"list": sortedUsers, "role": request.session['role']})
        else:
            return redirect("/")


    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "createuser":
                if request.session['role'] != 'admin':
                    return render(request, "directory.html", {"message": "Only admins can create users!"})
                else:
                    return redirect("/createuser/")
        if 'selecteduser' in request.POST:
            request.session["selecteduser"] = request.POST['selecteduser']
            return redirect("/userpage/")


class UserPage(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selecteduser' in request.session:
                return render(request, "userpage.html",
                      {"user": func_UserAsDict(request.session['selecteduser']),
                       "role": request.session['role'],
                       'ownpage': request.session['selecteduser'] == request.session['email'],
                       'editbio': 'False'})
            else:
                return redirect("/directory/")
        else:
            return redirect("/")

    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "edituser":
                if request.session['role'] != 'admin' and request.session['email'] != request.session['selecteduser']:
                    return render(request, "userpage.html", {"message": "Only admins can edit users!","user": func_UserAsDict(request.session['selecteduser'])})
                else:
                    return redirect("/edituser/")
            if request.POST['navigation'] == "deleteuser":
                message = self.deleteUser(request)
                if message == "User successfully deleted":
                    del request.session["selecteduser"]
                    return redirect("/directory/")
                else:
                    return render(request, "userpage.html", {"message": message,
                                                             "user": func_UserAsDict(
                                                                 request.session['selecteduser'])})
        if 'editbio' in request.POST:
            if request.POST['editbio'] == "True":
                return render(request, "userpage.html",
                              {"user": func_UserAsDict(request.session['selecteduser']),
                               "role": request.session['role'],
                               'ownpage': request.session['selecteduser'] == request.session['email'],
                               'editbio': 'True'})
        if 'savebio' in request.POST:
            func_SaveBio(request.session['selecteduser'], request.POST['savebio'] )
            return redirect('/userpage/')

    def deleteUser(self, request):
        if request.session['role'] != 'admin':
            return "Only admins can delete users!"
        return func_MyUserDeleter(request.session['selecteduser'])


class CreateUser(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if request.session['role'] != "admin":
                 return redirect("/directory/")
            else:
                return render(request, "createuser.html",)
        else:
            return redirect("/")
    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/directory/")

        message = self.createUser(request)
        return render(request, "createuser.html", {"message": message})

    def createUser(self, request):
        if (
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
        zip = request.POST["zipcode"]
        role = request.POST["role"]
        return func_MyUserCreator(email, pw, pwc, first, last, phone, street, city, state, zip, role)



class EditUser(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selecteduser' not in request.session:
                return redirect("/directory/")
            if request.session['role'] != "admin" and request.session['selecteduser'] != request.session['email']:
                return redirect("/directory/")
            else:
                return render(request, "edituser.html",{"user": func_UserAsDict(request.session['selecteduser']), 'role': request.session['role']})
        else:
            return redirect("/")

    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/userpage/")
        message = self.editUser(request)
        return render(request, "edituser.html", {"user": func_UserAsDict(request.session['selecteduser']), "message": message, 'role': request.session['role']})

    def editUser(self, request):
        if 'firstname' in request.POST:
            return func_EditFirstName(request.POST['firstname'], request.session['selecteduser'])
        if 'lastname' in request.POST:
            return func_EditLastName(request.POST['lastname'], request.session['selecteduser'])
        if 'phonenumber' in request.POST:
            return func_EditPhoneNumber(request.POST['phonenumber'], request.session['selecteduser'])
        if 'streetaddress' in request.POST:
            return func_EditStreetAddress(request.POST['streetaddress'], request.session['selecteduser'])
        if 'city' in request.POST:
            return func_EditCity(request.POST['city'], request.session['selecteduser'])
        if 'state' in request.POST:
            return func_EditState(request.POST['state'], request.session['selecteduser'])
        if 'zipcode' in request.POST:
            return func_EditZipcode(request.POST['zipcode'], request.session['selecteduser'])
        if 'role' in request.POST:
            return func_EditRole(request.POST['role'], request.session['selecteduser'])



class CourseList(View):
    def get(self, request):
        if "email" and "role" in request.session:
            sortedCourses = func_AlphabeticalCourseList(Course.objects.all())
            return render(request, "courselist.html", {"list": sortedCourses, "role": request.session['role']})
        else:
            return redirect("/")


    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "createcourse":
                if request.session['role'] != 'admin':
                    return render(request, "courselist.html", {"message": "Only admins can create courses!"})
                else:
                    return redirect("/createcourse/")
        if 'selectedcourse' in request.POST:
            request.session["selectedcourse"] = request.POST['selectedcourse']
            return redirect("/coursepage/")


class CoursePage(View):
    def get(self, request):
        if "email" and "role" in request.session:

            if 'selectedcourse' in request.session:
                return render(request, "coursepage.html",
                          {"course": func_CourseAsDict(request.session['selectedcourse']),
                           "role": request.session['role'],
                           'unassignedusers': func_AlphabeticalMyUserList(MyUser.objects.exclude(course=request.session['selectedcourse']))})
            else:
                return redirect("/courselist/")
        else:
            return redirect("/")

    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "createsection":
                if request.session['role'] != 'admin':
                    return render(request, "coursepage.html", {"message": "Only admins can create sections!"})
                else:
                    return redirect("/createsection/")
            if request.POST['navigation'] == "editcourse":
                if request.session['role'] != 'admin':
                    return render(request, "coursepage.html", {"message": "Only admins can edit courses!",
                                                             "course": func_CourseAsDict(request.session['selectedcourse'])})
                else:
                    return redirect("/editcourse/")
            if request.POST['navigation'] == "deletecourse":
                message = self.deleteCourse(request)
                if message == "Course deleted successfully":
                    del request.session["selectedcourse"]
                    return redirect("/courselist/")
                else:
                    return render(request, "coursepage.html", {"message": message,
                                                               "course": func_CourseAsDict(
                                                                   request.session['selectedcourse'])})
        if 'selectedsection' in request.POST:
            request.session["selectedsection"] = request.POST['selectedsection']
            return redirect("/sectionpage/")
        if 'selecteduser' in request.POST:
            request.session['selecteduser'] = request.POST['selecteduser']
            return redirect('/userpage/')

        if 'adduser' in request.POST:
                message = self.addUserToCourse(request)
                return render(request, "coursepage.html",
                              {"course": func_CourseAsDict(request.session['selectedcourse']),
                               "role": request.session['role'],
                               'unassignedusers': func_AlphabeticalMyUserList(
                                   MyUser.objects.exclude(course=request.session['selectedcourse'])),
                               'message': message})
        if 'removeuser' in request.POST:
            message = self.removeUserFromCourse(request)
            return render(request, "coursepage.html",
                          {"course": func_CourseAsDict(request.session['selectedcourse']),
                           "role": request.session['role'],
                           'unassignedusers': func_AlphabeticalMyUserList(
                               MyUser.objects.exclude(course=request.session['selectedcourse'])),
                           'message': message})

    def deleteCourse(self, request):
        if request.session['role'] != 'admin':
            return "Only admins can delete courses!"
        else:
            return func_CourseDeleter(request.session['selectedcourse'])

    def addUserToCourse(self, request):
        if request.session['role'] != 'admin':
            return "Only admins can add users to courses!"
        return func_AssignUserToCourse(request.POST['adduser'],request.session['selectedcourse'])

    def removeUserFromCourse(self, request):
        if request.session['role'] != 'admin':
            return "Only admins can remove users from courses!"
        return func_RemoveCourseUser(request.POST['removeuser'], request.session['selectedcourse'])




class CreateCourse(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if request.session['role'] != "admin":
                return redirect("/courselist/")
            else:
                return render(request, "createcourse.html", )
        else:
            return redirect("/")

    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/coursepage/")

        message = self.createCourse(request)
        return render(request, "createcourse.html", {"message": message})

    def createCourse(self, request):
        if ('coursename' not in request.POST or 'department' not in request.POST or
                'coursenumber' not in request.POST
                or 'semester' not in request.POST or 'year' not in request.POST):
            return "Please fill out all fields!"
        newCourseName = request.POST['coursename']
        newCourseDepartment = request.POST['department']
        newCourseNumber = int(request.POST['coursenumber'])
        newCourseSemester = request.POST['semester']
        newCourseYear = int(request.POST['year'])
        message = func_CourseCreator(newCourseName, newCourseDepartment, newCourseNumber, newCourseSemester,
                                     newCourseYear)
        return message



class EditCourse(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if request.session['role'] != "admin" or 'selectedcourse' not in request.session:
                return redirect("/courselist/")
            else:
                return render(request, "editcourse.html", {"course": func_CourseAsDict(request.session['selectedcourse'])})
        else:
            return redirect("/")


    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/coursepage/")

        message = self.editCourse(request)
        return render(request, "editcourse.html",
                  {"course": func_CourseAsDict(request.session['selectedcourse']), "message": message})

    def editCourse(self, request):
        chosen = Course.objects.filter(id=request.session['selectedcourse']).first()
        if 'coursename' in request.POST:
            return func_EditCourseName(request.POST["coursename"], request.session['selectedcourse'])

        if 'department' in request.POST:
            return func_EditDepartment(request.POST["department"], request.session['selectedcourse'])

        if 'coursenumber' in request.POST:
            return func_EditCourseNumber(int(request.POST["coursenumber"]), request.session['selectedcourse'])

        if 'semester' in request.POST:
            return func_EditSemester(request.POST["semester"], request.session['selectedcourse'])

        if 'year' in request.POST:
            return func_EditYear(int(request.POST["year"]), request.session['selectedcourse'])


class SectionPage(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selectedsection' in request.session:
                return render(request, "sectionpage.html",
                          {"section": func_SectionAsDict(request.session['selectedsection']),
                           "role": request.session['role'],
                           'unassignedusers': func_AlphabeticalMyUserList(MyUser.objects.filter(course=request.session['selectedcourse']))})
            else:
                return redirect("/coursepage/")
        else:
            return redirect("/")
    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "viewcourse":
                return redirect("/coursepage/")
            if request.POST['navigation'] == "editsection":
                if request.session['role'] != 'admin':
                    return render(request, "sectionpage.html", {"message": "Only admins can edit sections!","section": func_SectionAsDict(request.session['selectedsection'])})
                else:
                    return redirect("/editsection/")
            if request.POST['navigation'] == "deletesection":
                message = self.deleteSection(request)
                if message == "Section deleted successfully":
                    del request.session["selectedsection"]
                    return redirect("/coursepage/")
                else:
                    return render(request, "sectionpage.html", {"message": message,
                                                                "user": func_SectionAsDict(
                                                                    request.session['selectedsection'])})

        if 'adduser' in request.POST:
            message = self.addUserToSection(request)
            return render(request, "sectionpage.html",
                          {"section": func_SectionAsDict(request.session['selectedsection']),
                           "role": request.session['role'],
                           'unassignedusers': func_AlphabeticalMyUserList(
                               MyUser.objects.filter(course=request.session['selectedcourse'])),
                           'message': message})
        if 'removeuser' in request.POST:
            message = self.removeUserFromSection(request)
            return render(request, "sectionpage.html",
                          {"section": func_SectionAsDict(request.session['selectedsection']),
                           "role": request.session['role'],
                           'unassignedusers': func_AlphabeticalMyUserList(
                               MyUser.objects.filter(course=request.session['selectedcourse'])),
                           'message': message})
        if 'selecteduser' in request.POST:
            request.session['selecteduser'] = request.POST['selecteduser']
            return redirect('/userpage/')

    def deleteSection(self, request):
        if request.session['role'] != 'admin':
            return "Only admins can delete sections!"
        else:
            return func_SectionDeleter(request.session['selectedsection'])

    def addUserToSection(self, request):
        if request.session['role'] != 'admin' and not func_UserIsInstructorOfCourse(request.session['email'], request.session['selectedcourse']) == "True":
            return "Only admins or instructors of the course can add users to sections!"
        else:
            return func_AssignUserToSection(request.POST['adduser'], request.session['selectedsection'])

    def removeUserFromSection(self, request):
        if request.session['role'] != 'admin' and not func_UserIsInstructorOfCourse(request.session['email'], request.session['selectedcourse']) == "True":
            return "Only admins or instructors of the course can remove users from sections! "
        else:
            return func_RemoveSectionUser(request.POST['adduser'], request.session['selectedsection'])

class CreateSection(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if request.session['role'] != "admin":
                return redirect("/coursepage/")
            else:
                return render(request, "createsection.html", )
        else:
            return redirect("/")

    def post(self, request):
        if 'navigation' in request.POST:
            if 'email' not in request.session:
                return redirect('/')
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/coursepage/")

        message = self.createSection(request)
        return render(request, "createsection.html", {"message": message})

    def createSection(self, request):
        if ('sectionnumber' not in request.POST or 'location' not in request.POST or
                'starttime' not in request.POST
                or 'endtime' not in request.POST or 'type' not in request.POST):
            return "Please fill out all fields!"
        newSectionNumber = int(request.POST["sectionnumber"])
        newLocation = request.POST["location"]
        newDaysMeeting = ''
        for days in request.POST.getlist('daysmeeting'):
            newDaysMeeting += days
        newStartTime = request.POST["starttime"]
        newEndTime = request.POST["endtime"]
        newType = request.POST['type']
        return func_SectionCreator(newSectionNumber, request.session['selectedcourse'], newDaysMeeting, newLocation,
                                   newType,
                                   newStartTime, newEndTime)

class EditSection(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if request.session['role'] != "admin" or 'selectedsection' not in request.session:
                return redirect("/sectionpage/")
            else:
                return render(request, "editsection.html", {"section": func_SectionAsDict(request.session['selectedsection'])})
        else:
            return redirect("/")
    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                request.session.flush()
                return redirect("/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect('/sectionpage/')
        message = self.editSection(request)
        return render(request, "editsection.html",
                      {"section": func_SectionAsDict(request.session['selectedsection']), "message": message})

    def editSection(self, request):
        chosen = Section.objects.filter(id=request.session['selectedsection']).first()
        if 'sectionnumber' in request.POST:
            return func_EditSectionNumber(int(request.POST["sectionnumber"]), request.session['selectedsection'])

        if 'location' in request.POST:
            return func_EditLocation(request.POST["location"], request.session['selectedsection'])

        if 'daysmeeting' in request.POST:
            newDaysMeeting = ''
            for days in request.POST.getlist('daysmeeting'):
                newDaysMeeting += days
            return func_EditDaysMeeting(newDaysMeeting, request.session['selectedsection'])

        if 'starttime' in request.POST:
            return func_EditStartTime(request.POST["starttime"], request.session['selectedsection'])

        if 'endtime' in request.POST:
            return func_EditEndTime(request.POST["endtime"], request.session['selectedsection'])

        if 'type' in request.POST:
            return func_EditType(request.POST['type'], request.session['selectedsection'])

