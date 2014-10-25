from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from elo_ladder.models import Player, Match

def rating_change(winner, loser, games):
	if games == 2: K=64
	else: K=48

	EA = 1.0/(1+10**((loser.elo - winner.elo)/400.0))
	EB = 1.0/(1+10**((winner.elo - loser.elo)/400.0))

	change = (K*(1 - EA), K*(0 - EB))
	return change

def standings(request):
	players = Player.objects.order_by('-elo')
	return render(request, 'elo_ladder/standings.html', {'players': players})

def history(request):
	matches = Match.objects.order_by('-add_date')
	return render(request, 'elo_ladder/history.html', {'matches': matches})

def report(request):
	players = Player.objects.order_by('id')
	return render(request, 'elo_ladder/report.html', {'players': players})

def player_details(request, player_id):
	p = get_object_or_404(Player, pk=player_id)
	player_matches = Match.objects.filter(winning_player=player_id) | Match.objects.filter(losing_player=player_id)
	player_matches = player_matches.order_by('-add_date')
	player_matches = map((lambda x: (x.winning_player.id==int(player_id), x)), player_matches)
	return render(request, 'elo_ladder/player_details.html', {'player': p, 'matches': player_matches})

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
		winner.game_win_percent = float(winner.game_wins) / float(winner.game_wins + winner.game_losses) * 100.0
		winner.match_win_percent = float(winner.match_wins) / float(winner.match_wins + winner.match_losses) * 100.0

		loser.elo += change[1]
		loser.match_losses += 1
		loser.game_wins += games - 2
		loser.game_losses += 2
		loser.game_win_percent = float(loser.game_wins) / float(loser.game_wins + loser.game_losses) * 100.0
		loser.match_win_percent = float(loser.match_wins) / float(loser.match_wins + loser.match_losses) * 100.0


		match = Match(add_date = timezone.now(), 
					  winning_player = winner, 
					  losing_player = loser, 
					  games_played=games,
					  losers_prev_elo=loser.elo-change[1],
					  winners_prev_elo=winner.elo-change[0],
					  losers_new_elo=loser.elo,
					  winners_new_elo=winner.elo)
		
		loser.save()
		winner.save()
		match.save()

		return HttpResponseRedirect(reverse('standings'))
