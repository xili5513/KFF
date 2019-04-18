from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.conf.urls import include


urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/register', views.create_auth),
    path('users/login', views.login),
    path('snippets/data', views.SnippetList.as_view()),
    path('snippets/data/<int:pk>/', views.SnippetDetail.as_view()),
    path('snippets/', views.home, name='home'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]