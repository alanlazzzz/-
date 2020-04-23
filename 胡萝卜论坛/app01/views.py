from django.shortcuts import render, redirect
from django.http import HttpResponse
from app01.models import *
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
import os
import uuid
from app01.models import *
import time
import markdown
import requests
from lxml import etree
from django.views.decorators.csrf import csrf_exempt 
import re
def addi(data):
    status = 0
    html = ''
    k=0
    for i in data:
        if status == 0:
            if i == '<':
                status=1
            else:
                status=0
        elif status == 1:
            if i == 'h':
                status=2
            else:
                status=0
        elif status==2:
            if i == '2':
                status=3
            else:
                status=0
        elif status==3:
            if i == '>':
                status=4
            else:
                status=0
        if status == 4:
            html += ' '
            html += "id='i"
            html += str(k)
            html += "'"
            k += 1
            status = 0
        if status != 4:
            html += i
    return html
# Create your views here.
# 用户数据规则：
# 通过构造字典userdata={}，然后将需要的变量名作为键，变量值作为值存入字典，
# 统一通过context={'userdata':userdata}传到前端
# userdata={
# 	'hradimg':headimg,
# 	'account':account,
# }


def login(request):
    if request.POST:
        account = request.POST.get('account', None)
        password = request.POST.get('passwd', None)
        rememb_me = request.POST.get('rem', '')
        try:
            user = User.objects.get(account=account)
            if password == user.password:
                response = redirect('/home/')
                # response.set_cookie('tag',1)
                # if rememb_me:

                response.set_signed_cookie('account', account, salt='app')
                response.set_signed_cookie('password', '', salt='app')

                request.session['account'] = account
                request.session['headimg'] = user.headimg
                
                return response
            else:
                return render(request, 'login.html', {'msg': "密码错误！"})
        except:
            return render(request, 'login.html', {'msg': "登录失败！"})
    else:
        account = request.get_signed_cookie('account', '', salt='app')
        password = request.get_signed_cookie('password', '', salt='app')
        if account and password:
            return render(request, 'login.html', {'account': account, 'password': password})
        else:
            return render(request, 'login.html')


def logout(request):
    del request.session['account']
    return redirect('/home/')


def register(request):
    if request.POST:
        account = request.POST.get('account', '')
        password1 = request.POST.get('passwd', '')
        password2 = request.POST.get('vertipasswd', '')
        nickname = request.POST.get('nickname', '')
        gender = request.POST.get('sex', '')
        year = request.POST.get('year', '')
        month = request.POST.get('month', '')
        day = request.POST.get('day', '')
        birthday = year+'.'+month+'.'+day
        location = request.POST.get('location', '')
        headimg = 'default_photo.png'
        if password1 == password2:
            try:
                user = User(account=account, password=password1, nickname=nickname,
                            gender=gender, birthday=birthday, location=location, headimg=headimg)
                user.save()
                return render(request, 'login.html', {'msg': "注册成功，请登录"})
            except:
                return render(request, 'register.html', {'msg': "注册失败！"})
    else:
        return render(request, 'register.html')


def home(request):
	# account=request.session.get('account', '')
	# if account:
	headimgPath = 'imgs/'+request.session.get('headimg', '')
	userdata = {'headimg':headimgPath}
	if request.get_signed_cookie('account', None, salt='app') == request.session.get('account', ''):
		userdata['tag'] = 1
		return render(request, 'homepage.html', {'userdata': userdata})
	else:
		userdata['tag'] = 0
		userdata['headimg'] = ''
		return render(request, 'homepage.html', {'userdata':userdata})

    # else:
        # return redirect('/login/')


def uniqueAccount(request, account):
    users = User.objects.all()
    flag = 0
    for user in users:
        
        if account == user.account:
            flag = 1
    return HttpResponse(flag)



def index(request):
    ####################构造用户数据
    userdata = {}
    account = request.session.get('account', '')
    user = User.objects.filter(account=account)[0]
    account1 = User.objects.get(account=account)
    nickname=account1.nickname
    if request.get_signed_cookie('account', None, salt='app') == account:
        # <---------------读取签名 start------------------>
        obj = User.objects.get(account = account)
        print("--------------------account-----------------")
        print(account)
        path = obj.signature
        if path != '0':
            uploadTextPath = os.path.join(os.getcwd(), 'app01\\static\\uploadtext') + os.sep + path
            content = ''
            with open(uploadTextPath,'r') as f:
                content = f.read()
                userdata['signature'] = content
            # <---------------读取签名 end------------------>
        userdata['headimg'] = 'imgs/'+request.session.get('headimg', '')
        userdata['tag'] = 1

        #6.29照片墙
        # 获取用户最近六条动态数据
        Pic = Info.objects.filter(user_id = account).order_by("-infoid")[0:16]
        lstpath = list() # 格式转换时暂存用
        newlst = list()
        for i in range(16):
            try:
            # ----------------------图片处理-------------
                strpic = Pic[i].picid          # 获取picid数据
                # print("------------------------strpic----------------------")
                # print(strpic)
                # 进行数据格式转换{ 图片列表-> 有效路径 }
                lstpic = strpic[1:-1].split(',')
                imgpath = r"uploadimg/" + lstpic[0].replace("'","").replace(" ","")
                if imgpath == 'uploadimg/':
                    lstpath.append(None)
                else:
                    lstpath.append(imgpath)
            
            # ----------------------文本处理-----------------
                textpath = Pic[i].textid
                # 拼接文本文件的全部路径
                textFullPath = os.path.join(os.getcwd(), 'app01\\static\\uploadtext\\') + textpath
                with open(textFullPath, 'r') as f:
                    # print("---------------------------textbegin----------------------")
                    txtContext = f.read()
                    # 使用正则表达式进行动态简介爬取
                    try:
                        pattern = r'<h1(.*?)>(.*?)</h1>' # 匹配规则
                        # 匹配完成后转换成可用字符串
                        try:
                            result = re.match(pattern, txtContext).group(0)
                            result = result.replace("<h1>", "").replace("</h1>", "")
                        # result = result.replace("<h2>", "").replace("</h2>", "")
                        # result = result.replace("<h3>", "").replace("</h3>", "")
                        # result = result.replace("<h4>", "").replace("</h4>", "")
                        # result = result.replace("<h5>", "").replace("</h5>", "")
                        except:
                            result = None
                        print(result)
                    except:
                        print("无法进行匹配操作")
                    print("---------------------------textend----------------------")
                # 对空信息的处理
                if result == None:
                    newlst.append({"picid":lstpath[i]})
                    newlst[i]["text"] = None
                else:
                    newlst.append({"picid":lstpath[i]})
                    newlst[i]["text"] = result
            except:
                newlst.append({"picid":None})
        # 创建返回字典
        context = dict()
        # 数据存取
        context["piclstpath"] = newlst
        context["userdata"] = userdata
        context["nickname"] = nickname

        print(context)

        return render(request, "index.html", context)
    else:
        userdata['tag'] = 1
        return HttpResponse("<h1>Permission Denied!</h1>")
    


def submit(request):
    # obj = request.FILES.get('pic',None)
    log_title = request.POST.get('Name', None)
    log_kinds = request.POST.get('kinds', None)
    log_content = request.POST.get('Message', None)
    extensions = ['markdown.extensions.extra','markdown.extensions.tables', 'markdown.extensions.codehilite']
    log_content = markdown.markdown(log_content, extensions=extensions)
    html = etree.HTML(log_content)
    urls = html.xpath("//@src")
    names = []
    if len(urls) != 0:
        uploadPicPath = os.path.join(os.getcwd(), 'app01\\static\\uploadimg')
        try:
            for url in urls:
                response = requests.get(url)
                name = str(uuid.uuid1()) + '.' + url.split(".")[-1]
                uploadPicFullPath = uploadPicPath + os.sep + name
                with open(uploadPicFullPath, "wb") as f:
                    f.write(response.content)
                    names.append(name)
            names = str(names)
        except:
            userdata['error_msg'] = '请上传正确的网络图片'
            return render(request, 'index.html', {'userdata':userdata})
			# 生成唯一文件名
    uuidd = str(uuid.uuid1())
    uniqueTextName = uuidd + '.html'
    uploadTextPath = os.path.join(os.getcwd(), 'app01\\static\\uploadtext')
    if not os.path.exists(uploadTextPath):
        os.mkdir(uploadTextPath)
    uploadTextFullPath = uploadTextPath + os.sep + uniqueTextName
    try:
        # 写入文件数据
        with open(uploadTextFullPath, "w") as textf:
            textf.write(log_content)

            account = request.session.get('account','')
            user = User.objects.filter(account=account)[0]
            submit = Info(
                user = user,
                picid=names,
                textid=uniqueTextName,
                date=time.time(),
                praisecounr='0',
                title=log_title,
                kinds=log_kinds)
            submit.save()
        response = redirect('/index/')
        return response
    except:
        return response


@csrf_exempt
def saveHeader(request):
	obj = request.FILES.get('headimg', None)
	# 判断对象是否为空
	if(obj != None):
		# 获取头像图片
		stuff = os.path.splitext(obj.name)[1]
		# 检验头像是否合法
		allowedTypes = ['.png', '.jpg', '.gif', '.jpeg', '.bmp']
		if stuff.lower() not in allowedTypes:
			return render(request, "index.html")
		# 构造uuid
		uniqueName = str(uuid.uuid1()) + stuff
		# 构造路径
		uploadDirPath = os.path.join(os.getcwd(), 'app01\\static\\imgs')
		# 如果不存在则创建文件
		if not os.path.exists(uploadDirPath):
			os.mkdir(uploadDirPath)
		# 构造图片地址
		uploadFileFullPath = uploadDirPath + os.sep + uniqueName
		# 修改头像
		try:
			with open(uploadFileFullPath, "wb+") as f:
				for chumk in obj.chunks():
					f.write(chumk)
				f.close()
				user = User.objects.get(account=request.session.get('account', ''))
				user.headimg =  uniqueName
				user.save()
				request.session['headimg'] =  "/" + uniqueName
				return HttpResponse("")
		except:
			return HttpResponse("dsa")

# 保存签名控制函数

@csrf_exempt
def saveSignature(request, Signature):
        # 构造路径
    sigPath = os.path.join(os.getcwd(), 'app01\\static\\uploadtext')
    signame = str(uuid.uuid1())+'.txt'
    sigFullPath = sigPath+os.sep+signame
    print("<--------"+sigFullPath+"------->")
    # 写入签名文件
    with open(sigFullPath, 'w') as fp:
        fp.write(Signature)
    account = request.session.get('account',None)
    print("<--------"+account+"------->")
    obj = User.objects.filter(account=account)
    print("<--------"+str(len(obj))+"------->")
    obj[0].signature = signame
    obj[0].save()
    # 返回签
    return HttpResponse(Signature)

# 从breifpage跳转到detialpage


def gotodetailpage(request):
    userdata = {}
    # 从url中？infoid=value得到infoid
    # infoid = request.GET.get('infoid', None)
    # # 跳转到detialpage并且替换{{ infoid }}
    headimgPath = 'imgs/'+request.session.get('headimg', '')
    infoid = request.GET.get('infoid',None)
    
    if request.get_signed_cookie('account', None, salt='app') == request.session.get('account', ''):
        userdata['tag'] = 1
        userdata['infoid'] = infoid
        userdata['headimg'] = headimgPath
        # print(userdata['headimg'])
        return render(request, 'detailpage.html', {'userdata': userdata})
    else:
        userdata['tag'] = 0
        userdata['headimg'] = 'imgs/default_photo.png'
        userdata['infoid'] = infoid
        return render(request, 'detailpage.html', {'userdata':userdata})

# jquery Ajax加载文章时的响应控制函数


def detailpage(request, infoid):
        # 以infoid查询记录
    obj = Info.objects.filter(infoid=int(infoid))
    # 判断记录是否为空
    if len(obj) != 0:
        html = ''
        # 构造详细文章路径
        fullpath = os.path.join(os.getcwd(), "app01\\static\\uploadtext\\")
        fullpath = (fullpath + obj[0].textid)
        # 读取详细文章，以富文本格式
        with open(fullpath, 'r') as f:
            html = f.read()
            # 返回Ajax请求
        
        return HttpResponse(addi(html))
    else:
        return HttpResponse("暂无数据")


def search(request):
    if request.POST:
        q=request.POST.get('ppt')
        post_list=Info.objects.filter(title__icontains=q)
        lst = []
        for item in post_list:
            if item.picid == None:
                lst.append([item.title,None,'/gotodetailpage/?infoid='+str(item.infoid)])
            else:
                path_str = item.picid
                path_str = path_str[1:-1]
                path_list = path_str.split(',')
                path = path_list[0]
                path = path[1:-1]
                lst.append([item.title,'uploadimg/' + path ,'/gotodetailpage/?infoid='+str(item.infoid)])
        headimgPath = 'imgs/'+request.session.get('headimg', '')
        userdata = {'headimg':headimgPath}
        if request.get_signed_cookie('account', None, salt='app') == request.session.get('account', ''):
            userdata['tag'] = 1
            return render(request, 'search.html', {'userdata': userdata, 'lst':lst})
        else:
            userdata['tag'] = 0
            userdata['headimg'] = ''
            return render(request, 'search.html', {'userdata':userdata, 'lst':lst})
    else:
        return HttpResponse("<h1>Permission Denied!</h1>")



# <--------xuahi-6.29---------->
# def gotocomment(request):
#     headimgPath = 'imgs/'+request.session.get('headimg', '')
#     userdata = {'headimg':headimgPath}
#     if request.get_signed_cookie('account', None, salt='app') == request.session.get('account', ''):
#         userdata['tag'] = 1
#         return render(request, 'comment.html', {'userdata': userdata})
#     else:
#         userdata['tag'] = 0
#         userdata['headimg'] = ''
#         return render(request, 'comment.html', {'userdata':userdata})

def comment(request,infoid):
        # 只有在登陆成功的时候才能发送请求
    response = redirect("/gotodetailpage/?infoid="+infoid)
    if request.get_signed_cookie('account', None, salt='app') == request.session.get('account', ''):
            
        text = request.POST.get('texts',None)
        # infoid = request.GET.get('infoid',None)

        extensions = ['markdown.extensions.extra','markdown.extensions.tables', 'markdown.extensions.codehilite']
        text = markdown.markdown(text, extensions=extensions)
        name = str(uuid.uuid1()) + '.html'
        uploadTextPath = os.path.join(os.getcwd(), 'app01\\static\\uploadtext')
        uploadTextFullPath = uploadTextPath + os.sep + name
        with open(uploadTextFullPath, "w") as f:
            f.write(text)
        account = request.session.get('account', '')
        
        user = User.objects.filter(account = account)[0]
        # print(infoid,type(infoid))
        info = Info.objects.filter(infoid = infoid)[0]
        # comobj = Comment.objects.filter(account = account)[0]
        obj = Comment(content = name,
                        commenter = user,
                        date = time.time(),
                        info = info)      
        obj.save()
        
        return response
    else:
        return response


def showArticle(request,kind):
    obj_list = Info.objects.filter(kinds=kind)
    fullpath = os.path.join(os.getcwd(), "app01\\static\\uploadtext\\")
    content_list = []
    for obj in obj_list:
        path = fullpath + obj.textid
        title = obj.title
        infoid = obj.infoid
        user = obj.user.nickname
        with open(path,'r') as f:
            html = etree.HTML(f.read())
            text = html.xpath('string(.)')
            if len(text) >=350:
                content_list.append((text[0:300],title,str(infoid),user))
            else:
                content_list.append((text,title,str(infoid),user))
    finalHtml = ''
    for i in content_list:
        # show article-wwwwwww
        pre = "<ul id='comment-box-style' style='text-align: left;border:2px solid grey;border-radius:10px;'><li style='list-style:none;'><a id='comment-title-style' href=" + "/gotodetailpage/?infoid="+ i[2]+" >"+ i[1] +"</a><br><a id='comment-author-style' href = ''>" +i[3]+"</a><p>"
        end = "</p></li></ul>"
        finalHtml += pre
        finalHtml += '<div>' + i[0] + '</div><br>'
        finalHtml += end
        # content_list.append()
    
    return HttpResponse(finalHtml)


def showComment(request,infoid):
    obj_list = Comment.objects.filter(info_id=int(infoid))
    fullpath = os.path.join(os.getcwd(), "app01\\static\\uploadtext\\")
    content_list = []
    for obj in obj_list:
        content = obj.content
        commenter_id = obj.commenter_id
        content = obj.content
        path = fullpath + content
        with open(path,'r') as f:
            html = etree.HTML(f.read())
            text = html.xpath('string(.)')
            if len(text) >=300:
                content_list.append((text[0:300],commenter_id))
            else:
                content_list.append((text,commenter_id))
    finalHtml = ''
    for i in content_list:
        end = "</p></li></ul>"
        pre = "<ul style='text-align: left;border:2px solid grey;border-radius:10px;'><li style='list-style:none'><br><a id='comment-author-style' href = ''>" +i[1]+"</a><p>"
        finalHtml += pre
        finalHtml += '<div>' + i[0] + '</div><br>'
        finalHtml += end
        # content_list.append()
    
    return HttpResponse(finalHtml)



def gotoShowArticle(request):
    return render(request,'showArticle.html')

def movie(request):
    headimgPath = 'imgs/'+request.session.get('headimg', '')
    userdata = {'headimg':headimgPath}
    if request.get_signed_cookie('account', None, salt='app') == request.session.get('account', ''):
        userdata['tag'] = 1
        return render(request, 'moviehomepage.html', {'userdata': userdata})
    else:
        userdata['tag'] = 0
        userdata['headimg'] = ''
        return render(request, 'moviehomepage.html', {'userdata':userdata})

#------------------------music-------------------------------------
def music(request):
    headimgPath = 'imgs/'+request.session.get('headimg', '')
    userdata = {'headimg':headimgPath}
    if request.get_signed_cookie('account', None, salt='app') == request.session.get('account', ''):
        userdata['tag'] = 1
        return render(request, 'musichomepage.html', {'userdata': userdata})
    else:
        userdata['tag'] = 0
        userdata['headimg'] = ''
        return render(request, 'musichomepage.html', {'userdata':userdata})

def m1(request):
    return render(request,'m1.html')
def m2(request):
    return render(request,'m2.html')
def m3(request):
    return render(request,'m3.html')
def m4(request):
    return render(request,'m4.html')
def m5(request):
    return render(request,'m5.html')
def m6(request):
    return render(request,'m6.html')
def m7(request):
    return render(request,'m7.html')
def m8(request):
    return render(request,'m8.html')
def m9(request):
    return render(request,'m9.html')
        



# <------------------详情页点赞------------------>
@csrf_exempt
def praise(request,infoid):
    L = request.session.get('praise',None)
    if L == None:
        L=[infoid]
        request.session['praise'] = L
    else:
        L.append(infoid)
    print(str(request.session['praise']))
	# request.session.set_expiry(5)
		
	# infoid = '4'
    info = Info.objects.get(infoid=infoid)
    if not info.praisecounr:
        info.praisecounr='0'
    info.praisecounr=str(int(info.praisecounr)+1)
    info.save()
    return HttpResponse("")


def praise_status(request,infoid):
    L = request.session.get('praise',None)
    if L == None:
        return HttpResponse('0')
    else:
        for i in L:
            if i == infoid:
                return HttpResponse('1')
            return HttpResponse('0')


# <------------------详情页点赞 结束------------------>

#-----------------------book-----------------------
def book(request):
    headimgPath = 'imgs/'+request.session.get('headimg', '')
    userdata = {'headimg':headimgPath}
    if request.get_signed_cookie('account', None, salt='app') == request.session.get('account', ''):
        userdata['tag'] = 1
        return render(request, 'bookhomepage.html', {'userdata': userdata})
    else:
        userdata['tag'] = 0
        userdata['headimg'] = ''
        return render(request, 'bookhomepage.html', {'userdata':userdata})

def moviepage(request):
    headimgPath = 'imgs/'+request.session.get('headimg', '')
    userdata = {'headimg':headimgPath}
    if request.get_signed_cookie('account', None, salt='app') == request.session.get('account', ''):
        userdata['tag'] = 1
        return render(request, 'moviepages_spider-man.html', {'userdata': userdata})
    else:
        userdata['tag'] = 0
        userdata['headimg'] = ''
        return render(request, 'moviepages_spider-man.html', {'userdata':userdata})   


def b1(request):
    return render(request,'b1.html')

def b2(request):
    return render(request,'b2.html')

def b3(request):
    return render(request,'b3.html')

def b4(request):
    return render(request,'b4.html')

def b5(request):
    return render(request,'b5.html')

def b6(request):
    return render(request,'b6.html')

def b7(request):
    return render(request,'b7.html')

def b8(request):
    return render(request,'b8.html')


