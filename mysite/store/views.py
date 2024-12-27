from .models import *
from .serializers import *
from rest_framework import viewsets, generics, status
from .filters import PostFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Pagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username']

    def get_queryset(self):
        return UserProfile.objects.filter(username=self.request.user)


class FollowListCreateAPIView(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class PostListGreatAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
    ordering_fields = ['created_at']
    pagination_class = PageNumberPagination


class PostLikeListAPIView(generics.ListAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentLikeListApiVIew(generics.ListAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer


class StoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


class SavedListApiVIew(generics.ListAPIView):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer


class SaveItemViewSet(viewsets.ModelViewSet):
    queryset = SaveItem.objects.all()
    serializer_class = SaveItemSerializer



