from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
def is_esprit_mail(value):
    """Tests if an email end with @esprit.tn"""
    if str(value).endswith("@esprit.tn") == False:
	#raise genere une exception
        raise ValidationError("Votre  mail doit être @esprit.tn", params={'value': value})
        """raise lève une exception"""

class User(models.Model):
    nom = models.CharField('Prenom', max_length=30)
    prenom = models.CharField('Nom', max_length=30)
    email = models.EmailField('Email', validators=[is_esprit_mail])

    # str fortement recommendé càd la méthode d'affichage sera par user
    def __str__(self):
        return self.nom


class Student(User):
    pass

class Coach(User):
    pass
###########
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Ce champs sera modifié à la création
    updated_at=models.DateTimeField(auto_now=True)##modifier pour chaque update
    #Rajouter les meta donnée à notre class
    class Meta:
        abstract=True # pour dire que cette classe est une classe abstraite
        #et pour dire que cette classe on ne la considère pas comme etant
        # un modele c'est juste une classe utilitaure a fin d'éviter de dupliquer le code
        #classe abstraite=classe qu'on ne peut pas instancier

class Project(TimeStampedModel):
    nom_du_projet = models.CharField('Titre du projet', max_length=30)
    duree_du_projet = models.IntegerField('Duree estimee', default=0)
    temps_alloue_par_le_createur = models.IntegerField('Temps alloue', validators=[MinValueValidator(1), MaxValueValidator(10)])
    besoins = models.TextField(max_length=250)
    description = models.TextField(max_length=250)
    #created_at=models.DateTimeField(auto_now_add=True)#Ce champs sera modifié à la création
    #updated_at=models.DateTimeField(auto_now=True)##modifier pour chaque update

    # Validation State of the project
    est_valide = models.BooleanField(default=False)

    createur = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='project_owner'
    )

    superviseur = models.ForeignKey(
        Coach,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='project_coach'
    )

    membres = models.ManyToManyField(
        Student,
        through='MembershipInProject',
        # added to differ with the lead relation
        related_name='les_membres',
        blank=True,
    )

    def __str__(self):
        return self.nom_du_projet

    def get_related_members(self):
        return self.membres.all()

    def total_allocated_by_members(self):
        list_members_in_p = MembershipInProject.objects.filter(projet=self.pk)
        sum_invested_by_members = list_members_in_p.all().aggregate(Sum('time_allocated_by_member'))
        # Utiliser Aggregate pour regroupe les valeurs à aggrégé dans un dictionnaire
        return sum_invested_by_members['time_allocated_by_member__sum'] or 0
        # Récupération de la valeur à partir du dictionnnaire


class MembershipInProject(models.Model):
    projet = models.ForeignKey(Project, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Student, on_delete=models.CASCADE)
    time_allocated_by_member = models.IntegerField('Temps alloué par le membre')

    def __str__(self):
        return 'Membre ' + self.etudiant.nom

    # Meta pr dire ne peu pas etre dupliqué ds notre projet
    class Meta:
        unique_together = ("projet", "etudiant")
class Post(TimeStampedModel):
    title=models.CharField(max_length=255)
    body=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Ce champs sera modifié à la création
    updated_at = models.DateTimeField(auto_now=True)  # modifier pour chaque update
    def __str__(self):
        return self.title