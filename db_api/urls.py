from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from db_api import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'^newsarticles', views.NewsArticleViewSet)
router.register(r'^tags', views.TagViewSet)
router.register(r'^companies', views.CompanyViewSet, 'base')

# The router will determine the URLs automatically
urlpatterns = [
    url(r'^', include(router.urls)),
]
