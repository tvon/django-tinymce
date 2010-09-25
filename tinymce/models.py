# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.db import models
from django.contrib.admin import widgets as admin_widgets
from tinymce import widgets as tinymce_widgets

class HTMLField(models.TextField):
    """
    A large string field for HTML content. It uses the TinyMCE widget in
    forms.
    """
    def formfield(self, **kwargs):
        defaults = {'widget': tinymce_widgets.TinyMCE}
        defaults.update(kwargs)

        # As an ugly hack, we override the admin widget
        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = tinymce_widgets.AdminTinyMCE

        return super(HTMLField, self).formfield(**defaults)


class Style(models.Model):
    """A CSS style"""
    attribute = models.CharField(max_length=20)
    value = models.CharField(max_length=50)
    format = models.ForeignKey('Format', related_name='styles')


class Format(models.Model):
    """TinyMCE style for drop-down style menu"""
    title = models.CharField(max_length=20)

    inline = models.CharField(max_length=10, blank=True, help_text='Name of the inline element to produce for example "span". The current text selection will be wrapped in this inline element.')
    block = models.CharField(max_length=10, blank=True, help_text='Name of the block element to produce for example "h1". Existing block elements within the selection gets replaced with the new block element.')

    selector = models.CharField(max_length=20, blank=True, help_text='CSS 3 selector pattern to find elements within the selection by. This can be used to apply classes to specific elements or complex things like odd rows in a table.')
    classes = models.CharField(max_length=50, blank=True, help_text='Space separated list of classes to apply the the selected elements or the new inline/block element.')

    enabled = models.BooleanField()
    position = models.PositiveIntegerField(unique=True)

    def __unicode__(self):
        return self.title
        
    def as_config(self):
        result = {}
        result['title'] = self.title

        if self.inline:
            result['inline'] = self.inline
        if self.block:
            result['block'] = self.block
        if self.classes:
            result['classes'] = self.classes
        if self.selector:
            result['selector'] = self.selector
        if self.styles.all().count() > 0:
            result['styles'] = {}
            for style in self.styles.all():
                result['styles'][style.selector] = style.value

        return result