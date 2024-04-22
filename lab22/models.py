from django.db import models
from django.forms import ModelForm

# Create your models here.
class Course(models.Model):
    cname = models.CharField(max_length=10)
    ccode = models.CharField(max_length=30)
    credits = models.IntegerField()
    def __str__(self):
        return self.cname

class Students(models.Model):
    name = models.CharField(max_length=30)
    usn = models.CharField(max_length=50)
    sem = models.IntegerField()
    branch = models.CharField(max_length=30)
    sce = models.ManyToManyField(Course)
    def __str__(self):
        return self.name

class Project(models.Model):
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    topic=models.CharField(max_length=100)
    languages=models.CharField(max_length=100)
    duration=models.IntegerField()
    def __str__(self):
        return self.topic

class ProjectReg(ModelForm):
    required_css_class = 'required'
    class Meta:
        model=Project
        fields=('student','topic','languages','duration')
