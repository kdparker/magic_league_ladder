from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Player(models.Model):
	"""
	Model used to track a specific player. Extends user with a one to one field.
	"""

	STARTING_RATING = 1000 # Default elo value for all players in league (new players start with this rating)

	user = models.OneToOneField(User, default=0)
	game_wins = models.IntegerField(default=0)
	game_losses = models.IntegerField(default=0)
	match_wins = models.IntegerField(default=0)
	match_losses = models.IntegerField(default=0)
	elo = models.IntegerField(default=STARTING_RATING)

	def get_name(self):
		return self.user.first_name + " " + self.user.last_name[0]

	def __unicode__(self):
		"""
		Example: Keegan P - 1232
		"""
		return self.get_name() + " - " + str(self.elo)

	def game_win_percent(self):
		""""
		Returns a formatted string as a percentage of games won by player
		"""
		if (self.game_wins + self.game_losses == 0): return "N/A"
		return '{:.2%}'.format(float(self.game_wins) / float(self.game_wins + self.game_losses))

	def match_win_percent(self):
		""""
		Returns a formatted string as a percentage of matches won by player
		"""
		if (self.match_wins + self.match_losses == 0): return "N/A"
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
	reporter = models.ForeignKey(User, default=0)

	def __unicode__(self):
		"""
		Example: Winner over Loser in 2 on Oct 21, 10:32 pm
		"""
		return self.winning_player.get_name() + " over " + self.losing_player.get_name() + " in " + str(self.games_played) + " on " + str(self.add_date)

	def rating_change(self):
		"""
		Returns the rating change that happened from this game (since they are symmetric)
		"""
		return int(self.winners_new_elo) - int(self.winners_prev_elo) # Sometimes these fields return doubles, so we cast them as integers

class ResetPage(models.Model):
	"""
	Model used to track the reset password pages we create to send to users if they forget their password.
	"""
	add_date = models.DateTimeField('date added')
	user = models.ForeignKey(User, default=0)
	code = models.TextField(primary_key=True)
	used = models.BooleanField(default=False)

	def is_active(self):
		"""
		If a reset password page has not been used, and isn't older than a day, it is active
		"""
		d = timezone.now() - timedelta(days=1)
		return (not self.used) and (self.add_date > d)

	def __unicode__(self):
		"""
		Example: USER - active
		"""
		if self.is_active():
			return self.user.username + " - active"
		else:
			return self.user.username + " - inactive"