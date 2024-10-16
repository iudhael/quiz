import datetime
import random
from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader


#from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, ParagraphErrorList

from django.contrib import messages
from .forms import CreateUserform
from .models import Profile, Score_quiz, Commentaire, Questions, Defi_quiz,  Choices,User
from django.db import transaction, IntegrityError

# Create your views here.


global start_date, end_date, last_defi_id, total_defis

start_date = f"{date.today().year}-{date.today().month}-01"
end_date = f"{date.today().year}-{date.today().month}-27"
last_defi_id = Defi_quiz.objects.filter(date_de_publication__range=[start_date, end_date]).latest('pk')
total_defis = Defi_quiz.objects.filter(date_de_publication__lt=start_date) #recuperer totale des defis jusquau start_date

print(start_date)



# cette restriction peut etre fait pour d'autre vue en ajoutant @login_required(login_url='anime:login') au debut
@login_required(login_url='anime:login') # permet de rstreindre la vue home si la personne n'est pas connecter il n'a pas accec a home

def home(request):
    """
    start_date = f"{date.today().year}-0{date.today().month}-01"
    end_date = f"{date.today().year}-{date.today().month}-27"
    print(start_date)

    last_defi_id = Defi_quiz.objects.filter(date_de_publication__range=[start_date, end_date]).latest('pk')

    defis_precedent = Defi_quiz.objects.get(pk=(last_defi_id.id - 1))

    print(defis_precedent) #afficher le defi du immediatement avant celle du defi actuel

    defi_avenir =  Defi_quiz.objects.get(pk=(last_defi_id.id + 1)) # recuperer l'id du defi actuel + 1
    print(defi_avenir)

    context = {

        'defi_precedent':defis_precedent,
        'last_defi_id': last_defi_id,
        'defi_avenir': defi_avenir,

    }
    """
    context = {


    }


    return render(request, 'anime/acceuil.html', context)

@login_required(login_url='anime:login')
def profileuser(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        # enregistrer si les 2 formulaire sont valide
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Account has been updated!! ')

            return redirect('anime/profile.html')

    else:
        user_form = UserUpdateForm(instance=request.user)

        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form

    }

    return render(request, 'anime/profile.html', context)



def registerpage(request):

    # si la personne est autentifié
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserform()
        if request.method == 'POST':
            form = CreateUserform(request.POST, error_class=ParagraphErrorList)
            if form.is_valid():
                form.save()

                #recuperation du username pour le message de confirmation
                username = form.cleaned_data.get('username')

                #message de confirmation de creation de compte
                messages.success(request, 'Account was created for ' + username)

                # apres inscription on le redirige a la page de connexion
                return redirect('login')

    context = {'form':form}

    return render(request, 'anime/register.html', context)




def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            #demander le nom et le passe
            username = request.POST.get('username')
            password = request.POST.get('password')

            #verifier si l'utilisateur existe dans la bdd
            user = authenticate(request, username=username, password=password)

            #si il existe on le redirige a la page d'acceuil
            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                #dans le cas ou l'utilisateur n'existe pas ou a mal taper ses identifiants un message est envoyé
                messages.info(request, 'Username OR Password is incorrect')



        context = {}
        return render(request, 'anime/login.html', context)



def logoutuser(request):
    logout(request)
    return redirect('login')



"""
def defi_jouer(request):
    try:

        Score_quiz.objects.create(score=score, user_score_id=request.user.id, user_defi_score_id=last_defi_id.id)
    except:
        print("deja un score")
        return render(request, 'anime/deja_jouer.html', {})
    else:
        print("pas encore de score")
"""





def defi_actuel(request):



    print(last_defi_id.id)

    print(request.user)
    titre = Defi_quiz.objects.filter(date_de_publication__range=[start_date, end_date]).latest('pk')

    jeus = Questions.objects.filter(user_defi_id=last_defi_id)





    question_objs = list(jeus)


    random.shuffle(question_objs)


    nature = last_defi_id.nature_du_defi
    print(nature)

    if nature == "questionnaire" :

        if request.method == 'POST':
            #print(request.POST)



            score = 0
            wrong = 0
            correct = 0
            total = 0
            choix = []
            for question_obj in question_objs:

                choices = Choices.objects.filter(choix=request.POST.get(question_obj.question)).values('is_correct')
                for choice in choices:

                    choix = choice["is_correct"]
                    print(choix)


                total += 1
                #print(question_obj.question)
                #print(question_obj.reponse)
                print()
                if choix == True:
                    print(request.POST.get(question_obj.question))
                    score += 10
                    correct += 1
                else:

                        print(request.POST.get(question_obj.question))
                        wrong += 1
            percent = score / (total * 10) * 100


            #defi_jouer(request)
            try:

                Score_quiz.objects.create(score=score, user_score_id=request.user.id,
                                          user_defi_score_id=last_defi_id.id)
            except:
                print("deja un score")
                return render(request, 'anime/deja_jouer.html', {})
            else:
                print("pas encore de score")

            context = {
                'score': score,

                'correct': correct,
                'wrong': wrong,
                'percent': percent,
                'total': total,

                'jeus': jeus,


                'titre': titre,
                'question_objs': question_objs,
            }
            return render(request, 'anime/result.html', context)
        else:

            context = {


                'jeus': jeus,

                'titre': titre,
                'question_objs': question_objs,

            }
            return render(request, 'anime/defi_actuels/defi_actuel_questionnaire.html', context)

        #return render(request, 'anime/defi_actuels/defi_actuel_questionnaire.html', context)



    elif nature == "puzzul":

        context = {
            'titre': titre,
        }
        return render(request, 'anime/defi_actuels/defi_actuel_pezzul.html', context)



def defis_precedent(request):
    # date de debut du defi actuel mois actuel
    #start_date = f"{date.today().year}-0{date.today().month}-01"


    total_defi = len(total_defis)-1 #exclure le dernier defi c'est a dire le defi de date start_date


    # trier les defi par date de publication recent au ancien
    # recuperer les defis inferieur a start_date
    defi = Defi_quiz.objects.filter(date_de_publication__lt=start_date).order_by('-date_de_publication')

    print(start_date)
    #print(defis)


    context ={

        'defi': defi,
        }

    return render(request, 'anime/defi_precedent.html', context)


def detail(request, defi_quiz_id):

    defi_precedent_id = get_object_or_404(Defi_quiz, pk=defi_quiz_id)
    print(defi_precedent_id.nature_du_defi)

    print(f"{defi_precedent_id.id} et {last_defi_id.id}")

    if defi_precedent_id.id == last_defi_id.id:
        return redirect('anime:defi_actuel')  # restreindre l'acces a la page de defi actuel

        #parce que si le joueur y accede il pourra y jouer et un score lui sera afficher alors que il ne peut pas avoir un score si il y a deja jouer


    elif defi_precedent_id.id > last_defi_id.id:
        pass  # rediriger vers la page d'erreur 404

        # restreindre l'acces au defi dont l'id est superieur  a l'id du defi actuel


    else: #si le defi demander est un defi precedent on lui affiche les details (question ou puzzul)
        if defi_precedent_id.nature_du_defi == "questionnaire":

            defi_precedent = Questions.objects.filter(user_defi_id=defi_quiz_id)
            question_objs = list(defi_precedent)
            #print(question_objs)

            random.shuffle(question_objs)

            if request.method == 'POST':
                # print(request.POST)

                score = 0
                wrong = 0
                correct = 0
                total = 0
                choix = []
                for question_obj in question_objs:

                    choices = Choices.objects.filter(choix=request.POST.get(question_obj.question)).values('is_correct')
                    for choice in choices:
                        choix = choice["is_correct"]
                        print(choix)

                    total += 1
                    # print(question_obj.question)
                    # print(question_obj.reponse)
                    print()
                    if choix == True:
                        print(request.POST.get(question_obj.question))
                        score += 10
                        correct += 1
                    else:

                        print(request.POST.get(question_obj.question))
                        wrong += 1
                percent = score / (total * 10) * 100
                context = {
                    'score': score,

                    'correct': correct,
                    'wrong': wrong,
                    'percent': percent,
                    'total': total,

                    'defi_precedent_id': defi_precedent_id,
                    'question_objs': question_objs,
                }
                return render(request, 'anime/result.html', context)
            else:

                context = {
                    'question_objs': question_objs,
                    'defi_precedent_id': defi_precedent_id,
                }
                return render(request, 'anime/defi_precedents/detail_defi_precedent.html', context)



            #return render(request, 'anime/defi_precedents/detail_defi_precedent.html', context)
        elif defi_precedent_id.nature_du_defi == "puzzul":
            context = {
                'defi_precedent_id': defi_precedent_id,
            }
            return render(request, 'anime/defi_precedents/defi_precedent_pezzul.html', context)







def defis_avenir(request):
    #start_date = f"{date.today().year}-0{date.today().month}-01"
    #end_date = f"{date.today().year}-{date.today().month}-27"
    print(start_date)

    #last_defi_id = Defi_quiz.objects.filter(date_de_publication__range=[start_date, end_date]).latest('pk')

    defis_avenir = Defi_quiz.objects.get(pk=(last_defi_id.id + 1))

    context = {
        'defis_avenir': defis_avenir,

    }

    return render(request, 'anime/defi_avenir.html', context)



# envoyer des informations au serveur  comme parametre avec GET (methode 2)
def search(request):

    query = request.GET.get('query') # avec GET tous ce qui est taper dans l'url comme recherche est capturer



    if not query:
        title_defi = total_defis # total des defi precedent
        print(total_defis)
    else:
        #title_defi = total_defis.filter(title__icontains=query)  # title__icontains contient la requette qui est le titre mais pas exactement le titre de l'album si le titre est mal taper ou imcomplet
        title_defi = Defi_quiz.objects.filter(date_de_publication__lt=start_date, title__icontains=query)
        #print(total_defis)

        if not title_defi.exists():
            title_defi = Questions.objects.filter(user_defi__title__icontains=query) # chercher dans la table  les noms qui correspondent aux requette et renvoyer des album
            print(total_defis)



    title = "Résultats pour la requête %s"%query
    context = {
        'title_defi': title_defi,
        'title': title
    }

    return render(request, 'anime/search.html', context)













