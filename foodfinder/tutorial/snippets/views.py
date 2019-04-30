from snippets.models import Snippet
from snippets.models import Report
# from snippets.models import Member
from . import models
from snippets.serializers import SnippetSerializer
from snippets.serializers import ReportSerializer
from rest_framework import generics
# from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_auth(request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    gender = request.data.get("gender", "")
    age = request.data.get("age", "")
    email = request.data.get("email", "")
    # serialized = UserSerializer(data=request.DATA)
    try:
        if not username and not password and not email and not gender and not age:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            models.CustomUser.objects.create_user(
                username=username, password=password, gender=gender, age=age, email=email
            )
            return Response({'MSG': 'Successful'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'MSG': 'Sorry, account created failed, we are fixing the '
                                'amazing server made by Eddie please wait'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


def home(request):
    return render(request, 'index.html')


# @permission_classes((AllowAny,))
class UserList(generics.ListAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = UserSerializer


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, format = "json"):
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=request.data)
        # print(request.data)
        # rating = request.data.get("rating", "")
        # print('rating', rating)
        # product_name = request.data.get("product_name", "")
        # product_category = request.data.get("product_category", "")
        # accreditation = request.data.get("accreditation", "")
        # availability = request.data.get("availability", "")
        # image_label = request.data.get("image_label", "")
        if serializer.is_valid():
            serializer.save()
            # models.Snippet.objects.create(
            #     rating=rating, product_name=product_name, product_category=product_category,
            #     accreditation=accreditation, availability=availability,image_label=image_label
            # )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def post(self, request, format = "json"):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # models.Snippet.objects.create(
            #     rating=rating, product_name=product_name, product_category=product_category,
            #     accreditation=accreditation, availability=availability,image_label=image_label
            # )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
