from django.forms import ModelForm
from django.forms import ModelForm, TextInput, EmailInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.utils import ErrorList

from .models import Profile, Questions
class ParagraphErrorList(ErrorList):

# gerer la maniere dont apparait les erreur ici les fait apparaitre sous forme de paragraphe au lieu de <li></li>
# appeler la fonction au niveau de la vu registerpage

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return  ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="smail error">%s</p>' % e for e in self])


class CreateUserform(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({

            'placeholder':'Username...',


        })
        self.fields["email"].widget.attrs.update({

            'placeholder': 'Email...'

        })
        self.fields["password1"].widget.attrs.update({

            'placeholder': 'Password...'

        })
        self.fields["password2"].widget.attrs.update({

            'placeholder': 'Re-enter password...'

        })


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#formulaire de mise a jour des identifiants username et email
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


#formulaire de mise a jour de la photo de profile
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']


