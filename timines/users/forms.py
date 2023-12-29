from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from .models import Profile,Commande
from django.core.validators import MaxValueValidator, MinValueValidator

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Identifiant','class': 'form-control',}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'form-control',}))
    password1 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe','class': 'form-control','data-toggle': 'password','id': 'password',}))
    password2 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer mot de passe','class': 'form-control','data-toggle': 'password','id': 'password',}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
	username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control',}))
	password = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','data-toggle': 'password','id': 'password','name': 'password',}))

	class Meta:
		model = User 
		fields = ['username','password']

class UpdateProfileForm(forms.ModelForm):
    chambre = forms.CharField(widget=forms.TextInput({'placeholder':'chambre'}))
    class Meta:
        model = Profile
        fields = ['chambre']

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput({'placeholder':'Identifiant'}) )
    class Meta:
        model = User
        fields = ['username']

class commandeAdd(forms.ModelForm):
    TOPPING =(
        ('R','nature'),
        ('S','sucre'),
        ('N','nutella'),
        ('C','combinaison')
    )
    produit = forms.IntegerField()
    topping = forms.ChoiceField(choices=TOPPING)
    adresse = forms.CharField()
    remarque = forms.CharField(required=False,widget=forms.Textarea(attrs={ 'rows':3, 'cols':20}))
    class Meta:
        model = Commande
        fields = ['produit','topping','adresse','remarque']

class NotificationForm(forms.Form):
    head = forms.CharField(widget=forms.TextInput({'placeholder':'Titre'}))
    body = forms.CharField(widget=forms.TextInput({'placeholder':'contenu'}))
    icon = forms.CharField(widget=forms.TextInput({'placeholder':'image (lien)'}))
    url = forms.CharField(widget=forms.TextInput({'placeholder':'lien de la notif'}))