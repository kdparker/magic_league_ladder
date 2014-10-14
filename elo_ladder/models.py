from django.db import models

class Player(models.Model):
	name = models.CharField(max_length=200)
	game_wins = models.IntegerField(default=0)
	game_losses = models.IntegerField(default=0)
	match_wins = models.IntegerField(default=0)
	match_losses = models.IntegerField(default=0)
	elo = models.IntegerField(default=1000)

	def __unicode__(self):
		return self.name + " - " + str(self.elo)

class Match(models.Model):
	add_date = models.DateTimeField('date added')
	winning_player = models.ForeignKey(Player, related_name="match_winning_player")
	losing_player = models.ForeignKey(Player, related_name="match_losing_player")
	games_played = models.IntegerField(default=2)