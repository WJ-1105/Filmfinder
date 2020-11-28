from django.contrib import admin
from django.urls import path, include, re_path
from index.views import index, login,signup, homelogin, logout,detail,profile


urlpatterns = [
    re_path(r'^$', index, name = 'index_page'),
    re_path(r'^login/$',login, name = 'login_page'),
    re_path(r'^signup/$',signup,name = 'signup_page'),
    re_path(r'^homelogin/(?P<you>.+)$',homelogin,name = 'homelogin_page'),
    re_path(r'^people/([a-zA-Z0-9]*)$',profile,name = 'profile_page'),
    re_path(r'^movie/(\d+)$',detail,name = 'detail_page'),
    re_path(r'^homelogin/$',homelogin,name = 'homelogin_page'),
    re_path(r'^logout/$',logout,name = 'logout_page'),
    re_path(r'^detail/$',detail,name = 'detail_page'),
]
