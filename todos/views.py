from urllib import request
from django.shortcuts import render
from rest_framework import filters
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from todos.pagination import CustomPageNumberPagination
from todos.serializers import TodoSerializer
from .models import Todo
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class TodoApiView(ListCreateAPIView):
       serializer_class=TodoSerializer
       permission_classes=(IsAuthenticated,)
       filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
       pagination_class=CustomPageNumberPagination

       filterset_fields=['id','desc','title','is_complete']
       search_fields=['id','desc','title','is_complete']
       ordering_fields=['id','desc','title','is_complete']



       def perform_create(self, serializer):
            return serializer.save(owner=self.request.user)
       def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)


class TodoDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class=TodoSerializer
    permission_classes=(IsAuthenticated,)
    lookup_field='id'

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
