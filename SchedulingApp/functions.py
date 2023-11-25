from django.shortcuts import render, redirect
from django.views import View
from .models import Course, MyUser, Section
from django.http import HttpResponseRedirect
from operator import itemgetter
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

"""
POST Functions. These happen from button presses and form submissions.
Check if all the context variables from request.POST['variable'] are valid using validator functions
and create an object and returns a render of a page with a success message
If a validator function fails then no object is created and a render is returned with a failure method.   
"""
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
"""
MyUser validator functions used when creating or editing MyUser objects
"""
def func_ValidateEmail(email):
    pass
def func_ValidatePassword(password,confirmPassword):
    pass
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
"""
Course validator functions used when creating or editing Course objects
"""
def func_ValidateCourseName(name):
    pass
def func_ValidateDepartment(department):
    pass
def func_ValidateCourseNumber(courseNumber):
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

