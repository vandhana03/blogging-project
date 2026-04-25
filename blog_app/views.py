import datetime
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

from .models import Users
from .passwords import check_password, hash_password
from .serializers import UserSerializer
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
