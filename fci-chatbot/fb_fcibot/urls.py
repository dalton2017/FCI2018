from django.conf.urls import url
from .views import FCIView
urlpatterns =[
     url(r'^$', FCIView.as_view())
    ]

