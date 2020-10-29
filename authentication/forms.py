from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=_('Required. Add a valid email address.'))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', )


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'password')

	def clean(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			password = self.cleaned_data['password']
			if not authenticate(username=username, password=password):
				raise forms.ValidationError(_("Invalid login"))
















