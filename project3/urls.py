from django.conf.urls import url
from app1.views import food_view,rest_view,signup_view, login_view, feed_view, post_view, like_view, comment_view, log_out, first_view,sec_view,third_view
from django.contrib import admin

urlpatterns = [
    url(r'^$',first_view),
    url(r'^admin/', admin.site.urls),
    url(r'^post/$', post_view),
    url(r'^feed/$', feed_view),
    url(r'^like/$', like_view),
    url(r'^comment/$', comment_view),
    url(r'^login/$', login_view),
    url(r'^signup/$', signup_view),
    url(r'^log_out/$', log_out),
    url(r'^feed/rest/$', rest_view),
    url(r'^feed/rest/food/$', food_view),
]
