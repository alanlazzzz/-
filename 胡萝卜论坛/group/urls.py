"""group URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views 
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views as app01_v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', app01_v.home),
    path('login/', app01_v.login),
    path('register/', app01_v.register),
    path('app01/ajax/uniqueAccount/<str:account>', app01_v.uniqueAccount),
    path('logout/',app01_v.logout),
    
    path('search/',app01_v.search),
    # path('Comment/',app01_v.Comment),
    path('index/', app01_v.index),
    path('index/submit/', app01_v.submit), 
    path('index/saveHeader/', app01_v.saveHeader),
    path('index/saveSignature/<str:Signature>',app01_v.saveSignature),
    path('detailpage/<str:infoid>/',app01_v.detailpage),
    path('gotodetailpage/',app01_v.gotodetailpage),
    
#    <---------6.28-李鑫--start------>
    path('search/',app01_v.search),
#    <---------6.28-李鑫--end-------->
    # path('gotocomment/',app01_v.gotocomment),
    path('comment/<str:infoid>',app01_v.comment),
    
    path('showArticle/<str:kind>/',app01_v.showArticle),
    path('showComment/<str:infoid>/',app01_v.showComment),
    path('gotoShowArticle/',app01_v.gotoShowArticle),

    # ------music--------------
    path('music/',app01_v.music),
    path('m1/',app01_v.m1),
    path('m2/',app01_v.m2),
    path('m3/',app01_v.m3),
    path('m4/',app01_v.m4),
    path('m5/',app01_v.m5),
    path('m6/',app01_v.m6),
    path('m7/',app01_v.m7),
    path('m8/',app01_v.m8),
    path('m9/',app01_v.m9),

    #------------movie-----------
    path('movie/',app01_v.movie),
    path('moviepages_spider-man/',app01_v.moviepage),

    # <------详情页点赞----->
    path('praise_status/<str:infoid>',app01_v.praise_status),
    path('praiscounr/<str:infoid>/', app01_v.praise),

    # <-------book--------->
    path('book/',app01_v.book),
    path('book/b1/',app01_v.b1),
    path('book/b2/',app01_v.b2),
    path('book/b3/',app01_v.b3),
    path('book/b4/',app01_v.b4),
    path('book/b5/',app01_v.b5),
    path('book/b6/',app01_v.b6),
    path('book/b7/',app01_v.b7),
    path('book/b8/',app01_v.b8),
]
