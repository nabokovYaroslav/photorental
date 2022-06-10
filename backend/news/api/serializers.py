from rest_framework import serializers

from news.models import New


class NewSerializer(serializers.ModelSerializer):

    class Meta:
        model = New
        fields = "__all__"