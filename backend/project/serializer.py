from .models import Blog, Tag
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    user= serializers.ReadOnlyField(source= 'user.nickname')

    class Meta:
        model= Blog
        fields= "__all__"

class TagSerializer(serializers.ModelSerializer):
    user= serializers.ReadOnlyField(source= 'user.nickname')

    class Meta:
        model= Tag
        fields= "__all__"
        