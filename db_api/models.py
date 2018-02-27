from django.db import models
import datetime

class NewsArticle (models.Model):

    tstamp = models.DateTimeField(null=False, default='1970-01-01T00:00')
    url = models.TextField(primary_key=True)    
    title = models.TextField(null=False)
    brief = models.TextField(null=True)
    body = models.TextField(null=True)
    date = models.DateTimeField(null=False, default='1970-01-01T00:00')
    source = models.TextField(default='UNDEFINED', null=False)
    company = models.TextField(null=False, default='UNDEFINED')
    tag = models.TextField(null=True)

#    tstamp = models.DateTimeField()
#    url = models.CharField(max_length=300, blank=True, default='UNDEFINED')    
#    title = models.CharField(max_length=300, blank=True, default='UNDEFINED')
#    author = models.CharField(max_length=100, blank=True, default='UNDEFINED')
#    brief = models.TextField()
#    body = models.TextField()
#    source = models.CharField(choices=ARTICLE_CHOICES, default='UNDEFINED', max_length=100)
#    company = models.ForeignKey('Company', to_field='name', related_name='news_articles', 
#        default='UNDEFINED', on_delete=models.SET_DEFAULT)
#    tag = models.ManyToManyField('Tag', related_name='news_articles')

    
class Tag (models.Model):
    name = models.CharField(max_length=100, primary_key=True) 

    def __str__(self):
        return self.name

    
class Company (models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name
