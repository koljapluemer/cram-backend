from rest_framework import serializers

from .models import Language, LanguageString, Situation


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("id", "code", "name")


class LanguageStringSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(slug_field="code", read_only=True)

    class Meta:
        model = LanguageString
        fields = ("id", "language", "content")


class SituationSerializer(serializers.ModelSerializer):
    descriptions = LanguageStringSerializer(many=True, read_only=True)
    language_code = serializers.SerializerMethodField()

    class Meta:
        model = Situation
        fields = ("id", "last_updated", "image_url", "language_code", "descriptions")

    def get_language_code(self, obj):
        return self.context.get("language_code")
