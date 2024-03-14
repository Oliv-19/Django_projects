from django import forms    
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class TypesForm(forms.Form):
    sortTypes = forms.ChoiceField(label='Filter By:',required=False,choices=[(x, x) for x in ['All','Book', 'movies', 'serie', 'Games']])


class FilterForm(forms.Form):
    sortFilter = forms.ChoiceField(label='Order By:',required=False,choices=[(x, x) for x in ['All','Latest', 'Oldest']])

    

class FilterFormTwo(forms.Form):
    sortFilterTwo = forms.ChoiceField(label='Order By:',required=False,choices=[(x, x) for x in ['All','Latest', 'Oldest', 'Latest Addition', 'Oldest Addition', 'Rating ASC', 'Rating DESC']])


class TypesFormTwo(forms.Form):
    sortTypesTwo = forms.ChoiceField(label='Type of content:',required=False,choices=[(x, x) for x in ['Book', 'movies', 'serie', 'Games']])