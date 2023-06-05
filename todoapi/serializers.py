from rest_framework import serializers
from django.contrib.auth.models import User
from tasks.models import Todo



class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=["id","username","email","password"]
        # serializer.create eppozano varane appoze ee create wrk aavu
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

        # fields are automatically populated
        # create(),update()

class TodoSerializer(serializers.ModelSerializer):
        id=serializers.CharField(read_only=True)
        data=serializers.CharField(read_only=True)
        user=serializers.CharField(read_only=True)
        status=serializers.CharField(read_only=True)


        class Meta:
             model=Todo
             fields="__all__"


