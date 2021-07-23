from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm ,LoginForm ,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.

#Home
def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

#View
def about(request):
    return render(request,'blog/about.html')

#Contact
def contact(request):
    return render(request,'blog/contact.html')

#dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user =request.user
        full_name =user.get_full_name()
        gps=user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,"groups":gps})
    else :
        return HttpResponseRedirect('/login/')


#user_logout
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/login/')

#signup
def user_signup(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations !! You have become an Author")
            user=form.save()
            group=Group.objects.get(name="Author")
            user.groups.add(group)
    else:
        form=SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

#login
def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    else:
        if request.method=="POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user:
                    login(request,user)
                    messages.success(request,'Logged in successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        form=LoginForm()
        return render(request,'blog/login.html',{'form':form})

def user_edit(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            form=PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,'Updated post  successfully !!')
                return HttpResponseRedirect('/dashboard/')
        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)
        return render(request,'blog/editpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def user_delete(request,id):
    if request.user.is_authenticated:
        pi=Post.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Deleted post  successfully !!')
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

def addpost(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=PostForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Added post  successfully !!')
                return HttpResponseRedirect('/dashboard/')
        else:
            form=PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

