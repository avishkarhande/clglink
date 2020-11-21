from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from website.models import Profile,Education,work,Skills,achievement,Notification
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from website.forms import profilepic
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random
from random import shuffle
from django.views.defaults import page_not_found

import os
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        context = {}
        profile = Profile.objects.all()
        works = work.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(profile, 1)
        notifications = Notification.objects.filter(user=request.user)
        notiall = Notification.objects.all()
        curr_user_profile = Profile.objects.get(user=request.user)
        count = 0
        for n in notifications:
            count+=1
        try:
            profile = paginator.page(page)
        except PageNotAnInteger:
            profile = paginator.page(1)
        except EmptyPage:
            profile = paginator.page(paginator.num_pages)
        context['profile'] = profile
        context['count'] = count
        context['notifications'] = notifications
        context['curr_user_profile'] = curr_user_profile
        return render(request, 'index.html', context)
    else:
        return render(request,'home.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if(request.method == 'POST'):
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account Created For ' + user )
                return redirect('login')

        context = {'form':form}
        return render(request,'register.html',context)


def loginPage(request):
    User = get_user_model()
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method=='POST':
            email = request.POST['email']
            password = request.POST['pswrd']
            username = User.objects.get(email=email.lower()).username
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                messages.error(request,'Incorrect Credentials')
                return redirect('login')
        context = {}
        return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def myprofile(request):
    if request.user.is_authenticated:
        skill = Skills.objects.filter(user=request.user)
        desc = Profile.objects.get(user=request.user)
        edu = Education.objects.filter(user=request.user).reverse()
        works = work.objects.filter(user=request.user).reverse()
        achievements = achievement.objects.filter(user = request.user).reverse()
        curr_user_profile = Profile.objects.get(user=request.user)
        notifications = Notification.objects.filter(user=request.user)
        count = len(notifications)
        context = {'skill':skill,'desc':desc,'edu':edu,'works':works,'achievements':achievements}
        context['count'] = count
        context['curr_user_profile'] = curr_user_profile
        return render(request,'myprofile.html',context)
    else:
        return HttpResponse("You Must Login To View This Page")

def updateskill(request):
    if request.method=='POST':
        skill = request.POST['skill']
        username = request.POST['uname']
        skills = Skills.objects.filter(user=request.user).exists()
        if skills:
            new_skills = Skills.objects.filter(user=request.user)
            for s in new_skills:
                if s.skill == skill:
                    messages.warning(request,'Skill Already Exists')
                    return redirect('myprofile')
            b = Skills(skill=skill,user=request.user)
            b.save()
            messages.success(request,'Skill Added Successfully')
            return redirect('myprofile')
            return redirect('myprofile')
        else:
            if(skills is not None):
                b = Skills(skill=skill,user=request.user)
                b.save()
                messages.success(request,'Skill Added Successfully')
                return redirect('myprofile')
            else:
                
                return redirect('myprofile')

    else:
        return redirect('index')

def addbio(request):
    if request.method == 'POST':
        bio = request.POST['bio']
        username = request.POST['uname']
        user = User.objects.get(username=username)
        Profile.objects.filter(user=user).update(desc=bio)
        messages.success(request,'Bio Updated Successfully')
        return redirect('myprofile')
    else:
        return redirect('index')
            
def initialreg(request):
    if request.method == 'POST':
        fname = request.POST.get('fname',False)
        lname = request.POST.get('lname',False)
        email = request.POST.get('email',False)
        number = request.POST.get('phone',False)
        gender = request.POST.get('gender',False)
        username = request.POST['uname']
        password = request.POST['pswrd1']
        password2 = request.POST['pswrd2']
        pub = request.POST['public']
        if pub=='1':
            public = 1
        else:
            public=0
        name = fname+' '+lname
        if password!=password2:
            messages.error(request, "Passwords didn't match" )
            return redirect('register')
        if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
            User.objects.create_user(username,email,password)
            user = User.objects.get(username=username)
            profile = Profile(name=name,user=user,phone=number,is_phone=public)
            profile.save()
            messages.success(request,'Account Created Successfully')
            return redirect('login')
        else:
            if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
                messages.error(request, "Account with this Username and Email Exists" )
                return redirect('register')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Account with this Username Exists" )
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request, "Account with this Email Exists" )
                return redirect('register')
        return render(request,'myprofile.html')
    else:
        return redirect('index')

def add_edu(request):
    if request.method == 'POST':
        name = request.POST["edu-name"]
        degree = request.POST["edu-degree"]
        span = request.POST["edu-span"]
        user = request.user
        edu = Education(name=name,degree=degree,span=span,user=user)
        edu.save()
        messages.success(request,'Education Added Successfully')
        return redirect('myprofile')

def updateindividualskill(request,id=id):
    skill = Skills.objects.get(id=id)
    context = {'skill':skill}
    return render(request,'updateskill.html',context)

def profile(request,slug):
    if request.user.is_authenticated:
        user = User.objects.get(username=slug)
        profile = Profile.objects.get(user=user)
        skill = Skills.objects.filter(user=user)
        education = Education.objects.filter(user=user)
        works = work.objects.filter(user=user)
        achievements = achievement.objects.filter(user=user)
        notifications = Notification.objects.filter(user=request.user)
        count = len(notifications)
        curr_user_profile = Profile.objects.get(user=request.user)
        number_of_records = Profile.objects.count()
        random_index = int(random.random()*number_of_records)+1
        random_user = Profile.objects.get(sno=random_index)
        while(random_user.user==request.user or random_user.user==profile.user):
            number_of_records = Profile.objects.count()
            random_index = int(random.random()*number_of_records)+1
            random_user = Profile.objects.get(sno=random_index)
        
        context = {'profile':profile,'skill':skill,'count':count,'education':education,'works':works,'achievements':achievements,'random_user':random_user}
        context['curr_user_profile'] = curr_user_profile
        
        if request.user==user:
            return render(request,'profile.html',context)
        else:
            name = Profile.objects.get(user=request.user)
            msg = "Your Profile was viewed by " + name.name
            notific = Notification(notification=msg,user=user)
            notific.save()
            return render(request,'profile.html',context)
    else:
        return HttpResponse("Login To View Profiles")



def updateprofile(request,slug):
    user = User.objects.get(username=slug)
    profile = Profile.objects.get(user = user)
    if request.method == 'POST':
        user = User.objects.get(username=slug)
        form = profilepic(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Pic Successfully')
            return redirect('myprofile')
        else:
            messages.error(request,"Please Upload Image less than 5mb")
            return redirect('myprofile')
    else:    
        form = profilepic(instance=profile)
        user = User.objects.get(username=slug)
        context = {'profile':profile,'form':form}
        return render(request,'updateprofile.html',context)
    
def deleteindividualskill(request,id=id):
    skill = Skills.objects.get(id=id)
    skill.delete()
    return redirect('myprofile')

def updateedu(request,id=id):
    edu = Education.objects.get(id=id)
    context = {'edu':edu}
    return render(request,'updateedu.html',context)

def updatework(request,id=id):
    w = work.objects.get(id=id)
    context = {'works':w}
    return render(request,'updatework.html',context)

def add_work(request):
    if request.method == 'POST':
        name = request.POST["work-name"]
        workss = request.POST["work-work"]
        span = request.POST["work-span"]
        user = request.user
        works = work(name=name,work=workss,span=span,user=user)
        works.save()
        messages.success(request,'Work Added Successfully')
        return redirect('myprofile')
    else:
        return redirect('myprofile')

def updatededu(request,id=id):
    if request.method=='POST':
        edu = Education.objects.get(id=id)
        name = request.POST['name']
        degree = request.POST['degree']
        span = request.POST['span']
        edu.name = name
        edu.degree = degree
        edu.span = span
        edu.save()
        messages.success(request,'Education Updated Successfully')
        return redirect('myprofile')
    else:
        return redirect('index')

def updatedwork(request,id=id):
    if request.method=='POST':
        works = work.objects.get(id=id)
        name = request.POST['name']
        workss = request.POST['work']
        span = request.POST['span']
        works.name = name
        works.work = workss
        works.span = span
        works.save()
        messages.success(request,'Work Updated Successfully')
        return redirect('myprofile')
    else:
        return redirect('index')


#delete 

def deletework(request,id=id):
    if request.user.is_authenticated:
        works = work.objects.get(id=id)
        works.delete()
        messages.success(request,'Work Deleted Successfully')
    return redirect('myprofile')

def deleteedu(request,id=id):
    if request.user.is_authenticated:
        edu = Education.objects.get(id=id)
        edu.delete()
        messages.success(request,'Education Deleted Successfully')
        return redirect('myprofile')
    else:
        return redirect('index')


def addachievement(request):
    if request.method=='POST':
        achievement1 = request.POST['achievement']
        user = request.user
        achieve = achievement(achievement=achievement1,user=user)
        achieve.save()
        messages.success(request,'Achievement Saved Successfully')
        return redirect('myprofile')
    else:
        return redirect('index')

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        count = 0
        for n in notifications:
            count+=1
        curr_user_profile = Profile.objects.get(user=request.user)
        context = {'notifications':notifications,'count':count,'curr_user_profile':curr_user_profile}
        return render(request,'notifications.html',context)
    else:
        return redirect('index')

def deletenotifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.all()
        notifications.delete()
        return redirect('index')
    else:
        return redirect('index')

def passchange(request):
    return render(request,'passchange.html')

def changepassword(request):
    if request.method=='POST':
        current = request.POST["current"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if request.user.password==current:
            if password1==password2:
                request.user.password = password1
                return redirect('passchange')
            else:
                messages.error(request,"Passwords dont match")
                return redirect('passchange')
        else:
            messages.error(request,"The Password Entered is wrong")
            return redirect('passchange')
def addsocialmedia(request):
    if request.method=='POST':
        profile = Profile.objects.get(user=request.user)
        linkedin = request.POST['linkedin']
        facebook = request.POST['facebook']
        instagram = request.POST['instagram']
        profile.linkedin = linkedin
        profile.facebook = facebook
        profile.instagram = instagram
        profile.save()
        return redirect('myprofile')
    else:
        return redirect('index')

def settings(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        count = len(notifications)
        curr_user_profile = Profile.objects.get(user=request.user)
        context = {'count':count,'curr_user_profile':curr_user_profile}
        context['curr_user_profile'] = curr_user_profile   
        return render(request,'settings.html',context)
    else:
        return redirec('index')

def updateusername(request):
    if request.method=='POST':
        uname = request.POST['uname']
        check_user = User.objects.filter(username=uname)
        if check_user:
            messages.error(request,"Username is already taken")
            return redirect('myprofile')
        else:
            get_user = User.objects.get(username=request.user.username)
            get_user.username = uname
            profile = Profile.objects.get(user=request.user)
            profile.slug = uname
            profile.save()
            get_user.save()
            messages.success(request,"Username Changed Successfully")
            return redirect('myprofile')
    else:
        return redirect('index')



def search(request):
    res = []
    query = request.GET['query']
    query = query.split(" ")
    for q in query:
        profile = Profile.objects.filter(name__icontains=q)
        for p in profile:
            res.append(p)
        skills = Skills.objects.filter(skill__icontains=q)
        for s in skills:
            getuser = s.user
            pro = Profile.objects.get(user=getuser)
            res.append(pro)
    new_res = []
    for r in res:
        if r not in new_res:
            new_res.append(r)
        else:
            continue
    notifications = Notification.objects.filter(user=request.user)
    count = len(notifications)
    curr_user_profile = Profile.objects.get(user=request.user)    
    
    context = {'profile':new_res,'count':count,'curr_user_profile':curr_user_profile}
    return render(request,'search.html',context)

def updatephone(request):
    if request.method=='POST':
        phone = request.POST['phone']
        if phone=='':
            phone = None

        is_phone = request.POST['public']
        profile = Profile.objects.get(user=request.user)
        profile.phone = phone
        if is_phone == '1':
            profile.is_phone = 1
        else:
            profile.is_phone = 0
        profile.save()
        return redirect('myprofile')
    else:
        return redirect('index')

def updateyear(request):
    if request.method=='POST':
        year = request.POST['year']
        profile = Profile.objects.get(user=request.user)
        profile.year = year
        profile.save()
        messages.success(request,"Year Of Study Updated Succcessfully!")
        return redirect('myprofile')
    else:
        return redirect('index')



def handler_404(request, exception):
    return render(request,'404.html')


