from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime, timedelta

class SleepEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    sleep_time = models.TimeField()
    wake_time = models.TimeField()  
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    sleep_date = models.DateField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.sleep_time} to {self.wake_time} on {self.sleep_date}"

class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    time = models.TimeField(default=timezone.now())  # Ensure this field exists
    message = models.TextField(default="Night Pillow Alarm")
    triggered = models.BooleanField(default=False)  # Optional: Track if alarm was triggered

    def __str__(self):
        return f"{self.title} at {self.time}"
    
class SleepRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link sleep data to users
    date = models.DateField(auto_now_add=True)  # Date of sleep record
    sleep_time = models.TimeField()
    wake_up_time = models.TimeField()
    sleep_duration = models.FloatField(null=True, blank=True)  # Duration in hours
    rating = models.IntegerField(null=True, blank=True)  # Sleep quality rating (1-5)

    def calculate_duration(self):
        bedtime = datetime.strptime(str(self.sleep_time), "%H:%M:%S")
        wake_up = datetime.strptime(str(self.wake_up_time), "%H:%M:%S")

        if wake_up < bedtime:
            wake_up += timedelta(days=1)  # Handle sleeping past midnight

        self.sleep_duration = round((wake_up - bedtime).total_seconds() / 3600, 2)
        self.save()