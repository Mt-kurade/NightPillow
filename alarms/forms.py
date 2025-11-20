from django import forms
from .models import SleepRecord

class SleepForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ['sleep_time', 'wake_up_time', 'rating']