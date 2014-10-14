from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from elo_ladder.models import Player, Match

def rating_change(winner, loser, games):
	if games == 3: K=64
	else: K=48

	EA = 1.0/(1+10**((loser.elo - winner.elo)/400.0))
	EB = 1.0/(1+10**((winner.elo - loser.elo)/400.0))

	change = (K*(1 - EA), K*(0 - EB))
	return change

def standings(request):
	players = Player.objects.order_by('-elo')
	return render(request, 'elo_ladder/standings.html', {'players': players})

def report(request):
	players = Player.objects.order_by('id')
	return render(request, 'elo_ladder/report.html', {'players': players})

def make_report(request):
	players = Player.objects.order_by('id')
	winner_id = request.POST['winner']
	loser_id = request.POST['loser']
	games = int(request.POST['games'])
	if winner_id == loser_id:
		return render(request, 'elo_ladder/report.html', 
			{'message': "You selected the same person to win and lose. Try again.", 'players': players})
	else:
		winner = get_object_or_404(Player, pk=winner_id)
		loser = get_object_or_404(Player, pk=loser_id)
		change = rating_change(winner, loser, games)
	
		winner.elo += change[0]
		winner.match_wins += 1
		winner.game_wins += 2
		winner.game_losses += games - 2
		winner.save()

		loser.elo += change[1]
		loser.match_losses += 1
		loser.game_wins += games - 2
		loser.game_losses += 2
		loser.save()

		match = Match(add_date = timezone.now(), 
					  winning_player = winner, 
					  losing_player = loser, 
					  games_played=games)
		match.save()

		return HttpResponseRedirect(reverse('standings'))
