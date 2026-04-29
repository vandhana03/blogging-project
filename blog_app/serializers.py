from rest_framework import serializers
from .models import Users,Blog, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=["username","email","password","role"]
        extra_kwargs={
            'password':{'write_only':True}
        }
        

class Blogserializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields=[
            "id",
            "title",
            "content",
            "category",
            "status",
            "author",
            "created_at",
            "updated_at"
        ]
        read_only_fields=["id","author","created_at","updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields =["comment_id","user","post","comment_content","created_at","updated_at"]
        read_only_fields=["comment_id","user","created_at","updated_at"]

