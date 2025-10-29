from django.db.models import Prefetch
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Communication,
    Context,
    ContextType,
    Language,
    LanguageString,
    Prompt,
    Situation,
    Utterance,
)
from .serializers import LanguageSerializer, SituationSerializer


class LanguageListView(generics.ListAPIView):
    queryset = Language.objects.order_by("code")
    serializer_class = LanguageSerializer


class SituationsByLanguageView(generics.ListAPIView):
    serializer_class = SituationSerializer

    def get_queryset(self):
        language_code = self.kwargs["language_code"]
        return (
            Situation.objects.filter(languages__code=language_code)
            .prefetch_related(
                Prefetch(
                    "descriptions",
                    queryset=LanguageString.objects.filter(language__code=language_code),
                )
            )
            .order_by("id")
        )


class SituationDetailView(APIView):
    def get(self, request, situation_id: int):
        target_lang = request.query_params.get("target_lang")
        native_lang = request.query_params.get("native_lang")

        if not target_lang or not native_lang:
            return Response(
                {
                    "detail": "Query parameters 'target_lang' and 'native_lang' are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            situation = (
                Situation.objects.select_related("languages")
                .prefetch_related(
                    Prefetch(
                        "descriptions",
                        queryset=LanguageString.objects.filter(language__code=native_lang),
                    ),
                    Prefetch(
                        "prompts",
                        queryset=Prompt.objects.prefetch_related(
                            Prefetch(
                                "descriptions",
                                queryset=LanguageString.objects.filter(language__code=native_lang),
                            )
                        ),
                    ),
                    Prefetch(
                        "communications_of_situation",
                        queryset=Communication.objects.prefetch_related(
                            Prefetch(
                                "descriptions",
                                queryset=LanguageString.objects.filter(language__code=native_lang),
                            ),
                            Prefetch(
                                "utterances_of_communication",
                                queryset=Utterance.objects.filter(language__code=target_lang).prefetch_related(
                                    Prefetch(
                                        "contexts",
                                        queryset=Context.objects.prefetch_related(
                                            Prefetch(
                                                "descriptions",
                                                queryset=LanguageString.objects.filter(language__code=native_lang),
                                            )
                                        ),
                                    )
                                ),
                            ),
                        ),
                    ),
                )
                .get(pk=situation_id)
            )
        except Situation.DoesNotExist:
            return Response(
                {"detail": f"Situation with id {situation_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        situation_payload = self._serialize_situation(situation, native_lang)
        prompts_payload = self._serialize_prompts(situation.prompts.all(), native_lang)
        communications_payload = self._serialize_communications(
            situation.communications_of_situation.all(),
            target_lang,
            native_lang,
        )

        return Response(
            {
                "situation": situation_payload,
                "prompts": prompts_payload,
                "communications": communications_payload,
            }
        )

    def _serialize_situation(self, situation: Situation, native_lang: str):
        descriptions = [
            {
                "id": ls.id,
                "content": ls.content,
                "language": ls.language.code,
            }
            for ls in situation.descriptions.all()
            if ls.language.code == native_lang
        ]

        return {
            "id": situation.id,
            "last_updated": situation.last_updated,
            "image_url": situation.image_url,
            "language": situation.languages.code if situation.languages_id else None,
            "descriptions": descriptions,
        }

    def _serialize_prompts(self, prompts, native_lang: str):
        result = []
        for prompt in prompts:
            result.append(
                {
                    "id": prompt.id,
                    "last_updated": prompt.last_updated,
                    "descriptions": [
                        {
                            "id": ls.id,
                            "content": ls.content,
                            "language": ls.language.code,
                        }
                        for ls in prompt.descriptions.all()
                        if ls.language.code == native_lang
                    ],
                }
            )
        return result

    def _serialize_communications(self, communications, target_lang: str, native_lang: str):
        data = []
        for communication in communications:
            utterances = [
                self._serialize_utterance(utterance, native_lang)
                for utterance in communication.utterances_of_communication.all()
                if utterance.language.code == target_lang
            ]

            if not utterances:
                continue

            data.append(
                {
                    "id": communication.id,
                    "last_updated": communication.last_updated,
                    "shouldBeExpressed": communication.shouldBeExpressed,
                    "shouldBeUnderstood": communication.shouldBeUnderstood,
                    "descriptions": [
                        {
                            "id": ls.id,
                            "content": ls.content,
                            "language": ls.language.code,
                        }
                        for ls in communication.descriptions.all()
                        if ls.language.code == native_lang
                    ],
                    "utterances": utterances,
                }
            )

        return data

    def _serialize_utterance(self, utterance: Utterance, native_lang: str):
        contexts_data = []
        for context in utterance.contexts.all():
            context_type_payload = self._resolve_context_type(context, native_lang)
            contexts_data.append(
                {
                    "id": context.id,
                    "context_type": context.context_type,
                    "context_type_details": context_type_payload,
                    "descriptions": [
                        {
                            "id": ls.id,
                            "content": ls.content,
                            "language": ls.language.code,
                        }
                        for ls in context.descriptions.all()
                        if ls.language.code == native_lang
                    ],
                }
            )

        return {
            "id": utterance.id,
            "last_updated": utterance.last_updated,
            "language": utterance.language.code,
            "transliteration": utterance.transliteration,
            "content": utterance.content,
            "contexts": contexts_data,
        }

    def _resolve_context_type(self, context: Context, native_lang: str):
        context_type = (
            ContextType.objects.prefetch_related(
                Prefetch(
                    "descriptions",
                    queryset=LanguageString.objects.filter(language__code=native_lang),
                )
            )
            .filter(name=context.context_type)
            .first()
        )
        if not context_type:
            return None

        return {
            "id": context_type.id,
            "name": context_type.name,
            "descriptions": [
                {
                    "id": ls.id,
                    "content": ls.content,
                    "language": ls.language.code,
                }
                for ls in context_type.descriptions.all()
                if ls.language.code == native_lang
            ],
        }
