"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls import include, url

from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from anime import views

urlpatterns = [
    path('admin/root/user', admin.site.urls),

    url('register/', views.registerpage, name="register"),
    url('login/', views.loginpage, name="login"),
    url('logout/', views.logoutuser, name="logout"),


    # reinitialisation du mot de pass
    url('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='anime/password_reset.html'
    ),
         name="password_reset/"),

    #  page  qui indique qu'un mail a été envoiyé pour  la reinitialisation
    url('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='anime/password_reset_done.html'),
        name="password_reset_done"),

    # page de confirmation de reinitialisation
    #<uidb64>  id de l'utilisateur encoder en base 64
    # <token> --> pour la securisation verifie que le mot de pass est valide
    url('password-reset-confirm/<uid64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='anime/password_reset_confirm.html'),
        name="password_reset_confirm"),
        
        
        
        
    #url('defi_actuel/', views.defi_actuel, name="defi_actuel"),

    #url('defi_jouer/', views.defi_actuel, name="defi_actuel"),



    #url('defi_precedent/', views.defis_precedent, name="defi_precedent"),

    #url('defi_avenir/', views.defis_avenir, name="defi_avenir"),

    url(r'^$', views.home, name="home"),

    url(r'profile/$', views.profileuser, name="profile"),

    url(r'^anime/', include('anime.urls', namespace='anime')),


]



if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
      url(r'^__debug__/', include(debug_toolbar.urls)),
        #static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    	] + urlpatterns


if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)















