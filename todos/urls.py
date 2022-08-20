from django.urls import path
from .import views





urlpatterns=[

    path('',views.TodoApiView.as_view(),name='todos'),
    path('<int:id>',views.TodoDetailApiView.as_view(),name='todo')
]