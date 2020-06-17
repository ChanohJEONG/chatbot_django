from django.forms import forms, TextInput, PasswordInput
import django.forms as forms
from .models import Member,diary_answer


class LoginForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ['user_id', 'user_pw']
        widgets = {
            'user_id': TextInput(),
            'user_pw': PasswordInput(),
        }

class Diary_Post(forms.ModelForm):

    class Meta:
        model = diary_answer
        fields = ['useranswer']
        widgets = {'useranswer': TextInput(),}
