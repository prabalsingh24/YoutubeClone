from django.shortcuts import render
from django.views.generic.base import View,HttpResponse,HttpResponseRedirect
from .forms import LoginForm,RegisterForm,AddVideoForm,CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .models import Video,Comment
from django.utils import timezone
import random,string
from django.contrib.auth.decorators import login_required
# Create your views here.

class HomeView(View):
    template_name='home.html'
    def get(self,request):
        variable = "NEWVIDEO"
        videos = Video.objects.order_by('-datetime')
        print(videos)
        return render(request, 'home.html', {'videos': videos})


    def post(self,request):
        return HttpResponse('<h1>THis is the post</h1>')
##@login_required
class AddVideo(View):
    template_name='NewVideo.html'

    def get(self,request):
        variable = "NEWVIDEO"
        if request.user.is_authenticated:
            form = AddVideoForm()
            return render(request, self.template_name, {'form': form})
        else:
            print("USER NOT LOGGED IN ")
            return HttpResponseRedirect('/login')
    def post(self,request):
        ##form = AddVideoForm(request.POST, request.FILES)
        form = AddVideoForm(request.POST, request.FILES)
        ##print(request.POST)
        print(request.FILES)

        if form.is_valid():
            print("HEELLEEELOO")

            title=form.cleaned_data['title']
            description=form.cleaned_data['description']
            file=form.cleaned_data['file']
            randomchar=''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            path=randomchar+file.name
            new_video=Video(title=title,description=description,path=path,user=request.user,datetime=timezone.now())
            print(dir(new_video))
            new_video.save()
            print("VIDEO SAVED")
            return HttpResponseRedirect('/')
        else:
            print("FORM NOTD VALID")
        return HttpResponse('<h1>THis is the post</h1>')

class LoginView(View):
    template_name='Login.html'
    def get(self,request):
        variable = "NEWVIDEO"
        if request.user.is_authenticated:
            print('already logged in ..... ')
            print(request.user)
            return HttpResponseRedirect('/')
        form = LoginForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        print(request)
        print("hello this is post")
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['name']
            password =form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                #create a new entry in table log
            else:
                return  HttpResponse('<h1> invalid password</h1>')
            print(password)
            return HttpResponseRedirect('/')
        return HttpResponse('<h1>THis is the post</h1>')

class RegisterView(View):
    template_name='register.html'
    def get(self,request):
        variable = "NEWVIDEO"
        if request.user.is_authenticated:
            print("USER IS ALREADY LOGGED IN aaaaa")
            print(request.user)
            return HttpResponseRedirect('/')
        form = RegisterForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['name'])
            username=form.cleaned_data['name']
            password=form.cleaned_data['password']
            email=form.cleaned_data['youremail']
            newuser=User.objects.create_user(username=username,password=password,email=email)
           ## newuser.save()
            return HttpResponseRedirect('/login')
            #create a user account

        return HttpResponse('<h1>THis is the post</h1>')


class DetailedVideo(View):
    template_name="video.html"
    def get(self,request,id):
        currentVideo=Video.objects.get(id=id)
        comments=Comment.objects.all().filter(video=currentVideo).order_by('-datetime')
        context={
            'video':currentVideo,
            'comments':comments
        }
        if request.user.is_authenticated:
            form=CommentForm()
            context['form']=form
            print("I AM HERE")

        return render(request,self.template_name,context)

class CommentView(View):
    template_name='video.html'
    def post(self,request):
        form = CommentForm(request.POST)
        if form.is_valid():
            print("FORM IS VALID")
            text=form.cleaned_data['text']
            video_id=request.POST['video']
            video=Video.objects.get(id=video_id)
            new_comment=Comment(text=text,datetime=timezone.now(),video=video,user=request.user)
            new_comment.save()
            return HttpResponseRedirect('/video/{}'.format(str(video_id)))
        else:
            video_id = request.POST['video']
            return HttpResponseRedirect('/video/{}'.format(str(video_id)))