"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from dash import views
from django.urls import path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('types/<int:category_id>/', views.view_types, name='view_types'),
    path('articles/<int:type_id>/', views.view_article, name='view_article'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('view_types/<int:category_id>/', views.view_types, name='view_types'),
    path('delete_type/<int:type_id>/', views.delete_type, name='delete_type'),
    path('edit_type/<int:type_id>/', views.edit_type, name='edit_type'),
    path('edit_article/<int:article_sn>/', views.edit_article, name='edit_article'),
    path('delete_article/<int:article_sn>/', views.delete_article, name='delete_article'),
]

