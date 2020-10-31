"""Module for mapping path with its function."""
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'polls'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index_view, name='index'),
    # path('<int:pk>/', login_required(views.DetailView.as_view()), name='detail'),
    path('<int:pk>/', login_required(views.detail_view), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:pk>/results/', views.result_view, name='results'),
    path('<int:question_id>/vote/', views.can_access, name='vote'),
]
