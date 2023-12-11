from django.shortcuts import render, redirect
from django.views import View
from .models import Section, MyUser, Course
from django.http import HttpResponseRedirect
from .functions import func_CreateUser, func_EditUser, func_DeleteUser, func_CreateCourse, func_EditCourse, func_DeleteCourse, func_CreateSection, func_EditSection, func_DeleteSection, func_Login, func_AlphabeticalMyUserList, func_UserAsDict, func_AlphabeticalCourseList, func_CourseAsDict, func_AscendingSectionList, func_SectionAsDict, func_RemoveUserFromCourse


class Login(View):
    def get(self, request):
        if "email" and "role" in request.session:
            return redirect('/dashboard/')
        else:
            request.session.flush()
        return render(request, "login.html")
#login
    def post(self, request):
        if "email" and "password" in request.POST:
            message = func_Login(request)
            if message =="success.":
                user = MyUser.objects.get(email=request.POST['email'])
                request.session["email"] = user.email
                request.session["role"] = user.role
                return redirect("/dashboard/")
            else:
                return render(request, "login.html", {"message": message})



class Dashboard(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selecteduser' in request.session:
                del request.session['selecteduser']
            if 'selectedcourse' in request.session:
                del request.session['selectedcourse']
            if 'selectedsection' in request.session:
                del request.session['selectedsection']

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
            if 'selecteduser' in request.session:
                del request.session['selecteduser']
            if 'selectedcourse' in request.session:
                del request.session['selectedcourse']
            if 'selectedsection' in request.session:
                del request.session['selectedsection']
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
            if 'selectedcourse' in request.session:
                del request.session['selectedcourse']
            if 'selectedsection' in request.session:
                del request.session['selectedsection']

            if 'selecteduser' in request.session:
                return render(request, "userpage.html",
                      {"user": func_UserAsDict(request.session['selecteduser']), "role": request.session['role']})
            else:
                return redirect("/directory/")
        else:
            return redirect("/")

    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if request.POST['navigation'] == "logout":
            request.session.flush()
            return redirect("/")
        if request.POST['navigation'] == "dashboard":
            del request.session["selecteduser"]
            return redirect("/dashboard/")
        if request.POST['navigation'] == "courselist":
            del request.session["selecteduser"]
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            del request.session["selecteduser"]
            return redirect("/directory/")
        if request.POST['navigation'] == "edituser":
            if request.session['role'] != 'admin':
                return render(request, "userpage.html", {"message": "Only admins can edit users!","user": func_UserAsDict(request.session['selecteduser'])})
            else:
                return redirect("/edituser/")
        if request.POST['navigation'] == "deleteuser":
            if request.session['role'] != 'admin':
                return render(request, "userpage.html", {"message": "Only admins can delete users!","user": func_UserAsDict(request.session['selecteduser'])})
            else:
                func_DeleteUser(request)
                del request.session["selecteduser"]
                return redirect("/directory/")


class CreateUser(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selecteduser' in request.session:
                del request.session['selecteduser']
            if 'selectedcourse' in request.session:
                del request.session['selectedcourse']
            if 'selectedsection' in request.session:
                del request.session['selectedsection']
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

        message = func_CreateUser(request)
        return render(request, "createuser.html", {"message": message})


class EditUser(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selectedcourse' in request.session:
                del request.session['selectedcourse']
            if 'selectedsection' in request.session:
                del request.session['selectedsection']

            if request.session['role'] != "admin" or 'selecteduser' not in request.session:
                return redirect("/directory/")
            else:
                return render(request, "edituser.html",{"user": func_UserAsDict(request.session['selecteduser'])})
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
                del request.session["selecteduser"]
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                del request.session["selecteduser"]
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                del request.session["selecteduser"]
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/userpage/")
        message = func_EditUser(request)
        return render(request, "edituser.html", {"user": func_UserAsDict(request.session['selecteduser']), "message": message})




class CourseList(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selecteduser' in request.session:
                del request.session['selecteduser']
            if 'selectedcourse' in request.session:
                del request.session['selectedcourse']
            if 'selectedsection' in request.session:
                del request.session['selectedsection']
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
            if 'selecteduser' in request.session:
                del request.session['selecteduser']
            if 'selectedsection' in request.session:
                del request.session['selectedsection']

            if 'selectedcourse' in request.session:
                return render(request, "coursepage.html",
                          {"course": func_CourseAsDict(request.session['selectedcourse']), "role": request.session['role']})
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
                del request.session["selectedcourse"]
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                del request.session["selectedcourse"]
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                del request.session["selectedcourse"]
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
                if request.session['role'] != 'admin':
                    return render(request, "coursepage.html", {"message": "Only admins can delete courses!",
                                                               "course": func_CourseAsDict(request.session['selectedcourse'])})
                else:
                    func_DeleteCourse(request)
                    del request.session["selectedcourse"]
                    return redirect("/courselist/")
        if 'selectedsection' in request.POST:
            request.session["selectedsection"] = request.POST['selectedsection']
            return redirect("/sectionpage/")
        if 'removeuser' in request.POST:
            email_to_remove = request.POST['removeuser'] #dont need will remove later
            message = func_RemoveUserFromCourse(request, email_to_remove)
            return render(request, "createcourse.html", {"message": message})


class CreateCourse(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selecteduser' in request.session:
                del request.session['selecteduser']
            if 'selectedcourse' in request.session:
                del request.session['selectedcourse']
            if 'selectedsection' in request.session:
                del request.session['selectedsection']
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

        message = func_CreateCourse(request)
        return render(request, "createcourse.html", {"message": message})


class EditCourse(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selecteduser' in request.session:
                del request.session['selecteduser']
            if 'selectedsection' in request.session:
                del request.session['selectedsection']
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
                del request.session["selectedcourse"]
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                del request.session["selectedcourse"]
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                del request.session["selectedcourse"]
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/coursepage/")

        message = func_EditCourse(request)
        return render(request, "editcourse.html",
                  {"course": func_CourseAsDict(request.session['selectedcourse']), "message": message})


class SectionPage(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selecteduser' in request.session:
                del request.session['selecteduser']

            if 'selectedsection' in request.session:
                return render(request, "sectionpage.html",
                          {"section": func_SectionAsDict(request.session['selectedsection']),
                           "role": request.session['role']})
            else:
                return redirect("/coursepage/")
        else:
            return redirect("/")
    def post(self, request):
        if 'email' not in request.session:
            return redirect('/')
        if request.POST['navigation'] == "logout":
            request.session.flush()
            return redirect("/")
        if request.POST['navigation'] == "dashboard":
            del request.session["selectedcourse"]
            del request.session["selectedsection"]
            return redirect("/dashboard/")
        if request.POST['navigation'] == "courselist":
            del request.session["selectedcourse"]
            del request.session["selectedsection"]
            return redirect("/courselist/")
        if request.POST['navigation'] == "directory":
            del request.session["selectedcourse"]
            del request.session["selectedsection"]
            return redirect("/directory/")
        if request.POST['navigation'] == "viewcourse":
            del request.session["selectedsection"]
            return redirect("/coursepage/")
        if request.POST['navigation'] == "editsection":
            if request.session['role'] != 'admin':
                return render(request, "sectionpage.html", {"message": "Only admins can edit sections!","section": func_SectionAsDict(request.session['selectedsection'])})
            else:
                return redirect("/editsection/")
        if request.POST['navigation'] == "deletesection":
            if request.session['role'] != 'admin':
                return render(request, "sectionpage.html", {"message": "Only admins can delete sections!","user": func_SectionAsDict(request.session['selectedsection'])})
            else:
                func_DeleteSection(request)
                del request.session["selectedsection"]
                return redirect("/coursepage/")


class CreateSection(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selecteduser' in request.session:
                del request.session['selecteduser']
            if 'selectedsection' in request.session:
                del request.session['selectedsection']
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
                del request.session["selectedcourse"]
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                del request.session["selectedcourse"]
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                del request.session["selectedcourse"]
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect("/coursepage/")

        message = func_CreateSection(request)
        return render(request, "createsection.html", {"message": message})


class EditSection(View):
    def get(self, request):
        if "email" and "role" in request.session:
            if 'selecteduser' in request.session:
                del request.session['selecteduser']

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
                del request.session["selectedcourse"]
                del request.session["selectedsection"]
                return redirect("/dashboard/")
            if request.POST['navigation'] == "courselist":
                del request.session["selectedcourse"]
                del request.session["selectedsection"]
                return redirect("/courselist/")
            if request.POST['navigation'] == "directory":
                del request.session["selectedcourse"]
                del request.session["selectedsection"]
                return redirect("/directory/")
            if request.POST['navigation'] == "cancel":
                return redirect('/sectionpage/')
        message = func_EditSection(request)
        return render(request, "editsection.html",
                      {"section": func_SectionAsDict(request.session['selectedsection']), "message": message})


