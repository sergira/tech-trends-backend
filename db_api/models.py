from django.db import models


ARTICLE_CHOICES = (('spacedotcom','Space.com'),('spacenews', 'SpaceNews.com'),)


class NewsArticle (models.Model):

    tstamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=300, blank=True, default='UNDEFINED')    
    title = models.CharField(max_length=300, blank=True, default='UNDEFINED')
    author = models.CharField(max_length=100, blank=True, default='UNDEFINED')
    brief = models.TextField()
    body = models.TextField()
    source = models.CharField(choices=ARTICLE_CHOICES, default='UNDEFINED', max_length=100)
    company = models.ForeignKey('Company', to_field='name', related_name='news_articles', 
        default='UNDEFINED', on_delete=models.SET_DEFAULT)
    tag = models.ManyToManyField('Tag', related_name='news_articles')

    
class Tag (models.Model):
    name = models.CharField(max_length=100, primary_key=True)
#    news_articles = 

    def __str__(self):
        return self.name

    
class Company (models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name
