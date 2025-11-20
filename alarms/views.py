import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import SleepEntry
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
import json 
from .models import SleepRecord
from datetime import datetime
from .models import Alarm
from datetime import datetime
import pytz
LOCAL_TIMEZONE =  pytz.timezone("Asia/Kolkata")


@login_required
def home(request):
    return render(request, "alarms\home.html")  #alarms/home.html 
#Im confused on wtf i just did, just as long as its working I will not touch it

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            return redirect("login")
    return render(request, "alarms/signup.html")


def login_views(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('alarms/home')
    else:
        messages.error(request, "Invalid username or password")
        form = AuthenticationForm()
    return render(request, "alarms/login.html", {'form': form})

@login_required
def sleep_data(request):
    sleep_entries = SleepEntry.objects.all()
    labels = [str(entry.sleep_date) for entry in sleep_entries]
    sleep_durations = [round((entry.wake_time.hour + entry.wake_time.minute / 60) - (entry.sleep_time.hour + entry.sleep_time.minute / 60), 2) for entry in sleep_entries]
    return render(request, 'alarms/sleep_data.html', {'sleep_entries': sleep_entries, 'labels': json.dumps(labels), 'sleep_durations': json.dumps(sleep_durations)})

def sleep_calculator(request):
    recommended_times = []
    if request.method == "POST":
        sleep_time = request.POST.get("sleep_time")
        wake_time = request.POST.get("wake_time")
        
        if sleep_time:
            base_time = datetime.strptime(sleep_time, "%H:%M")
            recommended_times = [(base_time + timedelta(minutes=90 * i)).strftime("%H:%M") for i in range(1, 7)]
        elif wake_time:
            base_time = datetime.strptime(wake_time, "%H:%M")
            recommended_times = [(base_time - timedelta(minutes=90 * i)).strftime("%H:%M") for i in range(1, 7)]
        
    return render(request, "alarms/sleep_calculator.html", {"recommended_times": recommended_times})



@login_required
def save_sleep_data(request):
    print("save_sleep_data view called")
    if request.method == "POST":
        try:
            print("Request Body (raw):", request.body.decode('utf-8'))
            return JsonResponse({"message": "Data received!"})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": str(e)}, status=400)
    else:
        print("Invalid request method")
        return JsonResponse({"error": "Invalid request"}, status=400)
    
@login_required
def sleep_data(request):
    print("Logged-in user ID:", request.user.id)
    sleep_records = SleepRecord.objects.filter(user=request.user).order_by('date')
    print("Sleep records:", sleep_records)

    labels = []
    durations = []

    for record in sleep_records:
        sleep_datetime = datetime.combine(datetime.today(), record.sleep_time)
        wake_datetime = datetime.combine(datetime.today(), record.wake_time)
        if wake_datetime < sleep_datetime:
            wake_datetime += timedelta(days=1)
        duration = (wake_datetime - sleep_datetime).total_seconds() / 3600.0

        labels.append(str(record.date))
        durations.append(duration)

    print("Labels:", labels)
    print("Durations:", durations)

    return render(request, 'alarms/sleep_data.html', {'sleep_records': sleep_records, 'labels': labels, 'sleep_durations': durations})


def reminders(request):
    alarms = Alarm.objects.filter(user=request.user)
    return render(request, "alarms/reminders.html", {"alarms": alarms})

def create_alarm(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            time = data.get("time")
            message = data.get("message")
            alarm = Alarm.objects.create(title=title, time=time, message=message, user=request.user)
            return JsonResponse({"success": True, "alarm_id": alarm.id})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})

@require_http_methods(["DELETE"])
def delete_alarm(request, alarm_id):
    print(f"Deleting alarm with ID: {alarm_id}")
    alarm = get_object_or_404(Alarm, pk=alarm_id)
    alarm.delete()
    print(f"Alarm with ID: {alarm_id} deleted from database")
    return JsonResponse({"success": True})

def check_alarm(request):
    now = datetime.now(LOCAL_TIMEZONE).time()
    for alarm in Alarm.objects.filter(user=request.user):
        if alarm.time.hour == now.hour and alarm.time.minute == now.minute:
            return JsonResponse({"trigger": True, "message": alarm.message})
    return JsonResponse({"trigger": False})