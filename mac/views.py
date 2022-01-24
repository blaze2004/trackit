from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models.functions import Concat
from .models import Attendance_Record,Student,Class
from datetime import datetime,date,timedelta,time
import json
# Create your views here.

def time_diff(start, end):
    if isinstance(start, time): # convert to datetime
        assert isinstance(end, time)
        start, end = [datetime.combine(datetime.min, t) for t in [start, end]]
    if start <= end: 
        return end - start
    else: 
        end += timedelta(1)
        assert end > start
        return end - start

def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

@login_required
def dashboard(request):
    """View function for user dashboard page."""

    return render(request, 'dashboard.html')

@login_required
def save(request):
    """View function for showing attendance after the meet ends."""
    query = Attendance_Record.objects.filter(user_id = request.user)
    
    if query.exists():
        _query = query.latest(Concat('date', 'stop_time'))
        
        if _query.date == date.today():

            meet_duration = time_diff(_query.start_time,_query.stop_time)
            if meet_duration.seconds//3600 == 0:
                if meet_duration.seconds//60 == 0:
                    meet_duration = "Less than 1 Minute"
                else:
                    meet_duration = str(meet_duration.seconds//60)+" Minutes"
            else:
                if meet_duration.seconds//60 == 0:
                    meet_duration = str(meet_duration.seconds//3600)+" Hours"
                else:
                    meet_duration = str(meet_duration.seconds//3600)+" Hours "+str(meet_duration.seconds//60) + " Minutes"

            latest_meet_attendance = {
                "meet_code": _query.meet_code,
                "start_time": _query.start_time.strftime("%I:%M %p"),
                "stop_time": _query.stop_time.strftime("%I:%M %p"),
                "date": _query.date.strftime("%m/%d/%Y"),
                "meet_duration": meet_duration,
                "attendance": zip(_query.student_names, _query.join_time, _query.attended_duration),
                "participants": len(_query.student_names)
            }

            return render(request, "save.html", context=latest_meet_attendance)

    return redirect(index)

@csrf_exempt
def save_to_database(request):
    """View function for saving attendance to database."""

    if request.method == "POST":
        
        attendance_details = json.loads(request.POST.get('latest_meet_attendance'))
        attendance = Attendance_Record()
        attendance.meet_code = attendance_details['meet_code']
        attendance.start_time = attendance_details['start_time']
        attendance.stop_time = attendance_details['stop_time']
        attendance.date = datetime.strptime(attendance_details['date'], "%d/%b/%Y").date()
        attendance.user_id = request.user

        present_students = [] #to map student's names with their id in the database

        for student in attendance_details['student_names']:
            result = Student.objects.filter(name=student)
            print(type(result))
            present_students.append(result)

        attendance.student_names = attendance_details['student_names']
        attendance.join_time = attendance_details['join_time']
        attendance.attended_duration = attendance_details['attended_duration']

        try:
            attendance.save()
            print('Attendance successfully saved to database.')
            return JsonResponse({"status": "ok"}, status=200)
        except Exception:
            return JsonResponse({"status":"Failed"}, status=503)
    else:
        return JsonResponse({"status":"Failed"}, status=503)