from django.db import models



class User(models.Model):
    account = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=10)
    nickname = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, default='famle')
    birthday = models.CharField(max_length=30, default='2000/1/1')
    location = models.CharField(max_length=50, default=0)
    headimg = models.CharField(max_length=100, default=0)
    signature = models.CharField(max_length=100, default=0)
  
    pass


class Info(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    infoid = models.AutoField(primary_key=True)
    picid = models.CharField(max_length=1000)
    textid = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    praisecounr = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    kinds = models.CharField(max_length=100)
    

    pass

class Comment(models.Model):
    commentid = models.AutoField(primary_key=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    pass







    
