from snippets.models import Snippet
from snippets.models import Report
from snippets.models import Statistics
from snippets.serializers import StatisticsSerializer
# from snippets.models import Member
from django.db.models import Sum
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
                                'amazing server made by Eddie please wait'}, gender=gender, age=age, status=status.HTTP_400_BAD_REQUEST)


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
    user_info = models.CustomUser.objects.get(username=username)
    age = user_info.age
    gender = user_info.gender
    return Response({'token': token.key, 'age': age, 'gender': gender},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def report(request):
    product_id = request.data.get("product_id")
    product_name = request.data.get("product_name")
    coordinate = request.data.get("coordinate")
    location_description = request.data.get("location_description")
    # serializer = ReportSerializer(data=request.data)
    try:
        if not product_id and not product_name and not coordinate and not location_description:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # serializer.save()
            models.Report.objects.create(
                product_id=product_id, product_name=product_name, coordinate=coordinate, location_description=location_description
            )
            return Response({'msg': 'report successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'MSG': 'Sorry, report upload failed'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_google_user(request):
    username = request.data.get("username", "")
    token = request.data.get("password", "")
    gender = request.data.get("gender", "")
    age = request.data.get("age", "")
    email = request.data.get("email", "")
    # serialized = UserSerializer(data=request.DATA)
    try:
        if not username and not token and not email and not gender and not age:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            models.CustomUser.objects.create_user(
                username=username, password='', gender=gender, age=age, email=email
            )
            return Response({'MSG': 'Successful', }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'MSG': "Account already exist, do not have to create"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def auth_google_user(request):
    username = request.data.get("username", "")
    count = models.CustomUser.objects.filter(username=username).count()
    user_info = models.CustomUser.objects.get(username=username)
    age = user_info.age
    gender = user_info.gender
    if count == 0:
        return Response({'MSG': 'Username is available'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'MSG': 'Username is used by others', 'age': age, 'gender': gender},
                        status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def data_statistics(request):
    brand_name = request.data.get("brand_name", "")
    user_age = request.data.get("user_age", "")
    user_gender = request.data.get("user_gender", "")
    product_type = request.data.get("product_type", "")
    # count = models.CustomUser.objects.filter(username=username).count()
    if not brand_name and not user_age and not user_gender and not product_type:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # serializer.save()
        models.Statistics.objects.create(
            brand_name=brand_name, user_age=user_age, user_gender=user_gender, product_type=product_type
        )
        return Response({'msg': 'data collect successfully'}, status=status.HTTP_201_CREATED)


def home(request):
    from django.core import serializers
    age_result_1 = list(models.Statistics.objects.filter(user_age='Under 18').values("brand_name").annotate(
        total_num=Sum("num")).all().order_by('-total_num')[:5])
    age_result_2 = list(models.Statistics.objects.filter(user_age='18-29').values("brand_name").annotate(
        total_num=Sum("num")).all().order_by('-total_num')[:5])
    age_result_3 = list(models.Statistics.objects.filter(user_age='30-39').values("brand_name").annotate(
        total_num=Sum("num")).all().order_by('-total_num')[:5])
    age_result_4 = list(models.Statistics.objects.filter(user_age='40-49').values("brand_name").annotate(
        total_num=Sum("num")).all().order_by('-total_num')[:5])
    age_result_5 = list(models.Statistics.objects.filter(user_age='50-59').values("brand_name").annotate(
        total_num=Sum("num")).all().order_by('-total_num')[:5])
    age_result_6 = list(models.Statistics.objects.filter(user_age='60+').values("brand_name").annotate(
        total_num=Sum("num")).all().order_by('-total_num')[:5])
    # age_result_all = list(models.Statistics.objects.values())
    # data = {'data': age_result_all}
    data = {'data_1': age_result_1, 'data_2': age_result_2, 'data_3': age_result_3,'data_4': age_result_4,
            'data_5': age_result_5, 'data_6': age_result_6}
    # result = json.dumps(models.Statistics.objects.filter(user_age='60+').values("brand_name").annotate(
    #     total_num=Sum("num")).all().order_by('-total_num')[:5])
    return render(request, 'index.html', data)


def gender(request):
    gender_result_1 = list(models.Statistics.objects.filter(user_gender='Male').values("brand_name").annotate(
        total_num=Sum("num")).all().order_by('-total_num')[:5])
    gender_result_2 = list(models.Statistics.objects.filter(user_gender='Female').values("brand_name").annotate(
        total_num=Sum("num")).all().order_by('-total_num')[:5])
    data = {'data_1': gender_result_1, 'data_2': gender_result_2}
    return render(request, 'second.html', data)


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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StatisticsList(generics.ListCreateAPIView):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
