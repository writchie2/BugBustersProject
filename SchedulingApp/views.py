from django.shortcuts import render, redirect
from django.views import View
from .models import Course, MyUser, Section
from django.http import HttpResponseRedirect


class Login(View):
    def get(self, request):
        return render(request, "login.HTML")

    def post(self, request):
        return redirect("/dashboard")


class Dashboard(View):
    def get(self, request):
        return render(request, "dashboard.html")

    def post(self, request):
        if request.POST['navigation'] == "logout":
            return redirect("/login/")
        if request.POST['navigation'] == "viewself":
            return redirect("/userpage/")
        if request.POST['navigation'] == "courselist":
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            return redirect("/directory/")
        if request.POST['navigation'] == "dashboard":
            return redirect("/dashboard/")


class Directory(View):
    def get(self, request):
        return render(request, "directory.html")

    def post(self, request):
        if request.POST['navigation'] == "logout":
            return redirect("/login/")
        if request.POST['navigation'] == "dashboard":
            return redirect("/dashboard/")
        if request.POST['navigation'] == "courselist":
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            return redirect("/directory/")
        if request.POST['navigation'] == "viewaccount":
            return redirect("/userpage/")
        if request.POST['navigation'] == "createuser":
            return redirect("/createuser/")


class UserPage(View):
    def get(self, request):
        return render(request, "userpage.html")

    def post(self, request):
        if request.POST['navigation'] == "logout":
            return redirect("/login/")
        if request.POST['navigation'] == "dashboard":
            return redirect("/dashboard/")
        if request.POST['navigation'] == "courselist":
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            return redirect("/directory/")
        if request.POST['navigation'] == "edituser":
            return redirect("/edituser/")
        if request.POST['navigation'] == "deleteuser":
            return redirect("/dashboard/")


class CreateUser(View):
    def get(self, request):
        return render(request, "createuser.html")

    def post(self, request):
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                return redirect("/login/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/coursepage/")

        return func_CreateUser(request)


class EditUser(View):
    def get(self, request):
        return render(request, "edituser.html")

    def post(self, request):
        if request.POST['navigation'] == "logout":
            return redirect("/login/")
        if request.POST['navigation'] == "dashboard":
            return redirect("/dashboard/")
        if request.POST['navigation'] == "courselist":
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            return redirect("/directory/")




class CourseList(View):
    def get(self, request):
        return render(request, "courselist.html")

    def post(self, request):
        if request.POST['navigation'] == "logout":
            return redirect("/login/")
        if request.POST['navigation'] == "dashboard":
            return redirect("/dashboard/")
        if request.POST['navigation'] == "courselist":
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            return redirect("/directory/")
        if request.POST['navigation'] == "createcourse":
            return redirect("/createcourse/")
        if request.POST['navigation'] == "coursepage":
            return redirect("/coursepage/")


class CoursePage(View):
    def get(self, request):
        return render(request, "coursepage.html")

    def post(self, request):
        if request.POST['navigation'] == "logout":
            return redirect("/login/")
        if request.POST['navigation'] == "dashboard":
            return redirect("/dashboard/")
        if request.POST['navigation'] == "courselist":
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            return redirect("/directory/")
        if request.POST['navigation'] == "createsection":
            return redirect("/createsection/")
        if request.POST['navigation'] == "sectionpage":
            return redirect("/sectionpage/")
        if request.POST['navigation'] == "deletecourse":
            return redirect("/courselist/")


class CreateCourse(View):
    def get(self, request):
        return render(request, "createcourse.html")

    def post(self, request):
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                return redirect("/login/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/coursepage/")

        return func_CreateCourse(request)


class EditCourse(View):
    def get(self, request):
        return render(request, "editcourse.html")

    def post(self, request):
        if request.POST['navigation'] == "logout":
            return redirect("/login/")
        if request.POST['navigation'] == "dashboard":
            return redirect("/dashboard/")
        if request.POST['navigation'] == "courselist":
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            return redirect("/directory/")


class SectionPage(View):
    def get(self, request):
        return render(request, "sectionpage.html")

    def post(self, request):
        if request.POST['navigation'] == "logout":
            return redirect("/login/")
        if request.POST['navigation'] == "dashboard":
            return redirect("/dashboard/")
        if request.POST['navigation'] == "courselist":
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            return redirect("/directory/")
        if request.POST['navigation'] == "viewcourse":
            return redirect("/coursepage/")
        if request.POST['navigation'] == "deletesection":
            return redirect("/coursepage/")


class CreateSection(View):
    def get(self, request):
        return render(request, "createsection.html")

    def post(self, request):
        if 'navigation' in request.POST:
            if request.POST['navigation'] == "logout":
                return redirect("/login/")
            if request.POST['navigation'] == "dashboard":
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/coursepage/")

        return func_CreateSection(request)


class EditSection(View):
    def get(self, request):
        return render(request, "editsection.html")

    def post(self, request):
        if request.POST['navigation'] == "logout":
            return redirect("/login/")
        if request.POST['navigation'] == "dashboard":
            return redirect("/dashboard/")
        if request.POST['navigation'] == "courselist":
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            return redirect("/directory/")

#Functions to impliment and create tests for
def func_CreateUser(request):
    return redirect("/login")
def func_EditUser(request):
    return redirect("/login")
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
def func_ValidateFirstName(firstName):
    pass
def func_ValidateLastName(lastName):
    pass
def func_ValidatePhoneNumber(phoneNumber):
    pass
def func_ValidateStreetAddress(streetAddress):
    pass
def func_ValidateCity(city):
    pass
def func_ValidateState(state):
    pass
def func_ValidateZipCode(state):
    pass
def func_ValidateCourseName(name):
    pass
def func_ValidateDepartment(department):
    pass
def func_ValidateCourseNumber(courseNumber):
    pass
def func_ValidateYear(year):
    pass
def func_ValidateSectionNumber(sectionNumber):
    pass
def func_ValidateLocation(location):
    pass
def func_ValidateDaysMeeting(daysMeeting):
    pass
def func_ValidateStartTime(startTime):
    pass
def func_ValidateEndTime(endTime):
    pass

