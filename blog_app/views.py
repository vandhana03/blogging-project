import datetime
import json
import jwt

from tokenize import generate_tokens
from django.conf import settings

from . import models
SECRET_KEY=settings.SECRET_KEY

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from .models import Users,Blog, Category
from .passwords import check_password, hash_password
from .serializers import UserSerializer, Blogserializer
from blog_app.utils.email_utils import send_dynamic_email
# Create your views here.
@method_decorator(csrf_exempt,name='dispatch')
class register(View):
    def post(self,req):
        data={
            "username":req.POST.get('username'),
            "password":req.POST.get('password'),
            "email":req.POST.get('email'),
            "role":req.POST.get('role'),
        }
        if data['password']:
            data['password']=hash_password(data['password'])

        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_dynamic_email(req,data['username'],data['email'],'welcome_email')
            print("Email Value:",data['email'])

            return JsonResponse({
                "status":True,
                "message":"User registered succesffully",
                "data":serializer.data
            },status=201)
        else:
            print(serializer.errors)
        return JsonResponse(serializer.errors,status=400)
        
            
@method_decorator(csrf_exempt,name='dispatch')
class login(View):
    def post(self,req):
        username=req.POST.get('username')
        password=req.POST.get('password')

        if not username or not password:
            return JsonResponse({"error":"Missing Credentials"},status=400)
        
        try:
            user=Users.objects.get(username=username)
        except Users.DoesNotExist:
            return JsonResponse({"error":"user not found"},status=404)
        
        if not check_password(password,user.password):
            return JsonResponse({"error":"invalid response"},status=401)
        
        payload={
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            
        }
        token=jwt.encode(payload,SECRET_KEY,algorithm="HS256")
        return JsonResponse({
            "message": "Login successful",
            "token": token,
            "user":{
                "username":user.username,
                "email":user.email,
                "role":user.role
          }
        }, status=200)



@method_decorator(csrf_exempt,name='dispatch')
class BlogView(View):
    # def get(self,req):
    #     return JsonResponse({'status':'middleware worked well'})
    
    #create blog
    def post(self,request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JsonResponse({"error": "Token missing"}, status=401)
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = Users.objects.get(username=payload["username"])
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        
        data = json.loads(request.body)
        print(user)
        data['author'] = user.username
        print(data)
        serializer = Blogserializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        post = serializer.save(author=user)
        return JsonResponse(Blogserializer(post).data, status=201)
        
    #edit blog
    def patch(self,request,blog_id):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JsonResponse({"error": "Token missing"}, status=401)
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = Users.objects.get(username=payload["username"])
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        try:
            post = Blog.objects.get(id=blog_id)

        except Blog.DoesNotExist:
            return JsonResponse({"error":"blog not found"},status=404)

        if post.author != user:
            return JsonResponse({"error":"not allowed"},status=403)

        data = json.loads(request.body)

        serializer = Blogserializer(post, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

        return JsonResponse({
            "message":"Post updated",
            "data":serializer.data
        })
       

            
    
    #delete blog
    def delete(self,request,blog_id):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JsonResponse({"error": "Token missing"}, status=401)
        try:
            token = auth_header.split(" ")[1]

            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            user = Users.objects.get(username=payload["username"])

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)

        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        try:
            post = Blog.objects.get(id=blog_id)

        except Blog.DoesNotExist:
            return JsonResponse({"error":"post not found"},status=404)

        if post.author != user and user.role != "ADMIN":
            return JsonResponse({"error":"not allowed"},status=403)
        post.delete()

        return JsonResponse({"message":"Post deleted"})
        