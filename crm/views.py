from django.shortcuts import render,redirect
from django import forms
from django.views.generic import View
from django.contrib.auth.models import User
from crm.models import Employee 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model=Employee
        fields='__all__'
        widgets={"name":forms.TextInput(attrs={"class":"form-control"}),
                 "department":forms.TextInput(attrs={"class":"form-control"}),
                 "gender":forms.Select(attrs={"class":"form-select"}),
                "salary":forms.NumberInput(attrs={"class":"form-control"}),
                "email":forms.EmailInput(attrs={"class":"form-control"}),
                "profile_pic":forms.FileInput(attrs={"class":"form-control"}),
                "address":forms.Textarea(attrs={"class":"form-control"})
                 }

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model=User       
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={"first_name":forms.TextInput(attrs={"class":"form-control"}),
                 "last_name":forms.TextInput(attrs={"class":"form-control"}),
                 "email":forms.EmailInput(attrs={"class":"form-control"}),
                 "username":forms.TextInput(attrs={"class":"form-control"}),
                "password1":forms.PasswordInput(attrs={"class":"form-control"}),
                "password2":forms.PasswordInput(attrs={"class":"form-control"})


                }
        
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class EmployeeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=EmployeeForm()
        return render(request,"emp-add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=EmployeeForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("emp-list")
        return render(request,"emp-add.html",{"form":form})
    
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        return render(request,"emp-list.html",{"employees":qs})
    
class  EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        return render(request,"emp-detail.html",{"employees":qs})

class EmployeeEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp=Employee.objects.get(id=id)
        form=EmployeeForm(instance=emp)
        return render(request,"emp-edit.html",{"form":form}) 
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp=Employee.objects.get(id=id)
        form=EmployeeForm(instance=emp,data=request.POST,files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect("emp-detail",pk=id)
        return render(request,"emp-edit.html",{"form":form})  


class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id).delete()
        return redirect("emp-list")
             
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"acount has been created successfully")
            return redirect("signin")
        return render(request,"register.html",{"form":form})
    
             
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            print(usr)
            if usr:
                login(request,usr)
                return redirect("todo-list")
        return render(request,"login.html",{"form":form})
    
#class based view(cbv)
#function based view(fbv)
def signout_view(request,*args,**kwargs): 
    logout(request)
    return redirect("signin")

# class SignOutView(View):
#     def get(self,request,args,*kwargs):
#         logout(request)
#         return render("signin")





