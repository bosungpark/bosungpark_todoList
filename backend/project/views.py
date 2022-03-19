#데이터 처리
from distutils.command.sdist import sdist
from urllib import request
from django.test import tag
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.core.serializers.json import DjangoJSONEncoder

from pytz import timezone
from  .models import Blog, Tag, Applied
from .serializer import BlogSerializer, TagSerializer


#viewSet
from rest_framework import viewsets

#about athentications
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly

#APIVIEW
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
#timezone
from django.utils import timezone

from django.shortcuts import get_object_or_404, render

from rest_framework.pagination import LimitOffsetPagination


class BlogList(APIView, LimitOffsetPagination):

    authentication_classes=[BasicAuthentication,SessionAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # list
    def get(self, request):
        blogs=Blog.objects.all()

        results = self.paginate_queryset(blogs, request, view=self)
        serializer= BlogSerializer(results, many=True)
        return Response(serializer.data)
        # return render(request, "home.html")
    # edit
    def post(self,request):
        serializer=BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogDetail(APIView):
    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        blog=self.get_object(pk)
        serializer= BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        blog=self.get_object(pk)
        serializer= BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            blog.modify_at=timezone.now()

            #만약 목표가 달성되었음을 표시하면 완료일시가 자동으로 등록된다.
            if blog.is_achieved==True:
                blog.ended_at=timezone.now()

            serializer=BlogSerializer(blog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # edit tag
    def post(self,request,pk):
        serializer=TagSerializer(data=request.data)
        print('request.data      ', request.data)
        if serializer.is_valid():
            
            #만일 태그 이름이 같은 데이터가 존재하면 데이터를 보내준다.
            key=serializer.validated_data['tag']
            if Tag.objects.filter(tag=key):

                queryset=Tag.objects.filter(tag=key).values()
                queryset.blog=pk
                # print("               !!!!!!!",list(queryset))
                serialized_q = json.dumps(list(queryset), cls=DjangoJSONEncoder)
                # print(serialized_q)

                # return render(request, "tag.html",{'tag':queryset})
                return JsonResponse(serialized_q,safe=False)
            serializer.save()

            # 태그 등록시 등록된 태그 데이터베이스에 등록. unique 옵션을 주지 않았으므로, 객체마다 등록되고 삭제시 하나씩 삭제 가능
            applied=Applied(tag=serializer.validated_data["tag"])
            applied.save()
            print(applied)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        blog=self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagList(APIView):
    
    authentication_classes=[BasicAuthentication,SessionAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # list
    def get(self, request):
        tags=Tag.objects.all()

        serializer= TagSerializer(tags, many=True)
        return Response(serializer.data)
    

class TagDetail(APIView):
    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tag=self.get_object(pk)
        serializer= TagSerializer(tag)
        return Response(serializer.data)

    def put(self, request, pk, format=None):#개별 태그 부분 삭제는 put을 통해 연결을 끊는 방향으로 이후 구현, 모델에 삭제 여부 추가(ex. if 삭제버튼 클릭: tag.blog=-1, tag.name="dfajldsaljdsal;fdjjldsskdjdsl" applied.delete())
        tag=self.get_object(pk)
        serializer= TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            if tag.deleted==True:
                tag.blog=-1
            serializer.save()
    
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):#태그 전체 삭제
        tag=self.get_object(pk)
        tagname=self.get_object(pk).tag
        
        applied=Applied.objects.get(tag=tagname)
        if not applied:
            tag.delete()        
        else:
            print("이미 이용중인 태그는 삭제가 불가합니다.")
        

