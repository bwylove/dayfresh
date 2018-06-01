from django.conf.urls import url

from df_order import views

urlpatterns = [
    url(r'^$', views.order),
    url(r'^addorder/$',views.order_handle,name='addorder'),
    url(r'^pay&(\d+)/$',views.pay,name='pay')
]