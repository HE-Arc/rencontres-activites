from django.forms import *
from django.shortcuts import render
from django.template import Context
from django.template import loader
from django.utils.safestring import mark_safe


class UserCarouselMultiSelectWidget(CheckboxSelectMultiple):

    def render(self, name, value, attrs=None):
        """
        Renders a checkbox group with a custom template
        TODO: user renders_options
        Hide checkboxes to use a simple link click --> invite | uninvite
        :param name:
        :param value:
        :param attrs:
        :return:
        """
        t = loader.get_template('widgets/users_carousel.html')
        c = Context({"users": self.choices,"selected_ids":value})
        rendered = t.render(c)
        return mark_safe(rendered)
