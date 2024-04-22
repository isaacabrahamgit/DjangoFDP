from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from lab22.models import Students,Course,ProjectReg
from django.http import HttpResponse,HttpResponseRedirect,FileResponse
from django.views import generic
from reportlab.pdfgen import canvas
import csv

# Create your views here.
def download_csv(queryset):
    
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response

def download(request):
    data = download_csv(Course.objects.all())

    return HttpResponse (data, content_type='text/csv')

def generate_pdf_file():
    from io import BytesIO
 
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
 
    # Create a PDF document
    courses = Course.objects.all()
    p.drawString(100, 750, "Course Details")
 
    y = 700
    for course in courses:
        p.drawString(100, y, f"Title: {course.cname}")
        p.drawString(100, y - 20, f"Code: {course.ccode}")
        p.drawString(100, y - 40, f"Credits: {course.credits}")
        y -= 60
 
    p.showPage()
    p.save()
 
    buffer.seek(0)
    return buffer

def generate_pdf(request):
    response = FileResponse(generate_pdf_file(), 
                            as_attachment=True, 
                            filename='course_details.pdf')
    return response

class StudentListView(generic.ListView):
    model = Students
    template_name = 'student_list.html'

class StudentDetailView(generic.DetailView):
    model = Students
    template_name = "student_detail.html"

def add_project(request):
     submitted = False
     if request.method == 'POST':
         form = ProjectReg(request.POST)
         if form.is_valid():
             form.save()
             return HttpResponseRedirect('/add_project/?submitted=True')
     else:
         form = ProjectReg()
         if 'submitted' in request.GET:
             submitted = True
     return render(request, 'project_reg.html', {'form': form, 'submitted': submitted})

def register(request):
    if request.method == 'POST':
        sname = request.POST.get('sname')
        cname = request.POST.get('cname')
        students = Students.objects.filter(name=sname).values() 
        if students:
            print(students.first())
            sid=students.first()['id']
            s=Students.objects.get(id=sid)
            
            courses = Course.objects.filter(cname=cname).values() 
            if courses:
                cid=courses.first()['id']
                c=Course.objects.get(id=cid)
                s.sce.add(c)    
                return render(request,'register.html', {'message': 'Successfully registered'})
            else:
                return render(request,'register.html',{'message': 'Course not found'})
        else:
            return render(request,'register.html',{'message': 'Student not found'})

    else:
        return render(request,'sentry.html')

def viewstudent(request):
   
    courses = Course.objects.all().values() 
    if courses:
        
        
        return render(request,'view.html', {'courses':courses})
    else:
        return 'Student not found'
def displaystudents(request):
    cid = request.POST.get('course')
    
    
    students=Students.objects.all()
    l=list()
    
    for s in students:
        ss=s.sce.filter(id=cid).values()
        if ss:
            l.append(s.name)
        
    if len(l)>=1:
        return render(request,'displaystudents.html', {'l':l})
    else:
        return HttpResponse("NO Students found for the course")
