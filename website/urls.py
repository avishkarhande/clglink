"""clgin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.views.static import serve 
from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views
from . import views
from django.utils.text import slugify

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('myprofile/',views.myprofile,name='myprofile'),
    path('updateskill/',views.updateskill,name='updateskill'),
    path('addbio/',views.addbio,name='addbio'),
    path('initialreg/',views.initialreg,name='initialreg'),
    path('add-edu/',views.add_edu,name="add-edu"),
    path('add-work/',views.add_work,name="add-work"),
    path('updateindividualskill/<int:id>',views.updateindividualskill,name='updateindskill'),
    path('deleteindividualskill/<int:id>',views.deleteindividualskill,name='deleteindskill'),
    path('profile/<slug:slug>',views.profile,name='profile'),
    path('updateprofile/<slug:slug>',views.updateprofile,name='updateprofile'),
    path('updateedujhfdjhjdf/<int:id>/',views.updateedu,name='updateedu'),
    path('updatededukfjdkfjkdfj/<int:id>/',views.updatededu,name='updatededu'),
    path('updateworkhghgggdghjs/<int:id>/',views.updatework,name='updatework'),
    path('updatedworkdfdfsfdf/<int:id>/',views.updatedwork,name='updatedwork'),
    path('deleteworkhsdgjhsdgg/<int:id>/',views.deletework,name='deletework'),
    path('deleteedusdjhfjhdf/<int:id>/',views.deleteedu,name='deleteedu'),
    path('addachievement/',views.addachievement,name='addachievement'),
    path('notifications/',views.notifications,name='notifications'),
    path('deletenotifications/',views.deletenotifications,name='deletenotifications'),
    path('passchange/',views.passchange,name="passchange"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('addsocialmedia/',views.addsocialmedia,name="addsocialmedia"),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='settings.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),

    path('settings/',views.settings,name='settings'),
    path('change_username/',views.updateusername,name='changeusername'),
    path('search/',views.search,name='search'),
    path('updatephone/',views.updatephone,name="updatephone"),
    path('updateyear/',views.updateyear,name="updateyear")
]


handler404 = 'website.views.handler_404'
