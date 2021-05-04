from django.urls import path, include
from .views import signupfunc, loginfunc, listfunc,\
logoutfunc, detailfunc, goodfunc, BoardCreate, profilefunc, BoardDelete, BoardUpdate, followfunc, followpagefunc, ProfileCreate
urlpatterns = [
	path('signup/', signupfunc, name='signup'),
	path('', loginfunc, name='login'),
	path('list/', listfunc, name='list'),
	path('logout/', logoutfunc, name='logout'),
	path('detail/<int:pk>', detailfunc, name='detail'),
	path('good/<int:pk>', goodfunc, name='good'),
	path('create/', BoardCreate.as_view(), name='create'),
	path('delete/<int:pk>', BoardDelete.as_view(), name='delete'),
    path('update/<int:pk>',BoardUpdate.as_view(), name='update'),
	path('follow/<int:user_id>', followfunc, name='follow'),
	path('followpage/<int:user_id>', followpagefunc, name='followpage'),
	path('profilecreate/', ProfileCreate.as_view(), name='profilecreate'),
	path('profile/<int:user_id>', profilefunc, name='profile'),
]
