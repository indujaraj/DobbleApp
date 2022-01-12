from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('signup', views.SignUp.as_view(), name="signup"),
    path('signin',views.UserLogin.as_view(), name="login"),
    path('logout',views.LogoutView.as_view(), name="logout"),
    path('profile/<int:id>', views.ProfileDetailView.as_view(), name='profile'),
    path('profileview/<int:pk>', views.ProfileView.as_view(), name='profileview'),
    path('friends', views.ListFriends.as_view(), name='friends'),
    path('requests', views.ListRequests.as_view(), name='requests'),
    path('sendrequest/<int:id>', views.SendRequest.as_view(), name='sendrequest'),
    path('removerequest/<int:id>', views.RemoveRequest.as_view(), name='removerequest'),
    path('acceptrequest/<int:id>', views.AcceptRequest.as_view(), name='acceptrequest'),
    path('friendslist/<int:id>', views.FriendList.as_view(), name="friendslist"),
    path('delete/<int:id>', views.DeleteProfile.as_view(), name="deleteprofile"),
    path('rejectrequest/<int:id>', views.RejectRequest.as_view(), name='rejectrequest'),
    path('contact/', views.contactsendmail, name='contactus'),
    path('password/', views.change_password, name='change_password'),

]

