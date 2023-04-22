import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from mac.views import dashboard, duration, time_diff

from .models import AttendanceReport


@login_required
def saveAttendanceReport(request):

    if (request.method == "POST") and (request.user.is_authenticated):
        attendanceDetails = request.POST.get('latest_meet_attendance')

        if attendanceDetails is None:
            return JsonResponse({"message":"Bad Request"}, status=400)

        attendanceDetails = json.loads(attendanceDetails)

        attendanceReport = AttendanceReport()
        attendanceReport.meetCode = attendanceDetails["meetCode"]
        attendanceReport.date = datetime.strptime(attendanceDetails["date"], "%d/%m/%Y").date()
        attendanceReport.startTime = attendanceDetails["startTime"].strip()
        attendanceReport.stopTime = attendanceDetails["stopTime"].strip()
        attendanceReport.attendanceData = attendanceDetails["participants"]
        attendanceReport.userId = request.user

        try:
            attendanceReport.save()
            reportUrl = f"https://trackitnow.pythonanywhere.com/view-attendance-report/{attendanceReport.slug}/"
            return JsonResponse({"message":"Attendance report successfully saved.", "url":reportUrl}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({"message":"Failed to save attendance report."}, status=503)
    else:
        return JsonResponse({"message":"You are not authorised to perform this action."}, status=401)

@login_required
def viewAttendanceReport(request, slug=None):

    if slug is None:
        return redirect(dashboard)

    query = AttendanceReport.objects.filter(slug=slug)

    if query.exists():
        attendanceReport = query.first()

        if not attendanceReport.shared and attendanceReport.userId != request.user:
            return redirect(dashboard)

        isOwner = False
        if request.user == attendanceReport.userId:
            isOwner = True

        for i in range(len(attendanceReport.attendanceData)):
            attendanceReport.attendanceData[i]["joinTime"] = datetime.strptime(attendanceReport.attendanceData[i]["joinTime"],"%H:%M:%S")
            attendanceReport.attendanceData[i]["leaveTime"] = datetime.strptime(attendanceReport.attendanceData[i]["leaveTime"],"%H:%M:%S")
            attendanceReport.attendanceData[i]["percentage"] = str(round(attendanceReport.attendanceData[i]["attendedDuration"]/time_diff(attendanceReport.startTime, attendanceReport.stopTime).seconds*100,2))


        context = {
            "slug": attendanceReport.slug,
            "meetCode": attendanceReport.meetCode,
            "startTime": attendanceReport.startTime,
            "stopTime": attendanceReport.stopTime,
            "duration": duration(time_diff(attendanceReport.startTime, attendanceReport.stopTime)),
            "date": attendanceReport.date.strftime("%d %b, %Y"),
            "owner": isOwner,
            "shared": attendanceReport.shared,
            "attendanceData": attendanceReport.attendanceData,
            "participants": len(attendanceReport.attendanceData)
        }

        return render(request=request, template_name='attendance_report_view.html', context=context)

    else:
        return redirect(dashboard)

@login_required
def deleteAttendanceReport(request, slug=None):

    if slug is None:
        return redirect(dashboard)

    query = AttendanceReport.objects.filter(slug=slug)

    if query.exists():
        attendanceReport = query.first()

        if attendanceReport.userId != request.user:
            return redirect(dashboard)

        try:
            attendanceReport.delete()
            return redirect(dashboard)
        except Exception:
            return redirect(dashboard)

    else:
        return redirect(dashboard)

@login_required
def shareAttendanceReport(request, slug=None):

    if slug is None:
        return redirect(dashboard)

    query = AttendanceReport.objects.filter(slug=slug)

    if query.exists():
        attendanceReport = query.first()

        if attendanceReport.userId != request.user:
            return redirect(viewAttendanceReport, slug)

        try:
            attendanceReport.shared = not attendanceReport.shared
            attendanceReport.save()
            return redirect(viewAttendanceReport, slug)
        except Exception:
            return redirect(viewAttendanceReport, slug)

    else:
        return redirect(dashboard)