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
    description = models.TextField()
    image_url = models.URLField(blank=True)
    target_languages = models.ManyToManyField(
        Language,
        related_name="situations_available_as_target",
        blank=True,
    )

    def __str__(self) -> str:
        return self.description[:50] if self.description else f"Situation #{self.pk}"


class Communication(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    situations = models.ManyToManyField(Situation, related_name="communications_of_situation", blank=True)
    description = models.TextField()
    shouldBeExpressed = models.BooleanField()
    shouldBeUnderstood = models.BooleanField()

    def __str__(self) -> str:
        return self.description[:50] if self.description else f"Communication #{self.pk}"


class Prompt(models.Model):
    situations = models.ManyToManyField(Situation, related_name="prompts", blank=True)
    description = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.description[:50] if self.description else f"Prompt #{self.pk}"


class Utterance(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    communication = models.ForeignKey(Communication, on_delete=models.CASCADE, related_name="utterances_of_communication")
    transliteration = models.CharField(max_length=255, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="utterances")
    content = models.TextField()

    def __str__(self) -> str:
        return self.communication.description[:50] if self.communication.description else f"Utterance #{self.pk}"

class ContextType(models.Model):
    name = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)
    description = models.TextField()

class Context(models.Model):
    utterance = models.ForeignKey(Utterance, on_delete=models.CASCADE, related_name="contexts")
    context_type = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "contexts"

    def __str__(self) -> str:
        return self.description[:50] if self.description else f"Context #{self.pk}"
