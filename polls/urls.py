from django.urls import path
from . import views

app_name = 'polls'

# urlpatterns = [
#     path('', views.index, name ='Index'),
#     path('<int:question_id>/', views.detail, name='detail'),
#     path('<int:question_id>/results/', views.results, name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]


urlpatterns = [
path('', views.IndexView.as_view(), name='index'),
path('<int:pk>/', views.DetailView.as_view(), name='detail'),
path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
path('<int:question_id>/vote/', views.vote, name='vote'),
path('register', views.create_user, name='register'),
path('upload', views.upload_file, name = 'upload'),
path('login', views.user_login, name = 'login'),
path('home', views.landing_page, name = 'landing'),

]