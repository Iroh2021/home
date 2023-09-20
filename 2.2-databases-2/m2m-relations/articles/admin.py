from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_main = 0
        for form in self.forms:
            data = form.cleaned_data
            if data.get('is_main'):
                count_main += 1
            else:
                continue


        if count_main == 0:
            raise ValidationError('Укажите основной тэг')

        if count_main > 1:
            raise ValidationError('Основным может быть только один тэг')

        return super().clean() 


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [ScopeInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']