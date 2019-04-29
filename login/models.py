from django.db import models

# Create your models here.


class Player(models.Model):
    playerID = models.AutoField(db_column='playerID', primary_key=True)
    playerName = models.CharField(db_column='Name', max_length=40)
    playerPhone = models.CharField(db_column='telephone', max_length=11)
    playerMail = models.CharField(db_column='mailbox', max_length=80)
    password = models.CharField(db_column='password', max_length=400)

    class Meta:
        db_table = 'player_table'

