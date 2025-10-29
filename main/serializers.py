from rest_framework import serializers

from .models import Language, Situation


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("id", "code", "name")


class SituationSerializer(serializers.ModelSerializer):
    language_code = serializers.SerializerMethodField()

    class Meta:
        model = Situation
        fields = ("id", "last_updated", "image_url", "language_code", "description")

    def get_language_code(self, obj):
        return self.context.get("language_code")
