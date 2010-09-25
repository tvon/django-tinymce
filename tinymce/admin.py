from django.contrib import admin

from tinymce.models import Style, Format


class InlineStyleAdmin(admin.StackedInline):
    model = Style


class FormatAdmin(admin.ModelAdmin):

    list_display = ['title', 'enabled', 'position']
    list_editable = ['enabled', 'position']
    inlines = [InlineStyleAdmin,]


admin.site.register(Format, FormatAdmin)
