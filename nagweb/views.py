from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import tweets
from .forms import tweetform,userregistration


def index_view(request):
    return render(request,'index.html')

def tweet_list(request):
   tweet=tweets.objects.all().order_by('-created_at')
   return render(request,'tweet_list.html',{'tweets':tweet})
@login_required
def tweet_create(request):
    if request.method =='POST':
     form=tweetform(request.POST,request.FILES)
     if form.is_valid():
        tweet=form.save(commit=False)
        tweet.user=request.user
        tweet.save()
        return redirect('tweet_list')
     
    else:
       form=tweetform()
    return render(request,'tweet_form.html',{'form':form})   

@login_required
def tweet_edit(request,tweet_id):
   tweet=get_object_or_404(tweets,pk=tweet_id,user=request.user)

   if request.method=='POST':
       form=tweetform(request.POST,request.FILES,instance=tweet)
       if form.is_valid():
          tweet=form.save(commit=False)
          tweet.user=request.user
          tweet.save()
          return redirect('tweet_list')
   else:
      form=tweetform(instance=tweet)
   return render(request,'tweet_form.html',{'form':form})  

@login_required
def tweet_delete(request,tweet_id):
   tweet=get_object_or_404(tweets,pk=tweet_id,user=request.user)
   if request.method=='POST':
      tweet.delete()
      return redirect("tweet_list")
   return render(request,'tweet_confirm_delete.html',{'tweet':tweet})
 
def register(request):
   if request.method=='POST':
      form=userregistration(request.POST)
      if form.is_valid():
         user=form.save(commit=False)
         user.set_password(form.cleaned_data['password1'])
         user.save() 
         login(request,user)
         return redirect('tweet_list')

   else:
     form=userregistration()
   return render(request,'register.html',{'form':form})