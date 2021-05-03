from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel, ProfileModel
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy



# Create your views here.

def signupfunc(request):
	if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			try:
				user = User.objects.create_user(username, '', password)
				return redirect('login')
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
			for object_profile in ProfileModel.objects.all():
				if username == object_profile.author:
					return redirect('list')
			return redirect('profilecreate')
		else:
			return render(request, 'login.html', {})
	return render(request, 'login.html', {})

@login_required
def listfunc(request):
	object_list = BoardModel.objects.all()
	object_profile = ProfileModel.objects.all()
	return render(request, 'list.html', {'object_list':object_list,'object_profile':object_profile})

def logoutfunc(request):
	logout(request)
	return redirect('login')

@login_required
def detailfunc(request, pk):
	object = get_object_or_404(BoardModel, pk=pk)
	return render(request, 'detail.html', {'object':object})

def goodfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in object.readtext:
        return redirect('list')
    else:
        object.good = object.good + 1
        object.readtext = object.readtext + ' ' + username
        object.save()
        return redirect('list')


class BoardCreate(CreateView):
	template_name = 'create.html'
	model = BoardModel
	fields = ('title', 'content', 'author', 'sns_image')
	success_url = reverse_lazy('list')

class ProfileCreate(CreateView):
	template_name = 'profilecreate.html'
	model = ProfileModel
	fields = ('author', 'header_image', 'one_thing', 'follow_number', 'follow_text', 'befollowed_number', 'befollowed_text')
	success_url = reverse_lazy('list')

def profilefunc(request, pk):
	pk_board = BoardModel.objects.get(pk=pk)
	user = request.user
	object_board = []
	for b in BoardModel.objects.all():
		if pk_board.author == b.author:
			object_board.append(b)
	for p in ProfileModel.objects.all():
		if pk_board.author == p.author:
			object_profile = p
			break
	return render(request, 'profile.html', {'object_board':object_board, 'object_profile':object_profile})

class BoardDelete(DeleteView):
    template_name = 'delete.html'
    model = BoardModel
    success_url = reverse_lazy('list')

class BoardUpdate(UpdateView):
    template_name = 'update.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'sns_image')
    success_url = reverse_lazy('list')

def followfunc(request, pk):
	object = BoardModel.objects.get(pk=pk)
	user = request.user
	profile_object = ProfileModel.objects.all()
	for p_object in profile_object:
		if user.username == p_object.author:
			p_object.follow_number += 1
			p_object.follow_text += ' ' + object.author
			p_object.save()
	for p_object in profile_object:
		if object.author == p_object.author:
			p_object.befollowed_number += 1
			p_object.befollowed_text += ' ' + user.username
			p_object.save()
	return redirect('list')

def followpagefunc(request):
	user = request.user
	return render(request, 'followpage.html', {'follow_list':follow_list})