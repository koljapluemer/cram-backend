from django.contrib import admin

from .models import (
    Communication,
    Context,
    Language,
    LanguageString,
    Prompt,
    Situation,
    Utterance,
)


admin.site.register(Language)
admin.site.register(LanguageString)
admin.site.register(Situation)
admin.site.register(Communication)
admin.site.register(Prompt)
admin.site.register(Utterance)
admin.site.register(Context)
