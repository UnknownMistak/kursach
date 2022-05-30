"""portfolios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include, re_path
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import routers, serializers, viewsets, status, pagination, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from accs.models import Project


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

    def validate_username(self, username):
      if has_numbers(username):
          raise ValidationError('Имя пользователя не может содержать цифр')
      return username


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'date_created']


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['is_staff']

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'status']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    action_serializers = {
        'change_staff': StaffSerializer
    }
    @action(methods=['GET'], detail=False)
    def staff(self, request):
        staff_users = User.objects.filter(Q(is_staff=True)) #фильтрация если пользователь админ
        page = self.paginate_queryset(staff_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(staff_users, many=True)
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=True)
    def change_staff(self, request, pk = None):
        user = self.get_object()
        serializer = StaffSerializer(data = request.data)
        if (serializer.is_valid()):
            is_staff = serializer.validated_data['is_staff']
            user.is_staff = is_staff
            user.save()
            return Response({
                'status': 'Права пользователя изменены'
            })
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def me(self, request):
        current_user = request.user
        try: 
          me = User.objects.get(pk=current_user.pk)
          if me is not None:
              serializer = self.get_serializer(me)
              return Response(serializer.data)
        except: 
          return Response({
              'status': 'Вы не авторизованы'
          })

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)
        return super(MyModelViewSet, self).get_serializer_class()



    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email', 'is_staff']
    

api_router = routers.DefaultRouter()
api_router.register(r'users', UserViewSet)
api_router.register(r'projects', ProjectViewSet)

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('accs.urls')),
    path('sentry-debug/', trigger_error),
    re_path(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/', include(api_router.urls)),
]
