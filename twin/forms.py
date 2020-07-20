from django import forms

from .models import Project

from django import forms
from django.forms import Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('nom_du_projet',
                  'duree_du_projet',
                  'temps_alloue_par_le_createur',
                  'besoins',
                  'description',
                  'createur',
                  )
        widgets = {'besoins': Textarea(attrs={'cols': 20, 'rows': 20})}

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
