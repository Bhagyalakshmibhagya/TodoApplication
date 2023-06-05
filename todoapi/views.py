from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication,permissions
from todoapi.serializers import UserSerializer,TodoSerializer
from django.contrib.auth.models import User
from tasks.models import Todo



class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    model=User
    # create,list,retrieve,update,destroy
     
    # encrypt the password
    # def create(self, request, *args, **kwargs):
    #     serializer=UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         usr=User.objects.create_user(**serializer.validated_data)
    #         serializer=UserSerializer(usr)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

# User.objects.create(username,email,password)=>ee methosil pwd encrypt aavilla
# User.objects.create_user(username,email,password)=>ee method use cheytha pwd encrypt aavum




class TodosView(ModelViewSet):
    serializer_class=TodoSerializer
    queryset=Todo.objects.all()
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

    # method1
    # def list(self, request, *args, **kwargs):
    #     qs=Todo.objects.filter(user=request.user)
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)
    
    # method2
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)



            





