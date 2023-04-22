from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models.functions import Concat
from .models import Attendance_Record,Student,Class
from shesh.models import AttendanceReport
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

def duration(meet_duration):
    if meet_duration.seconds//3600 == 0:
        if meet_duration.seconds//60 == 0:
            meet_duration = "Less than 1 Minute"
        else:
            meet_duration = str(meet_duration.seconds//60)+" Minutes"
    else:
        if meet_duration.seconds//60 == 0:
            meet_duration = str(meet_duration.seconds//3600)+" Hours"
        else:
            meet_duration = str(meet_duration.seconds//3600)+" Hours "+str((meet_duration.seconds//60) - (60*(meet_duration.seconds//3600))) + " Minutes"

    return meet_duration

def normalize_time(time):
    time = time.lower()

    if "am" in time:
        time = time.replace("am","")
    elif "pm" in time:
        time = time.replace("pm","")
        time = time.strip(" ")
        time_chunks = time.split(":")
        if int(time_chunks[0]) != 12:
            time_chunks[0] = str(int(time_chunks[0])+12)
        time = ":".join(time_chunks)

    return time

def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

@login_required
def dashboard(request):
    """View function for user dashboard page."""

    query = Attendance_Record.objects.filter(user_id= request.user)

    if query.exists():

        attendance_list = []

        for i in range(0,len(query)):
            attendance_list.append((i+1, query[i].meet_code, query[i].date.strftime("%d %b, %Y"), duration(time_diff(query[i].start_time,query[i].stop_time)),  len(query[i].student_names), query[i].slug))

        context = {"Attendance_record": attendance_list}

    else:
        context = {"Attendance_record": "None"}

    reports = AttendanceReport.objects.filter(userId = request.user)

    if reports.exists():

        reportsList = []

        for i in range(len(reports)):
            reportsList.append((i+1, reports[i].meetCode, reports[i].date.strftime("%d %b, %Y"), duration(time_diff(reports[i].startTime, reports[i].stopTime)), len(reports[i].attendanceData), reports[i].slug))

        context["AttendanceReports"] = reportsList

    else:
        context["AttendanceReports"] = "None"

    return render(request, 'dashboard.html', context=context)

@login_required
def save(request):
    """View function for showing attendance after the meet ends."""

    return render(request, "save.html")


@csrf_exempt
def save_to_database(request):
    """View function for saving attendance to database."""

    if (request.method == "POST") and (request.user.is_authenticated):

        attendance_details = json.loads(request.POST.get('latest_meet_attendance'))

        attendance = Attendance_Record()


        attendance_details['start_time'] = normalize_time(attendance_details['start_time'])
        attendance_details['stop_time'] = normalize_time(attendance_details['stop_time'])

        attendance.meet_code = attendance_details['meet_code']
        attendance.start_time = attendance_details['start_time'].strip(' ')
        attendance.stop_time = attendance_details['stop_time'].strip(' ')
        # print(attendance_details['date'])
        if "ago" in attendance_details['date'].lower():
            attendance_details['date'] = attendance_details['date'].lower().replace("ago","Aug")

        if "sept" in attendance_details['date'].lower():
            attendance_details['date'] = attendance_details['date'].lower().replace("sept","Sep")

        if "set." in attendance_details['date'].lower():
            attendance_details['date'] = attendance_details['date'].lower().replace("set.","Sep")

        if "out." in attendance_details['date'].lower():
            attendance_details['date'] = attendance_details['date'].lower().replace("out.","Oct")


        attendance.date = datetime.strptime(attendance_details['date'], "%d/%b/%Y").date()
        attendance.user_id = request.user

        present_students = [] #to map student's names with their id in the database

        for student in attendance_details['student_names']:
            result = Student.objects.filter(name=student)
            present_students.append(result)

        att = attendance_details['attended_duration']
        for i in range(len(att)):
            att[i] = round((att[i]/attendance_details['meet_duration'])*100,2)

        attendance.student_names = attendance_details['student_names']

        attendance.attended_duration = att

        for i in range(0,len(attendance_details['join_time'])):
            attendance_details['join_time'][i] = normalize_time(attendance_details['join_time'][i])
            attendance_details['join_time'][i] = normalize_time(attendance_details['join_time'][i])

        attendance.join_time = attendance_details['join_time']

        if Attendance_Record.objects.count()>0:
            uuid  = Attendance_Record.objects.all().last().pk
        else:
            uuid = 1

        attendance.slug = attendance_details['meet_code']+str(uuid)
        # print(attendance.__dict__)

        try:

            attendance.save()
            # print('Attendance successfully saved to database.')
            return JsonResponse({"record_id": attendance.slug}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"status":"Failed"}, status=503)
    else:
        return JsonResponse({"status":"Unauthenticated"}, status=401)

@login_required
@csrf_exempt
def report_view(request, meet_code_id=None):
    """View function for showing attendance report."""

    if meet_code_id is None:
        return redirect(index)

    report_id = meet_code_id

    _query = Attendance_Record.objects.filter(slug=report_id).first()

    if not _query.shared and request.user != _query.user_id:
        return redirect(index)

    owner = False
    if request.user == _query.user_id:
        owner = True

    s_no = range(1,len(_query.student_names)+1)

    context = {
        "id": report_id,
        "meet_code": _query.meet_code,
        "start_time": _query.start_time,
        "stop_time": _query.stop_time,
        "date": _query.date.strftime("%d %b, %Y"),
        "meet_duration": duration(time_diff(_query.start_time,_query.stop_time)),
        "attendance": zip(s_no,_query.student_names, _query.join_time, _query.attended_duration),
        "participants": len(_query.student_names),
        "owner": owner,
        "shared": _query.shared,
        "record_id":_query.slug
    }

    return render(request, 'report_view.html', context=context)

def docs(request):
    """View function for docs page."""

    return render(request, 'docs.html')

def privacy_policy(request):
    """View function for privacy policy page."""

    return render(request, 'privacy_policy.html')

def delete_record(request, meet_code_id= None):
    """View function for deleting attendance record."""
    report_id = meet_code_id

    if meet_code_id == None:
        return redirect(index)

    _query = Attendance_Record.objects.filter(slug=report_id).first()

    if request.user == _query.user_id:
        try:
            _query.delete()
            return redirect(dashboard)
        except Exception:
            return redirect(dashboard)
    else:
        return redirect(dashboard)

def change_sharing_status(request, meet_code_id = None):
    """View function for sharing and unsharing a report"""
    report_id = meet_code_id

    if meet_code_id == None:
        return redirect(index)

    _query = Attendance_Record.objects.filter(slug=report_id).first()

    if request.user == _query.user_id:
        try:
            if _query.shared:
                _query.shared = False
            else:
                _query.shared = True
            _query.save()
            return redirect(report_view,meet_code_id)
        except Exception:
            return redirect(report_view,meet_code_id)
    else:
        return redirect(report_view,meet_code_id)