from django.urls import path
from . import views
urlpatterns=[
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('travels', views.travels),
    path('logOut', views.logOut),
    path('addtrip', views.addtrip),
    path('add', views.add),
    path('join/<int:destinationID>', views.join),
    path('cancel/<int:destinationID>', views.cancel),
    path('view/<int:destinationID>', views.destinationInfo),
    path('delete/<int:destinationID>', views.delete)
]