from django.contrib.auth.models import User
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAuthenticated

from .models import Article
from .serializers import ArticleSerializer, UserSerializer

from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication


class ArticleGenericsMixin:

    @staticmethod
    def modify_data(request, article=None):
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleGenericViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]


class ArticleViewSet(viewsets.ViewSet, ArticleGenericsMixin):

    @staticmethod
    def get_current_article(pk):
        return Article.objects.get(pk=pk)

    @staticmethod
    def list(request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data)

    def create(self, request):
        return super().modify_data(request)

    @staticmethod
    def retrieve(request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        article = self.get_current_article(pk=pk)
        return super().modify_data(request, article=article)

    def destroy(self, request, pk=None):
        article = self.get_current_article(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleListUpdated(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class ArticleList(APIView, ArticleGenericsMixin):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        return super().modify_data(request)


@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        pass
        # return modify_data(request)


class ArticleDetailsUpdated(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, pk=id)

    def put(self, request, id):
        return self.update(request, pk=id)

    def delete(self, request, id):
        return self.destroy(request, pk=id)


class ArticleDetails(APIView, ArticleGenericsMixin):
    @staticmethod
    def get_article(id):
        try:
            return Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.get_article(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, id):
        article = self.get_article(id)
        return super().modify_data(request, article=article)

    def delete(self, request, id):
        article = self.get_article(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def article_details(request, id):
    try:
        article = Article.objects.get(pk=id)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    if request.method == 'PUT':
        pass
        # return modify_data(request, article=article)

    if request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsAuthenticated, ]
