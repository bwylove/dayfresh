from django.conf.urls import url

from df_cart import views

urlpatterns = [
    url(r'^$',views.cart,name='cart' ),
    url(r'^delete/$',views.delete,name='delete'),
    url(r'^edit/$',views.edit,name='edit'),
    url(r'^add/$',views.add,name='add'),
]