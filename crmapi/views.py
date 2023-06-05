from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from crm.models import Employee
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework import permissions,authentication

class EmployeeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Employee
        fields="__all__"
        # exclude=("id",)

# request.POST=>request.data
# form=>serializers

class EmployeesView(ViewSet):
    # list,create,retrieve,update,destroy
    # get=>list,retrieve
    # post=>create
    # put=>update
    # delete=>destroy
    # localhost:8000/api/employees/
    # method=>get
    def list(self,request,*args,**kwargs):
        # return all employee records
        qs=Employee.objects.all()
        # localhost:8000/api/employees/?department=HR
        # request.query_params={'department':["HR"]}

        if "department" in request.query_params:
            dept=request.query_params.get("department")
            qs=qs.filter(department__iexact=dept)

        if "salary" in request.query_params:
            sal=request.query_params.get("salary")
            qs=qs.filter(salary=sal)

        if "salary_gt" in request.query_params:
            sal=request.query_params.get("salary_gt")
            qs=qs.filter(salary__gte=sal)

        # qs=>python native type=>deserialization
        # varname=serializerName(qs)
        # deserialization
        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    # method=>post
    def create(self,request,*args,**kwargs):
        # create a employee record
        # serialization
        serializer=EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        # return Response(data={"result":"creating employee record"})
    
    # method=>get
    # localhost:8000/api/employees/3/
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(qs)
        return Response(data=serializer.data)
    
    # method=>put
    # localhost:8000/api/employees/3/
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp_obj=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(instance=emp_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.data)
        # return Response(data={"result":"updating employee object"})
    
    # method=>delete
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Employee.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no matching record found")
 # return Response(data={"result":"deleting employee object"})


# custom methods
# depts=Employee.objects.all().values_list('department',flat=True).distinct()
    @action(methods=["get"],detail=False)
    def all_departments(self,request,*args,**kwargs):
        qs=Employee.objects.all().values_list("department",flat=True).distinct()
        return Response(data=qs)

class EmployeeViewsetView(ModelViewSet):
    serializer_class=EmployeeSerializer
    model=Employee
    queryset=Employee.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAdminUser]






        
