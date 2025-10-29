from django.db import models

class Language(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class LanguageString(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="language_strings")
    content = models.TextField()

    def __str__(self) -> str:
        return f"{self.language.code}: {self.content[:50]}"


class Situation(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    descriptions = models.ManyToManyField(LanguageString, related_name="situations", blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self) -> str:
        english = (
            self.descriptions.filter(language__code="eng")
            .values_list("content", flat=True)
            .first()
        )
        return english or f"Situation #{self.pk}"

    def has_utterances_for_language(self, language_code: str) -> bool:
        """
        Check whether the situation has at least one communication with
        an utterance in the provided language.
        """
        return self.communications_of_situation.filter(
            utterances_of_communication__language__code=language_code
        ).exists()


class Communication(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    situations = models.ManyToManyField(Situation, related_name="communications_of_situation", blank=True)
    descriptions = models.ManyToManyField(LanguageString, related_name="communications", blank=True)
    shouldBeExpressed = models.BooleanField()
    shouldBeUnderstood = models.BooleanField()

    def __str__(self) -> str:
        english = (
            self.descriptions.filter(language__code="eng")
            .values_list("content", flat=True)
            .first()
        )
        return english or f"Communication #{self.pk}"


class Prompt(models.Model):
    situations = models.ManyToManyField(Situation, related_name="prompts", blank=True)
    descriptions = models.ManyToManyField(LanguageString, related_name="prompts", blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        english = (
            self.descriptions.filter(language__code="eng")
            .values_list("content", flat=True)
            .first()
        )
        return english or f"Prompt #{self.pk}"


class Utterance(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    communication = models.ForeignKey(Communication, on_delete=models.CASCADE, related_name="utterances_of_communication")
    transliteration = models.CharField(max_length=255, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="utterances")
    content = models.TextField()

    def __str__(self) -> str:
        english = (
            self.communication.descriptions.filter(language__code="eng")
            .values_list("content", flat=True)
            .first()
        )
        return english or f"Utterance #{self.pk}"

class ContextType(models.Model):
    name = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)
    descriptions = models.ManyToManyField(LanguageString, related_name="context_type_of_description", blank=True)

class Context(models.Model):
    utterance = models.ForeignKey(Utterance, on_delete=models.CASCADE, related_name="contexts")
    context_type = models.CharField(max_length=255)
    descriptions = models.ManyToManyField(LanguageString, related_name="context_of_description", blank=True)

    class Meta:
        verbose_name_plural = "contexts"

    def __str__(self) -> str:
        english = (
            self.descriptions.filter(language__code="eng")
            .values_list("content", flat=True)
            .first()
        )
        return english or f"Context #{self.pk}"
