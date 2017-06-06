from django.conf.urls import url
from . import views
app_name = 'login_and_registration_app'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^registration$', views.registration, name = 'registration'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^logout$', views.logout, name = 'logout'),
    url(r'^update_account_info$', views.update_account_info, name = 'update_account_info')

]
