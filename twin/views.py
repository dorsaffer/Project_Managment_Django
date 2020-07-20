####1) from django.http import httpresponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
# create your views here.
from twin.forms import AddProjectForm,CreateUserForm
from twin.models import Project, Student, Post
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.shortcuts import render,redirect

""" 1ère Méthode d'inscription
def register_user(request):
    #if request.user.is_authenticated:
     #   return redirect('index')
    #else:
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            #user_form=form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            #messages.success(request, 'Account was created for ' + username)
            #user_form.save()
            new_user = User.objects.create_user(
            username=username, email=email,password=password,
            first_name=first_name,
            last_name=last_name,)
            new_user.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'user/register.html', context)
def login_user(request):
    #if request.user.is_authenticated:
        #return redirect('index')
    #else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect')

    a = {}
    return render(request, 'user/login.html', a)
def logout_user(request):
    logout(request)
    return redirect('index')
"""
def test(request):
    return render(request,'user/test.html')

"""1)))
def index(request):
    return httpresponse("you're looking to the index page.")
def projects(request):
    return httpresponse("you're looking to the projects page.")

def project_details(request, pid):
    return httpresponse("you're looking to the projet %s details page." % pid)
"""

def index(request):
    return render(request, 'index.html')
#1)
def list_projects(request):
    projects_list = Project.objects.all()
    output= ','.join([p.nom_du_projet for p in projects_list])
    return HttpResponse(output)
#2)
def projects(request):
    projects_list = Project.objects.all()
    return render(request, 'projects.html', {'projects_list': projects_list})
#3)
@login_required(login_url='login')
def project_details(request, pId):
    #project = get_object_or_404(Project, pk=pId)
    project=Project.objects.get(pk=pId)
    #project = Project.objects.get(Project, pk=pId)
    return render(request, 'project_details.html', {'project': project})
#4)
def edit_project(request, pId):
    """
    Methode permettant à un étudiant de éditer son propre projet
    :param request:
    :param p_id:
    :return:
    """
    project = get_object_or_404(Project, pk=pId)
    if request.method == "GET": #recuperer le formulaire
        genForm = AddProjectForm(instance=project)
        return render(request, 'edit_project.html', {'form': genForm, 'p_id': pId})
    # s'il s'agit d'une demande POST, nous devons traiter les données du formulaire
    if request.method == "POST":
        # créer une instance de formulaire et la remplir avec les données de la demande
        genForm = AddProjectForm(request.POST, instance=project)
        if genForm.is_valid():
            genForm.save()
            return HttpResponseRedirect(reverse('liste'))
        else:
            return HttpResponseRedirect(reverse('liste'))
def Delete_project(request, id):
    project = get_object_or_404(Project, pk=id)
    project.delete()
    return HttpResponseRedirect(reverse('liste'))
@login_required(login_url='login')
def add_project(request):
    if request.method == "GET":
        form = AddProjectForm()
        return render(request, 'add_project.html', {'form': form})

    if request.method == "POST":
        form = AddProjectForm(request.POST)
        if form.is_valid():
            postProject = form.save(commit=False)#commit pour recevoir les instances
            # de modèles non enregistrées
            postProject.save()
            return HttpResponseRedirect(reverse('liste'))
        else:
            return render(request, 'add_project.html',
                          {'msg_erreur': 'Erreur lors de la création du projet',
                           'form':form})
def index_post(request):
    posts=Post.objects.all()
    return render(request,'blog/index.html',{'posts':posts})
def show_post(request,id):
    posts = get_object_or_404(Post,pk=id)
    #try:
    # posts = Post.objects.get(pk=id)
    # except Post.DoesNotExist:
    #    raise Http404("Sorry! The post {} was not Find".format(id))
    return render(request, 'blog/show.html', {'posts': posts})

def search(request):
    if 'nom' in request.GET and request.GET['nom']:
        nom = request.GET['nom']
        project = Project.objects.filter(nom_du_projet__icontains=nom)
        return render(request, 'search_results.html',
        {'project': project, 'query': nom})
    else:
        return HttpResponse('Veuillez définir votre requête.')

def search_form(request):
    return render(request,'search_form.html')