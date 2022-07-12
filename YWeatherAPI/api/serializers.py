from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Report
        read_only_fields = ('id', 'date')
