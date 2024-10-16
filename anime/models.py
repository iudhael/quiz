from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import random

# Create your models here.

#class Player(User):
#    pass


class Profile(models.Model):  # heritage qui créer un lien entre la representation d'une table en python et la table en elle meme en SQL

    profile_pic = models.ImageField('Photo de profile', default='default.jpg', upload_to='profile_pics')

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)





    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs): # remplacer la methode de sauvegarde por ajouter des fonctionaliter au save parent
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)  #on ouvre l'image acctuelle et on va redimentionner

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)   #redimentioner 300/300
            img.save(self.profile_pic.path)


    class Meta:
        verbose_name = "profile"


class Commentaire(models.Model): # heritage qui créer un lien entre la representation d'une table en python et la table en elle meme en SQL

    suggestion = models.TextField('suggestion')

    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    #player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.suggestion

    class Meta:
        verbose_name = "commentaire"




class Defi_quiz(models.Model): # heritage qui créer un lien entre la representation d'une table en python et la table en elle meme en SQL

    defi = models.CharField('defi', max_length=50)
    created_at = models.DateTimeField('date creation du defi', auto_now_add=True)

    title = models.CharField('titre', max_length=250)
    nature_du_defi = models.CharField('questionnaire ou puzzul', max_length=20, blank=True)
    description = models.TextField('description du defi', blank=True)

    date_de_publication = models.DateField('date de publication du defi actuel', default="2022-11-10")

    #start_date = models.DateField('date de debut du defi actuel', default="2022-11-10")

    #end_date = models.DateField('date de fin  du defi actuel', default="2022-11-10")



    image = models.ImageField('image du defi',default='default.jpg', upload_to='defi_precedents')


    class Meta:
        verbose_name = "Defi_quiz"

    def __str__(self):
        return self.defi




class Questions(models.Model):

    question = models.TextField('question')

    #choix1 = models.TextField('choix1')
    #choix2 = models.TextField('choix2')
    #choix3 = models.TextField('choix3')

    reponse = models.TextField('reponse')


    user_defi = models.ForeignKey(Defi_quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    def get_answers(self):
        choix_objs = list(Choices.objects.filter(question = self))
        random.shuffle(choix_objs)

        data = []
        for choix_obj in choix_objs:
            data.append(
                choix_obj.choix,
                #'is_correct' : choix_obj.is_correct
            )

        return data

class Choices(models.Model):
    choix = models.TextField('choix')
    is_correct = models.BooleanField('correct', default=False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)

    def __str__(self):
        return self.choix




class Score_quiz(models.Model): # heritage qui créer un lien entre la representation d'une table en python et la table en elle meme en SQL

    score = models.IntegerField('score', default=0)
    user_score = models.ForeignKey(User, on_delete=models.CASCADE)
    user_defi_score = models.OneToOneField(Defi_quiz, null=True,  on_delete=models.CASCADE)
    #player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)



    class Meta:
        verbose_name = "score_quiz"







