from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from elo_ladder.models import Player, Match

def rating_change(winner, loser):
	if winner.match_wins + winner.match_losses < 5: K_W = 64
	else: K_W = 32

	if loser.match_wins + loser.match_losses < 5: K_L = 64
	else: K_L = 32

	EA = 1/(1+10**((winner.elo - loser.elo)/400))
	EB = 1/(1+10**((loser.elo - winner.elo)/400))

	change = (K_W*(1 - EA), K_L*(0 - EB))
	return change

def standings(request):
	players = Player.objects.order_by('-elo')
	return render(request, 'elo_ladder/standings.html', {'players'= players})

def report_results(request):
	players = Player.objects.all()
	winner_id = request.POST['winner']
	loser_id = request.POST['loser']
	games = int(request.POST['games'])
	if winner_id = loser_id:
		return render(request, 'elo_ladder/report_results.html', 
			{'message': "You selected the same person to win and lose. Try again.",})
	else:
		winner = get_object_or_404(Player, pk=winner_id)
		loser = get_object_or_404(Player, pk=winner_id)
		change = rating_change(winner, loser)
	
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



def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
