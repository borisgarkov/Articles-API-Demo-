from django.urls import path, include
from .views import ArticleList, ArticleDetails, ArticleListUpdated, ArticleDetailsUpdated, ArticleViewSet, \
    ArticleGenericViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(prefix='articles', viewset=ArticleGenericViewSet, basename='articles')
router.register(prefix='users', viewset=UserViewSet, basename='users')


urlpatterns = [
    path('api/', include(router.urls)),
    # path('', ArticleListUpdated.as_view()),
    # path('articles/<int:id>/', ArticleDetailsUpdated.as_view()),
]
