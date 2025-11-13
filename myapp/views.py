from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import bcrypt
from .models import new_crud
import cloudinary
from cloudinary import uploader
import cloudinary.api
from .serializers import CrudSerializer
from rest_framework.parsers import JSONParser
# Create your views here.


def userlist(req):
    if req.method=="GET":
        users=new_crud.objects.all()
        serializer=CrudSerializer(users,many=True)
        return JsonResponse(serializer.data,safe=False)

def partial_user(req,user_id):
    if req.method== 'GET':
        try:
            single_user=new_crud.objects.get(id=user_id)
            serializer=CrudSerializer(single_user)
            return JsonResponse(serializer.data,safe=False)
        except:
            return JsonResponse({"error":"User not found"})

@csrf_exempt
def new_register(req):
    if req.method=='POST':
        try:
            data=req.POST
            img=req.FILES.get('profile_url')
            # print(img)
            profile_url=None
            if img:
                upload_result=cloudinary.uploader.upload(img)
                # print(upload_result)
                profile_url=upload_result.get('secure_url')
            raw_pass=data.get('password')
            hashed_password=bcrypt.hashpw(raw_pass.encode('utf-8'),bcrypt.gensalt(rounds=12)).decode('utf-8')
            payload={
                "name":data.get('name'),
                "email":data.get('email'),
                "phone":data.get('number'),
                "profile_url":profile_url,
                "password":hashed_password
            }
            # user_name=req.POST.get('name')
            # user_mail=req.POST.get('email')
            # user_num=req.POST.get('number')
            # user_profile=req.FILES.get('profile')
            # img_url=cloudinary.uploader.upload(user_profile)
            # serialized=CrudSerializer(data=)
            # new_record=new_crud.objects.create(name=user_name,email=user_mail,phone=user_num,profile_url=img_url['secure_url'])
            # print(img_url['secure_url'])
            # print(user_profile)
            serializer=CrudSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=201)
            return JsonResponse(serializer.errors)
        except Exception as e:
            return JsonResponse({"error":str(e)})
    return JsonResponse({"msg":"only post method accept","data": serializer.data},
        status=201)
            
@csrf_exempt  
def update(req,user_id):
    if req.method == 'POST':
        try:
            user=new_crud.objects.get(id=user_id)
            # print(user)
            # if req.POST.get('name'):
            #     user.name=req.POST.get('name')
            # if req.POST.get('email'):
            #     user.email=req.POST.get('email')
            # if req.POST.get('number'):
            #     user.email=req.POST.get('number')
            # if req.POST.get('profile'):
            #     user.email=req.POST.get('profile')
            data=JSONParser().parse(req)
            serializer=CrudSerializer(user,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)
        except Exception as e:
            return JsonResponse({"error":str(e)})
    return JsonResponse({"error":"only post method accept"})


@csrf_exempt
def delete(req,user_id):
    if req.method  == 'DELETE':
        try:
            user=new_crud.objects.get(id=user_id)
            user.delete()
            return JsonResponse ({"msg":"User deleted successfully"})
        except:
            return JsonResponse({"error":"No user found"})
            