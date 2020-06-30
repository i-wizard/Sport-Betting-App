from rest_framework import serializers

from support.models import Support


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = '__all__'

    def create(self, validated_data):
        issue = Support.objects.create(title=validated_data['title'], username=validated_data['username'],
                                       email=validated_data['email'], message=validated_data['message'])

        return issue
