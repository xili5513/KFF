from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.conf.urls import include


urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/register', views.create_auth),
    path('users/login', views.login),
    path('products/data', views.SnippetList.as_view()),
    path('products/data/<int:pk>/', views.SnippetDetail.as_view()),
    path('products/', views.home, name='home'),
    path('report/', views.ReportList.as_view()),
    path('auth/', include('rest_framework_social_oauth2.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]