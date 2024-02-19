"""notes_project URL Configuration

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
from django.contrib import admin
from django.urls import path
from notes_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:id>/', views.get_note, name='get_note'),
    path('notes/share/', views.share_note, name='share_note'),
    path('notes/<int:id>/update/', views.update_note, name='update_note'),
    path('notes/version-history/<int:id>/', views.get_note_version_history, name='get_note_version_history'),

]
