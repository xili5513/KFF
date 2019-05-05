from rest_framework import serializers
from snippets.models import Snippet
from snippets.models import Report
from django.contrib.auth.models import User
from snippets.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'gender', 'age')


class SnippetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snippet
        fields = ('id', 'rating', 'product_name', 'product_category', 'accreditation',
                  'availability', 'image_label')
        # owner = serializers.ReadOnlyField(source='owner.username')


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ('id', 'product_id', 'product_name', 'coordinate', 'location_description')


