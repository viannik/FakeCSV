"""FakeCSV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from authentication.views import CustomLoginView, LogoutView
from data_schemas.views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', CustomLoginView.as_view(), name='home'),
	path('login/', CustomLoginView.as_view(), name='login'),
	path('logout/', LogoutView, name='logout'),
	path('schemas/', schema_list, name='schema_list'),
	path('schemas/new/', schema_create, name='schema_new'),
	path('schemas/<int:pk>/edit/', schema_update, name='schema_edit'),
	path('schemas/<int:pk>/delete/', schema_delete, name='schema_delete'),
	path('schemas/<int:pk>/datasets/', schema_datasets, name='schema_datasets'),
	path('schemas/<int:pk>/datasets/<int:dataset_pk>/delete/', schema_dataset_delete, name='dataset_delete'),
	path('schemas/<int:pk>/datasets/<int:dataset_pk>/download/', schema_dataset_download, name='dataset_download'),
]
