from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('student/<slug:stud_id>/attendance/', views.attendance, name='attendance'),
    path('student/<slug:stud_id>/<slug:course_id>/attendance/', views.attendance_detail, name='attendance_detail'),
    path('student/<slug:class_id>/timetable/', views.timetable, name='timetable'),
   
    path('t_form/<slug:assign_id>', views.t_form, name='t_form'),
    path('upload/<slug:assign_id>', views.t_upload, name='t_upload'),
    path('teacher/<slug:teacher_id>/Classes/', views.t_clas, name='t_clas'),
    path('teacher/<int:assign_id>/Students/attendance/', views.t_student, name='t_student'),
    path('teacher/<int:ass_c_id>/attendance/', views.t_attendance, name='t_attendance'),
    path('teacher/<slug:stud_id>/<slug:course_id>/attendance/', views.t_attendance_detail, name='t_attendance_detail'),
    path('teacher/<int:att_id>/change_attendance/', views.change_att, name='change_att'),
    path('teacher/<slug:teacher_id>/t_timetable/', views.t_timetable, name='t_timetable'),
    
    path('form/', views.form, name='form'),
    path('studentupload/<slug:stud_id>', views.s_upload, name='s_upload'),

    path('signup/<slug:role>/', views.signup, name='signup'),
    path('home/', views.home, name='home'), 

]