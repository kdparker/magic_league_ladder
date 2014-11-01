from django.db import models

class Player(models.Model):
	"""
	Model used to track a specific player. 
	"""

	STARTING_RATING = 1000 # Default elo value for all players in league (new players start with this rating)

	name = models.CharField(max_length=200)
	game_wins = models.IntegerField(default=0)
	game_losses = models.IntegerField(default=0)
	match_wins = models.IntegerField(default=0)
	match_losses = models.IntegerField(default=0)
	elo = models.IntegerField(default=STARTING_RATING)

	def __unicode__(self):
		"""
		Example: Keegan - 1232
		"""
		return self.name + " - " + str(self.elo)

	def game_win_percent(self):
		""""
		Returns a formatted string as a percentage of games won by player
		"""
		return '{:.2%}'.format(float(self.game_wins) / float(self.game_wins + self.game_losses))

	def match_win_percent(self):
		""""
		Returns a formatted string as a percentage of matches won by player
		"""
		return '{:.2%}'.format(float(self.match_wins) / float(self.match_wins + self.match_losses))

class Match(models.Model):
	"""
	Model used to track a specific match. Contains history data to allow for later
	implementation of backtracking (ie taking back a match).
	"""
	add_date = models.DateTimeField('date added')
	winning_player = models.ForeignKey(Player, related_name="match_winning_player")
	losing_player = models.ForeignKey(Player, related_name="match_losing_player")
	games_played = models.IntegerField(default=2)
	losers_prev_elo = models.IntegerField(default=0)
	winners_prev_elo = models.IntegerField(default=0)
	losers_new_elo = models.IntegerField(default=0)
	winners_new_elo = models.IntegerField(default=0)

	def __unicode__(self):
		"""
		Example: Winner over Loser in 2 on Oct 21, 10:32 pm
		"""
		return self.winning_player.name + " over " + self.losing_player.name + " in " + str(self.games_played) + " on " + str(self.add_date)

	def rating_change(self):
		"""
		Returns the rating change that happened from this game (since they are symmetric)
		"""
		return int(self.winners_new_elo) - int(self.winners_prev_elo) # Sometimes these fields return doubles, so we cast them as integers