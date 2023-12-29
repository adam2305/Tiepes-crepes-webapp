from django.shortcuts import render,get_object_or_404,redirect
from .models import Commande,Profile
from django.views import View 
from .forms import RegisterForm,UpdateProfileForm,UpdateUserForm,commandeAdd,NotificationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from webpush import send_group_notification
from .apps import utilisateurs
from django.contrib.auth.models import User 
from django.utils import timezone

# Create your views here.

def home(request):
    webpush = {"group": 'all' }
    return render(request,'users/homepage.html',{"webpush":webpush})

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key':'name'}
    template = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request,self.template,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid()  :
            test_email = len(User.objects.filter(email=form.cleaned_data.get('email')))
            if test_email > 0:
                messages.error(request, "Ce mail existe déjà")
                return render(request,self.template,{'form':form})
            if form.cleaned_data.get('email') in utilisateurs:
                print("valid")
                form.save()
                username = username = form.cleaned_data.get('username')
                messages.success(request, f'Compte creé pour {username}')
                return redirect(to="/")
            else:
                messages.error(request, f"vous ne pouvez pas créer un compte vous n'êtes pas cotisant")
                return render(request,self.template,{'form':form})
        print("not valid")
        return render(request,self.template,{'form':form})

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    def get_sucess_url(self):
        return reverse_lazy('tasks')
    def form_invalid(self,form):
        print("mauvais mdp")
        messages.error(self.request,'Identifiant ou mot de passe incorrect')
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profil modfié')
            return redirect(to='/profile_overview')
    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)
        user_form = UpdateUserForm(instance=request.user)
    context = {
        'profile_form' : profile_form,
        'user_form' : user_form}
    return render(request, "users/profile.html",context)

@login_required
def profile_overview(request):
    total_commande = len(Commande.objects.filter(user=request.user.username))
    context = {
        'total_commande' : total_commande
    }
    return render(request,"users/profile_overview.html",context)

@login_required
def commander(request):
    nombre_clients = len(Profile.objects.all())
    nombre_livraisons = len(Commande.objects.all())
    nombre_en_cours = len(Commande.objects.filter(delivered=False))
    commandes_en_cours = Commande.objects.filter(user=request.user.username,delivered=False)
    attente = False
    if len(commandes_en_cours) > 0:
        attente = True 
    print("test")
    if request.method == 'POST':
        commande_form = commandeAdd(request.POST)
        if commande_form.is_valid() :
            n_produit = commande_form.cleaned_data['produit']
            n_toppig = commande_form.cleaned_data['topping']
            n_adresse = commande_form.cleaned_data['adresse']
            n_remarque = commande_form.cleaned_data['remarque']
            n_user = request.user.username
            n_date = timezone.now()
            new_command = Commande(user=n_user,produit=n_produit,topping=n_toppig,adresse=n_adresse,remarque=n_remarque,date=n_date)
            try:
                if not attente:
                    new_command.save()
                    messages.success(request,'Commande effectuée !!')
                else:
                   messages.error(request, " Vous avez déjà une commande en attente !!!!") 
            except:
                message.error(request, "Nous avons pas reussi à prendre vôtre commande")
            return redirect(to="/commander")
    else:
        commande_form = commandeAdd()
    context = {
                'attente' : attente,
                'commande_form' : commande_form,
                'clients': nombre_clients,
                'livraisons':nombre_livraisons,
                'en_cours':nombre_en_cours
            }
    return render(request,"users/commander.html", context)

def info(request):
    return render(request,'users/info.html')

def planning(request):
    return render(request,'users/planning.html')

@login_required
def notification(request):
    if not request.user.is_superuser:
        print("ok")
        return redirect(to="/")
    else:
        if request.method == 'POST':
            notification_form = NotificationForm(request.POST)
            if notification_form.is_valid():
                payload = {
                    "head": notification_form.cleaned_data['head'],
                    "body": notification_form.cleaned_data['body'],
                    "icon": notification_form.cleaned_data['icon'],
                    "url": notification_form.cleaned_data['url']
                }
                send_group_notification(group_name="all", payload=payload, ttl=2500)
                return redirect(to="/notification")
            else:
                messages.error(request,"Erreur pour générer la notificaton")
                return redirect(to="/notification")
        else:    
            notification_form = NotificationForm()
            context = {
                "notification_form": notification_form
            }
            return render(request,"users/notification.html",context)

