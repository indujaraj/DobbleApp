from django.urls import path

from . import views

urlpatterns = [
    path('timeline', views.PostListView.as_view(), name="timeline"),
    path('post/<int:pk>/like', views.AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike',views. AddDislike.as_view(), name='dislike'),
    path('myposts', views.MyPosts.as_view(), name="myposts"),
    path("comments/add/<int:id>", views.Comments.as_view(),name="addcomment"),
    path('inbox/', views.ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread', views.CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', views.ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/',views.CreateMessage.as_view(), name='create-message'),
    path('search/', views.UserSearch.as_view(), name='profile-search'),
    path('delete/<int:id>', views.PostDelete.as_view(), name="delete"),
    path('update/<int:id>', views.PostUpdate.as_view(), name="update"),

]