from django.forms import ModelForm, DecimalField, modelformset_factory#, CharField
from django.forms.widgets import Select
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Bb, Rubric

class BbForm(ModelForm):
	class Meta:
		model = Bb # класс модели с которой связана  форма
		fields = ('title', 'content', 'price', 'rubric') # последовательность из имен полей модели, которые должны присутствоать в форме
		labels = {'title': 'Название товара'}
		help_texts = {'rubric': 'Не забудьте задать рубрику!'}
		field_classes = {'price': DecimalField}
		#widgets = {'rubric': Select(attrs={'size': 8})}
	def clean(self):
		super().clean()
		errors = {}
		if not self.cleaned_data['content']:
			errors['content'] = ValidationError('Укажите описание провадаемого товара')
		if self.cleaned_data['price'] < 0:
			errors['price'] = ValidationError('Укажите неотрицательное значение цены')
		if errors:
			raise ValidationError(errors)

#class RegisterUserForm(ModelForm):
#	password1 = CharField(label = 'Пароль')
#	password2 = CharField(label = 'Пароль (повторно)')#

#	class Meta:
#		model = User
#		fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

RubricFormSet = modelformset_factory(Rubric, fields=('name',), can_order=True, can_delete=True)