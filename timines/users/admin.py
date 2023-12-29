from django.contrib import admin
from .models import Commande,Profile
from django.contrib.auth.models import User
# Register your models here.

class CommandeAdmin(admin.ModelAdmin):
	list_display = ('user','date', 'produit', 'topping','remarque','adresse','delivered')


	def CommandeEffectué(modeladmin,request,queryset):
		queryset.update(delivered=True)

	def has_add_permission(self, request):
		return False

	admin.site.add_action(CommandeEffectué, "Commande livrée")

admin.site.register(Commande,CommandeAdmin)
admin.site.register(Profile)