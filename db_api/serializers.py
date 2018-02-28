from rest_framework import serializers
from db_api.models import NewsArticle, Tag, Company


class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = ('tstamp', 'url', 'title', 'brief', 'body', 
            'date', 'source', 'company', 'tag',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name',)
