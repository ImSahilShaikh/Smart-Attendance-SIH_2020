from django import forms
from AMS.models import Student

class StudentForm(forms.ModelForm):
	model = Student
	fields = "__all__"	 