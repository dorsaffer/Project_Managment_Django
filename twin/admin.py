from django.contrib import admin,messages
from .models import *

class MembershipInline(admin.StackedInline):
    model = MembershipInProject
    extra = 0


# Register your models here.
class ProjetDureeListFilter(admin.SimpleListFilter):
    title = ('Duree')
    parameter_name = 'duree'
    def lookups(self, request, model_admin):
        return (
            ('1 mois', ("moins d'un mois")),
            ('3 mois', ("Plus que 1 mois"))
        )
    def queryset(self, request, queryset):
        if self.value() == '1 month':
            return queryset.filter(duree_du_projet__lte=30)
        if self.value() == '3 mois':
            #lte  less then or equeal
            #gte greather tha or equal
            return queryset.filter(duree_du_projet__lte=90, duree_du_projet__gte=30)

class ProjetAdmin(admin.ModelAdmin):
    ######## 1)
    """hedhi el button """
    actions = ['set_to_valid', 'set_to_no_valid']
    def set_to_valid(self, request, queryset):
        queryset.update(est_valide=True)
    set_to_valid.short_description = "Valider"
    ##########
    ### 4)
    #inlines = (MembershipInline)
    def set_to_no_valid(self,request,queryset):
        rows_no_valid=queryset.filter(est_valide=False)
        if rows_no_valid.count() > 0:
            messages.error(request, "%s projects valide= false" % rows_no_valid.count())
        else:
            rows_updated = queryset.update(est_valide=False)
            if rows_updated == 1:

                message = "1 project was"
            else:
                message = "%s projects were" % rows_updated
            self.message_user(request, level='success', message="%s successfully marked as not valid" % message)

    set_to_no_valid.short_description = "Refuser"
    list_display = ('nom_du_projet', 'duree_du_projet', 'description', 'est_valide', 'createur', 'total_allocated_by_members','superviseur')
    fieldsets = (
       ('Etat', {'fields': ('est_valide',)}),
      ('A propos', {
           'fields': ('nom_du_projet', ('createur', 'superviseur'), 'besoins', 'description',),
        }),
      ('Durées', {
         'fields': (('duree_du_projet', 'temps_alloue_par_le_createur'),)
      }),
    )
    list_per_page = 2 #paggination
    #desecndre l'action en bas
    actions_on_bottom = True
    actions_on_top = False
    list_filter = ('createur__prenom',ProjetDureeListFilter)######Liste de recherche par createur
    ##### 5) Barre de recherche
    search_fields = ['nom_du_projet', 'createur__nom']

    inlines = (MembershipInline,)
    ##### 2)


#@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email')
    fields = (('nom', 'prenom'), 'email')
    ordering = ['prenom']
    ##########
    ##### 3)



class StudentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email')
    """hedhi bech n display les champs exaxtement"""
    fields = (('nom', 'prenom'), 'email')
    """hedhi bech fel affichage fel add yjiw nom and prenom fields bahdha b3adhom"""
    #ordering = ['prenom']
    search_fields = ['nom', 'prenom']



admin.site.register(Student, StudentAdmin)
admin.site.register(Coach,CoachAdmin)
admin.site.register(Project, ProjetAdmin)
admin.site.register(Post)