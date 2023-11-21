"""
URL configuration for BugBusters project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from SchedulingApp.views import Login, Dashboard, Directory, UserPage, CreateUser, EditUser, CourseList, CoursePage, CreateCourse, EditCourse, SectionPage, CreateSection, EditSection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('login/', Login.as_view()),
    path('dashboard/',Dashboard.as_view()),
    path('directory/', Directory.as_view()),
    path('userpage/', UserPage.as_view()),
    path('createuser/', CreateUser.as_view()),
    path('edituser/', EditUser.as_view()),
    path('courselist/', CourseList.as_view()),
    path('coursepage/', CoursePage.as_view()),
    path('createcourse/', CreateCourse.as_view()),
    path('editcourse/', EditCourse.as_view()),
    path('sectionpage/', SectionPage.as_view()),
    path('createsection/', CreateSection.as_view()),
    path('editsection/', EditSection.as_view()),

]
