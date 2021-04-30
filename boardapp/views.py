from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel, FollowModel
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy



# Create your views here.

def signupfunc(request):
	if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			try:
				user = User.objects.create_user(username, '', password)
				return render(request, 'signup.html', {'some':100})
			except IntegrityError:
				return render(request, 'signup.html', {'error':'このユーザーは既に登録されています'})
	return render(request, 'signup.html')


def loginfunc(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('list')
		else:
			return render(request, 'login.html', {})
	return render(request, 'login.html', {})

@login_required
def listfunc(request):
	object_list = BoardModel.objects.all()
	follow_list = FollowModel.objects.all()
	user = request.user
	for f in follow_list:
		if user.username == f.author:
			following = f 
	return render(request, 'list.html', {'object_list':object_list, 'following':following})

def logoutfunc(request):
	logout(request)
	return redirect('login')

@login_required
def detailfunc(request, pk):
	object = get_object_or_404(BoardModel, pk=pk)
	return render(request, 'detail.html', {'object':object})

def goodfunc(request, pk):
	object = BoardModel.objects.get(pk=pk)
	object.good += 1
	object.save()
	return redirect('list')

def readfunc(request, pk):
	object = BoardModel.objects.get(pk=pk)
	username = request.user.get_username()
	if username in object.readtext:
		return redirect('list')
	else:
		object.read += 1
		object.readtext += ' ' + username
		object.save()
		return redirect('list')

class BoardCreate(CreateView):
	template_name = 'create.html'
	model = BoardModel
	fields = ('title', 'content', 'author', 'sns_image')
	success_url = reverse_lazy('list')

def followfunc(request, pk):
	object = BoardModel.objects.get(pk=pk)
	user = request.user
	judge1 = True
	judge2 = True
	follow_object = FollowModel.objects.all()
	for f_object in follow_object:
		if user.username in f_object.author:
			f.follow += 1
			f.followtext += ' ' + object.author
			judge1 = False
	if judge1:
		f1 = FollowModel(
			author = user.username,
			follow = 1,
			followtext = object.author,
			befollowed = 0,
			befollowedtext = "initial"
		)
		f1.save()
	for f_object in follow_object:
		if object.author in f_object.author:
			f.befollowed += 1
			f.befollowedtext += ' ' + user.username
			judge2 = False
	if judge2:
		f2 = FollowModel(
			author = object.author,
			follow = 1,
			followtext = "initial",
			befollowed = 0,
			befollowedtext = user.username
		)
		f2.save()
	return redirect('list')

def followpagefunc(request):
	user = request.user
	return render(request, 'followpage.html', {'follow_list':follow_list})