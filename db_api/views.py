from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from db_api.models import NewsArticle, Tag, Company
from db_api.serializers import NewsArticleSerializer, TagSerializer, CompanySerializer
from db_api.filters import NewsArticleFilterSet
from url_filter.integrations.drf import DjangoFilterBackend

class NewsArticleViewSet(viewsets.ModelViewSet):
    """
    list, create, retrieve, update and destroy
    """
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
#    filter_backends = [DjangoFilterBackend]  #Already specified in settings
#    filter_fields = ['id','title','company']
    filter_class = NewsArticleFilterSet
    def get_queryset(self):
        return NewsArticle.objects \
            .prefetch_related('tag') \
            .select_related('company') 

class TagViewSet(viewsets.ModelViewSet):
    """
    list, create, retrieve, update and destroy
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    list, create, retrieve, update and destroy
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
#    filter_fields = ['name']


    
