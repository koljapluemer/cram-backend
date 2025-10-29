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
    languages = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="situations_for_language")
    image_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return f"Situation #{self.pk}"


class Communication(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    situations = models.ManyToManyField(Situation, related_name="communications_of_situation", blank=True)
    descriptions = models.ManyToManyField(LanguageString, related_name="communications", blank=True)
    shouldBeExpressed = models.BooleanField()
    shouldBeUnderstood = models.BooleanField()

    def __str__(self) -> str:
        return f"Communication #{self.pk}"


class Prompt(models.Model):
    situations = models.ManyToManyField(Situation, related_name="prompts", blank=True)
    descriptions = models.ManyToManyField(LanguageString, related_name="prompts", blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Prompt #{self.pk}"


class Utterance(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    communication = models.ForeignKey(Communication, on_delete=models.CASCADE, related_name="utterances_of_communication")
    transliteration = models.CharField(max_length=255, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="utterances")
    content = models.TextField()

    def __str__(self) -> str:
        return f"Utterance #{self.pk}"

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
        return f"Context #{self.pk}"
