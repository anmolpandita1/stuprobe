import os, shutil



from os import path
from django.core import serializers
from django.urls import reverse
from django.utils import timezone

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


from .models import *
from stuprobe.forms import *



reg_save = 'C:/project/be/data/registered/'
classroom_save = 'C:/project/be/data/classroom_uploads/'



# Create your views here.
def index(request):
    return render(request, 'stuprobe/logout.html')


def signup(request, role):
    if role == 'student':
        if request.method == 'POST':
            user_form = UserRegForm(request.POST)
            student_form = StudentForm(request.POST)

            if user_form.is_valid() and student_form.is_valid():
                user = user_form.save()
                student = student_form.save(False)

                student.user = user
                student.save()

                return render(request, 'stuprobe/base.html')

        else:
            user_form = UserRegForm()
            student_form = StudentForm()
        context = {
            'UserForm' : user_form,
            'StudentForm' : student_form,
            'role' : role
        }
        return render(request, 'stuprobe/signup.html', context )

    else:
        if request.method == 'POST':
            user_form = UserRegForm(request.POST)
            teacher_form = TeacherForm(request.POST)
            if user_form.is_valid() and teacher_form.is_valid():
                user = user_form.save()
                teacher = teacher_form.save(False)

                teacher.user = user
                teacher.save()

                return render(request, 'stuprobe/base.html')

        else:
            user_form = UserRegForm()
            teacher_form = TeacherForm()

        context = {
            'UserForm' : user_form,
            'TeacherForm' : teacher_form,
            'role' : role
        }
        return render(request, 'stuprobe/signup.html', context )





@login_required
def home(request):
    if request.user:
        return render(request, 'stuprobe/homepage.html')
    return render(request, 'stuprobe/logout.html')


@login_required()
def attendance(request, stud_id):
    stud = Student.objects.get(GRN=stud_id)
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    att_list = []
    for ass in ass_list:
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'stuprobe/attendance.html', {'att_list': att_list})


@login_required()
def attendance_detail(request, stud_id, course_id):
    stud = get_object_or_404(Student, GRN=stud_id)
    cr = get_object_or_404(Course, id=course_id)
    att_list = Attendance.objects.filter(course=cr, student=stud).order_by('date')
    att_list_graph = Attendance.objects.only("date", "status")
    att_list_graph = serializers.serialize('json', att_list_graph)


    context = {
        'att_list': att_list,
        'cr': cr,
        'json':att_list_graph,
    }
    return render(request, 'stuprobe/att_detail.html', context)










@login_required
def t_clas(request, teacher_id):
    teacher1 = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'stuprobe/t_clas.html', {'teacher1': teacher1})


@login_required()
def t_student(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    att_list = []
    for stud in ass.class_id.student_set.all():
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'stuprobe/t_students.html', {'att_list': att_list})



@login_required()
def t_attendance(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
        'assc': assc,
    }
    return render(request, 'stuprobe/t_attendance.html', context)




@login_required()
def t_attendance_detail(request, stud_id, course_id):
    history = []
    stud = get_object_or_404(Student, GRN=stud_id)
    cr = get_object_or_404(Course, id=course_id)
    att_list = Attendance.objects.filter(course=cr, student=stud).order_by('date')
    for a in att_list:
        if a.status:
            print(a.status)
            history.append(1)
        else:
            print(a.status)
            history.append(0)
    return render(request, 'stuprobe/t_att_detail.html', {'att_list': att_list, 'cr': cr, 'history':history})


@login_required()
def change_att(request, att_id):
    a = get_object_or_404(Attendance, id=att_id)
    a.status = not a.status
    a.save()
    return HttpResponseRedirect(reverse('t_attendance_detail', args=(a.student.GRN, a.course_id)))





@login_required()
def timetable(request, class_id):
    asst = AssignTime.objects.filter(assign__class_id=class_id)
    matrix = [['' for i in range(9)] for j in range(6)]

    for i, d in enumerate(DAYS_OF_WEEK):
        t = 0
        for j in range(9):
            if j == 0:
                matrix[i][0] = d[0]
                continue
            if j == 3 or j == 6:
                continue
            try:
                a = asst.get(period=time_slots[t][0], day=d[0])
                matrix[i][j] = a.assign.course_id
            except AssignTime.DoesNotExist:
                pass
            t += 1

    context = {'matrix': matrix}
    return render(request, 'stuprobe/timetable.html', context)


@login_required()
def t_timetable(request, teacher_id):
    asst = AssignTime.objects.filter(assign__teacher_id=teacher_id)
    class_matrix = [[True for i in range(9)] for j in range(6)]
    for i, d in enumerate(DAYS_OF_WEEK):
        t = 0
        for j in range(9):
            if j == 0:
                class_matrix[i][0] = d[0]
                continue
            if j == 3 or j == 6:
                continue
            try:
                a = asst.get(period=time_slots[t][0], day=d[0])
                class_matrix[i][j] = a
            except AssignTime.DoesNotExist:
                pass
            t += 1

    print(class_matrix)
    context = {
        'class_matrix': class_matrix,
    }
    return render(request, 'stuprobe/t_timetable.html', context)


###################___________UPLOAD FORM VIEWS___________#######################
def form(request):
    return render(request, "stuprobe/form.html")



def t_form(request, assign_id):
    print('######################################')
    
    
    for filename in os.listdir(classroom_save):
        file_path = os.path.join(classroom_save, filename)
        print(file_path)
        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return render(request, "stuprobe/form.html", {'assign_id':assign_id})



def t_upload(request, assign_id):

    


    
    course_name = get_object_or_404(Assign, id=assign_id)
    course_id = course_name.course_id
    
    

    if not path.exists(classroom_save + course_id + '/'):
	    os.mkdir(classroom_save + course_id + '/')

    for count, x in enumerate(request.FILES.getlist("files")):
        def process(f):
            with open(classroom_save + course_id + '/' + str(count) + '.jpg', 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        process(x)
    return render(request, 'stuprobe/message.html')




def s_upload(request, stud_id):
    if not path.exists(reg_save + stud_id + '/'):
        os.mkdir(reg_save + stud_id + '/')
    
    for count, x in enumerate(request.FILES.getlist("files")):
        def process(f):
            with open(reg_save + stud_id + '/' + str(count) + '.jpg', 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        process(x)
    return render(request, 'stuprobe/message.html')

