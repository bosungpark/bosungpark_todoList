from django.db import models

from account.models import User

import random

class Blog(models.Model):
      
    id= models.AutoField(primary_key=True, null=False, blank=False)
    user= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    title=models.CharField(max_length=100)#제목
    body=models.TextField()#상세설명
    
    created_at= models.DateTimeField(auto_now_add=True)#생성일
    modify_at = models.DateTimeField(null=True, blank=True)#수정일
    goal_at=models.CharField(null=False, blank=False,max_length=100,default="목표날짜를 정해놓고 하는 것은 아님.")# 목표 마감일
    ended_at=models.DateTimeField(null=True, blank=True)#실제 마감일

    is_achieved= models.BooleanField(default=False)#달성여부


class Tag(models.Model):#태그
    Tag_TextColors=["red","yellow","blue","green"]#글자 색
    i=random.randrange(0,4)

    Tag_BackgroundColors=["red","yellow","blue","green"]#배경색
    j=random.randrange(0,4)

    id= models.AutoField(primary_key=True, null=False, blank=False)
    user= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    blog= models.ForeignKey(Blog, null=False, blank=False, on_delete=models.CASCADE)#매칭될 게시글의 pk
    tag= models.TextField()#태그 이름

    text_color=models.CharField(max_length=100, default=Tag_TextColors[i])#글자 색
    background_color=models.CharField(max_length=100, default=Tag_BackgroundColors[j])#배경색
    
    def __str__(self):
        return self.tag

class Applied(models.Model):
    tag=models.TextField()#태그 이름, unique 옵션을 주지 않았으므로, 객체마다 등록되고 삭제시 하나씩 삭제 가능

        