from datetime import datetime
from multiprocessing import context
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render
from .models import Employee, Role,Department
from datetime import datetime
from django.db.models import Q



# Create your views here.
def index(request):
    return render( request, 'index.html')

def all_emp(request):
    emps=Employee.objects.all()
    context={
        'emps': emps
    }
    print(context)
    return render( request, 'all_emp.html',context)

def add_emp(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone=request.POST['phone']
        role=request.POST['role']
        dept=request.POST['dept']
        salary=int(request.POST['salary'])
        bonus=int(request.POST['bonus'])

        new_emp=Employee(first_name=first_name,last_name=last_name,phone=phone,role_id=role,dept_id=dept,salary=salary,bonus=bonus,hire_date=datetime.now())
        new_emp.save()
        return HttpResponse('Employee Added Successfully')
    elif request.method=="GET":
        return render( request, 'add_emp.html')
    else:
        return render('An Error Occured')

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed=Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed")
        except:
            return HttpResponse("Please return a valid emp id")
    emps=Employee.objects.all()
    context={
        'emps':emps
    }
    return render( request, 'remove_emp.html',context)

def filter_emp(request):
    if request.method=='POST':
        # first_name=request.POST['first_name']
        # last_name=request.POST['last_name']
        name=request.POST['name']
        dept=request.POST['dept']
        role=request.POST['role']
        emps =Employee.objects.all()
        # if first_name:
        #     pass
        # if last_name:
        #     pass
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(dept__name__icontains=role)

        context = {
            'emps':emps
        }
        return render(request,'all_emp.html',context)

    elif request.method =='GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occured')
