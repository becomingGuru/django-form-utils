r"""
Tests for django-form-utils

Time-stamp: <2008-10-13 13:05:51 carljm __init__.py>


forms
=====

>>> from django import forms

>>> from form_utils.forms import BetterForm


Define a ``BetterForm`` with a couple fieldsets:

>>> class MyForm(BetterForm):
...     one = forms.CharField()
...     two = forms.CharField()
...     three = forms.CharField()
...     class Meta:
...         fieldsets = (('main', {'fields': ('two',), 'legend': ''}),
...                      ('Advanced', {'fields': ('three', 'one')}))


Subclass it, and override one of those fieldsets:

>>> class YourForm(MyForm):
...     four = forms.CharField()
...     class Meta:
...         fieldsets = (('main', {'fields': ('four', 'two'), 'legend': ''}),) 

>>> yf = YourForm()


We can iterate over the fieldset, and within each fieldset iterate
over the ``BoundFields``.  We get the superclass fieldsets that were
not overridden by the subclass:

>>> for fs in yf.fieldsets:
...     print fs
...     for f in fs:
...         print f
Fieldset('main', ['four', 'two'], legend='', description='')
<input type="text" name="four" id="id_four" />
<input type="text" name="two" id="id_two" />
Fieldset('Advanced', ['three', 'one'], legend='Advanced', description='')
<input type="text" name="three" id="id_three" />
<input type="text" name="one" id="id_one" />


>>> from form_utils.tests.models import FieldsetTestModel
>>> from form_utils.forms import BetterModelForm


Create and test a ``BetterModelForm`` with a couple fieldsets:

>>> class MyModelForm(BetterModelForm):
...     additional = forms.CharField()
...     class Meta:
...         model = FieldsetTestModel
...         fieldsets = (('main', {'fields': ('one', 'additional', 'blah'),
...                                'legend': ''}),
...                      ('More', {'fields': ('two',),
...                                'description': 'Something more'}))

>>> mmf = MyModelForm()

>>> for fs in mmf.fieldsets:
...     print fs
...     for f in fs:
...         print f
Fieldset('main', ['one', 'additional'], legend='', description='')
<input type="text" name="one" id="id_one" />
<input type="text" name="additional" id="id_additional" />
Fieldset('More', ['two'], legend='More', description='Something more')
<input type="text" name="two" id="id_two" />


``BetterModelForm``s can also be subclassed:

>>> class YourModelForm(MyModelForm):
...     more = forms.CharField()
...     class Meta(MyModelForm.Meta):
...         fieldsets = (('Some', {'fields': ('additional', 'one')}),
...                      ('More', {'fields': ('more', 'two')}))

>>> ymf = YourModelForm()

>>> for fs in ymf.fieldsets:
...     print fs
...     for f in fs:
...         print f
Fieldset('main', ['one', 'additional'], legend='', description='')
<input type="text" name="one" id="id_one" />
<input type="text" name="additional" id="id_additional" />
Fieldset('More', ['more', 'two'], legend='More', description='')
<input type="text" name="more" id="id_more" />
<input type="text" name="two" id="id_two" />
Fieldset('Some', ['additional', 'one'], legend='Some', description='')
<input type="text" name="additional" id="id_additional" />
<input type="text" name="one" id="id_one" />


If we don't define the fieldsets, by default we get a single "main"
fieldset that includes all fields:

>>> class AnotherForm(BetterForm):
...     one = forms.CharField()
...     two = forms.CharField()

>>> af = AnotherForm()
>>> for fs in af.fieldsets:
...     print fs
...     for f in fs:
...         print f
Fieldset('main', ['one', 'two'], legend='', description='')
<input type="text" name="one" id="id_one" />
<input type="text" name="two" id="id_two" />


Can still iterate over fields directly in a BetterForm:

>>> for field in af:
...     print field
<input type="text" name="one" id="id_one" />
<input type="text" name="two" id="id_two" />


Test defining row_attrs:

>>> class AttrsForm(BetterForm):
...     one = forms.CharField()
...     two = forms.CharField(required=False)
...     class Meta:
...         row_attrs = {'one': {'style': 'display: none'}}

>>> af = AttrsForm()
>>> for field in af:
...     print "%s: '%s'" % (field.name, field.row_attrs)
one: ' style="display: none" class="required"'
two: ' class="optional"'

>>> for fs in af.fieldsets:
...     for field in fs:
...         print "%s: '%s'" % (field.name, field.row_attrs)
one: ' style="display: none" class="required"'
two: ' class="optional"'


Template filters
================

>>> from django.conf import settings
>>> import os
>>> _old_template_dirs = settings.TEMPLATE_DIRS
>>> settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

>>> from form_utils.templatetags.form_utils_tags import render

>>> class PlainForm(forms.Form):
...     one = forms.CharField()

>>> pf = PlainForm()

>>> render(pf)
u'\n\n<input type="text" name="one" id="id_one" />\n\n\n\n'

>>> render(af)
u'\nfieldset main\n\n\n<input type="text" name="one" id="id_one" />\n\n<input type="text" name="two" id="id_two" />\n\n\n\n\n'

>>> render(af, 'form_utils/other_form.html')
 u'<h1>Other form</h1>\n\n\n<input type="text" name="one" id="id_one" />\n\n<input type="text" name="two" id="id_two" />\n\n\n\n\n'

>>> settings.TEMPLATE_DIRS = _old_template_dirs
"""
