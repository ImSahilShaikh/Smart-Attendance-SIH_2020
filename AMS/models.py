# Create your models here.
from django.db import models

class Student(models.Model):
	rollno=models.IntegerField(unique=True)
	name=models.CharField(max_length=20)
	status=models.BooleanField(default=False)
	class Meta:
		db_table="student"