
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from stuprobe.models import *


class UserRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super(UserRegForm,self).save()
        return user

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('class_id','GRN','name')

    def save(self, commit=True):
        user = super(StudentForm,self).save()
        return user


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ('id', 'dept','name')

    def save(self, commit=True):
        user = super(TeacherForm,self).save()
        return user