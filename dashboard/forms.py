from django import forms
from .models import *


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        widgets = {'due':DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']


class DashBoardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter your search-:")