from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile, Commentaire, Questions, Score_quiz, Defi_quiz, Choices
from django.contrib.auth.admin import UserAdmin


# Register your models here.


admin.site.register(Profile)
admin.site.register(Commentaire)


admin.site.register(Score_quiz)
admin.site.register(Defi_quiz)






class ChoiceAdmin(admin.StackedInline):
    model = Choices
    extra = 0



class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceAdmin, ]


admin.site.register(Questions, QuestionAdmin)
admin.site.register(Choices)






