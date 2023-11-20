from django.shortcuts import render, redirect
from django.views import View
from .models import Course, MyUser, Section
from django.http import HttpResponseRedirect

class Login(View):
    def get(self, request):
        return render(request, "login.HTML")
    def post(self,request):
        return redirect("/dashboard")

class Dashboard(View):
    def get(self, request):
        return render(request, "dashboard.html")
    def post(self,request):
        return redirect("/login")
