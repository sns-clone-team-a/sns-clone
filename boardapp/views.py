from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel, ProfileModel
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages



# Create your views here.

def signupfunc(request):

	if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			try:
				user = User.objects.create_user(username, '', password)
				user = authenticate(request, username=username, password=password)
				login(request, user)
				return redirect('profilecreate')
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
	object_profile = ProfileModel.objects.all()
	user = request.user
	keyword = request.GET.get('keyword')
	if keyword:
		object_list = object_list.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword) |Q(author__icontains=keyword))
		messages.success(request, ' 「{}」の検索結果'.format(keyword))
	return render(request, 'list.html', {'object_list':object_list,'object_profile':object_profile, 'user':user})

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
	fields = ('user_id', 'title', 'content', 'author', 'sns_image')
	success_url = reverse_lazy('list')

class ProfileCreate(CreateView):
	template_name = 'profilecreate.html'
	model = ProfileModel
	fields = ('user_id', 'author', 'header_image', 'one_thing', 'follow_number', 'follow_text', 'befollowed_number', 'befollowed_text')
	success_url = reverse_lazy('list')

def profilefunc(request, user_id):
	object_profile = ProfileModel.objects.get(user_id=user_id)
	object_board = []
	for b in BoardModel.objects.all():
		if user_id == b.user_id:
			object_board.append(b)
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

def followfunc(request, user_id):
	user = request.user
	follow = ProfileModel.objects.get(user_id=user.id)   #フォローしている人
	befollowed = ProfileModel.objects.get(user_id=user_id)    #フォローされてる人
	profile_object = ProfileModel.objects.all()

	follow.follow_number += 1 								#フォロー側の処理
	follow.follow_text += ' ' + str(befollowed.user_id )           
	follow.save()

	befollowed.befollowed_number += 1						#フォロワー側の処理
	befollowed.befollowed_text += ' ' + str(follow.user_id)
	befollowed.save()

	return redirect('list')

def followpagefunc(request, user_id):
	user = ProfileModel.objects.get(user_id=user_id)
	follow_list = []
	for b in BoardModel.objects.all():
		for f in user.follow_text.split():
			if str(b.user_id) == f:
				follow_list.append(b)
	return render(request, 'followpage.html', {'follow_list':follow_list})