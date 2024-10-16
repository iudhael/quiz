from django.conf.urls import url # importer les urls du projet

from . import  views # import all views of store so we can use them in urls.

app_name = 'anime' # important pour le namespace

urlpatterns = [
    url(r'register/$', views.registerpage, name="register"),
    url(r'login/$', views.loginpage, name="login"),
    url(r'logout/$', views.logoutuser, name="logout"),
    #url(r'^$', views.home, name="home"),
    url(r'profile/$', views.profileuser, name="profile"),
    url(r'defi_actuel/$', views.defi_actuel, name="defi_actuel"),
    url(r'defi_jouer/$', views.defi_actuel, name="defi_actuel"),
    url(r'defi_precedent/$', views.defis_precedent, name="defi_precedent"),
    url(r'defi_avenir/$', views.defis_avenir, name="defi_avenir"),
    url(r'^(?P<defi_quiz_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'search/$', views.search, name="search"),
    #url(r'^(?P<all_defi_id>[0-9]+)/$', views.detail_all_defi, name="detail_all_defi"),





         ]





