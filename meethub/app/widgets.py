from django.core import validators
from django.forms import *
from django.shortcuts import render
from django.template import Context
from django.template import loader
from django.utils.safestring import mark_safe


class UserCarouselMultiSelectWidget(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None):
        t = loader.get_template('widgets/users_carousel.html')
        c = Context({"users": self.choices, "selected_ids": value})
        rendered = t.render(c)
        return mark_safe(rendered)


class Html5Date(DateTimeInput):
    input_type = "date"


class Html5Time(DateTimeInput):
    input_type = "time"
