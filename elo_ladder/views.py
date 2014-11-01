from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from elo_ladder.models import Player, Match

def rating_change(winner, loser, games):
	""" elo rating calculation according to this page: http://en.wikipedia.org/wiki/Elo_rating_system
			Using K factor of 60 for games in 2 and a K factor of 48 for game in 3.
	"""
	if games == 2: K=60
	else: K=48

	EA = 1.0/(1+10**((loser.elo - winner.elo)/400.0))

	change = K*(1 - EA)
	return change

def standings(request):
	"""View to send standings data based on template in elo_ladder/standings.html"""
	players = Player.objects.order_by('-elo')
	return render(request, 'elo_ladder/standings.html', {'players': players})

def history(request):
	"""View to send history data based on template in elo_ladder/history.html"""
	matches = Match.objects.order_by('-add_date')
	return render(request, 'elo_ladder/history.html', {'matches': matches})

def report(request):
	"""View to send data to form page with template in elo_ladder/report.html"""
	players = Player.objects.order_by('id')
	return render(request, 'elo_ladder/report.html', {'players': players})

def player_details(request, player_id):
	"""View to send player data corresponding to player_id to page with template in elo_ladder/player_details.html"""
	p = get_object_or_404(Player, pk=player_id)
	player_matches = Match.objects.filter(winning_player=player_id) | Match.objects.filter(losing_player=player_id)
	player_matches = player_matches.order_by('-add_date')
	""" Make the list of matches a list of tuples.
			The first entry is a boolean stating if player corresponding to player_id won.
			The second entry is the match un-altered."""
	player_matches = map((lambda x: (x.winning_player.id==int(player_id), x)), player_matches)

	return render(request, 'elo_ladder/player_details.html', {'player': p, 'matches': player_matches})

def make_report(request):
	"""Calculates change in rating based on data received from form. 
	   Returns back to report page if user gives invalid input (duplicate players).
	   After changes are done in database, send the user back to standings with a message regarding successful submission."""
	players = Player.objects.order_by('id')
	winner_name = request.POST['winner']
	loser_name = request.POST['loser']
	games = int(request.POST['games'])
	if winner_name == loser_name:
		messages.error(request, "You selected the same person to win and lose. Try again.")
		return render(request, 'elo_ladder/report.html', {'players': players})
	else:
		player_objects = Player.objects.all()
		print player_objects

		for object in player_objects:
			if winner_name == object.name:
				winner = object
				break
		else:
			raise Http404

		for object in player_objects:
			if loser_name == object.name:
				loser = object
				break
		else:
			raise Http404
		change = rating_change(winner, loser, games)
	
		winner.elo += change
		winner.match_wins += 1
		winner.game_wins += 2
		winner.game_losses += games - 2

		loser.elo -= change
		loser.match_losses += 1
		loser.game_wins += games - 2
		loser.game_losses += 2

		match = Match(add_date = timezone.now(), 
					  winning_player = winner, 
					  losing_player = loser, 
					  games_played=games,
					  losers_prev_elo=loser.elo+change,
					  winners_prev_elo=winner.elo-change,
					  losers_new_elo=loser.elo,
					  winners_new_elo=winner.elo)
		
		loser.save()
		winner.save()
		match.save()

		messages.success(request, "Submission successful! " + winner.name + " gained " + str(match.rating_change()) + " rating," + \
			" and " + loser.name + " lost " + str(match.rating_change()) + " rating.")
		return HttpResponseRedirect(reverse('standings'))
