from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from elo_ladder.models import Player, Match
import re

def rating_change(winner, loser, games):
	""" elo rating calculation according to this page: http://en.wikipedia.org/wiki/Elo_rating_system
			Using K factor of 60 for games in 2 and a K factor of 48 for game in 3.
	"""
	if games == 2: K=60
	else: K=48

	EA = 1.0/(1+10**((loser.elo - winner.elo)/400.0))

	change = K*(1 - EA)
	return change

def is_valid_entry(entry):
	"""Returns if a given entry is a valid input"""
	return (entry and len(entry) <= 30 and len(entry) >= 4 and re.match('^[A-Za-z\-_@0-9.]*$', entry))

def is_valid_user(info):
	"""Returns if a given user_creation info is valid. If not, gives an appropriate message alongside"""
	if not is_valid_entry(info['username']): return (False, "Please enter a valid username")
	if User.objects.filter(username=info['username']): return (False, "Username taken, please select another")
	if not is_valid_entry(info['password']): return (False, "Please enter a valid password")
	if not is_valid_entry(info['confirm_password']): return (False, "Please confirm your password")
	if not (info['password'] == info['confirm_password']): return (False, "Your passwords did not match.")
	if not is_valid_entry(info['email']): return (False, "Please enter a valid e-mail")
	if User.objects.filter(username=info['email']): return (False, "Email already in use")
	if not is_valid_entry(info['first_name']): return (False, "Please enter a valid first name")
	if not is_valid_entry(info['last_name']): return (False, "Please enter a valid last name")
	return (True, "")

def standings(request):
	"""View to send standings data based on template in elo_ladder/standings.html"""
	players = Player.objects.order_by('-elo')
	return render(request, 'elo_ladder/standings.html', {'players': players})

def history(request):
	"""View to send history data based on template in elo_ladder/history.html"""
	matches = Match.objects.order_by('-add_date')
	return render(request, 'elo_ladder/history.html', {'matches': matches})

@login_required
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

def register(request):
	"""Page to allow registration from user, using generic RegisterForm from django's library"""

	registered = False

	if request.method == 'POST':
		info ={"username": request.POST['username'],"password": request.POST['password'], "confirm_password": request.POST['confirm_password'],
				"email": request.POST['email'],"first_name": request.POST['first_name'],"last_name": request.POST['last_name']}
		processed_info = is_valid_user(info)
		if processed_info[0]:
			new_user = User.objects.create_user(username=info['username'],
												email=info['email'],
												first_name=info['first_name'],
												last_name=info['last_name'])

			new_user.set_password(info['password'])
			new_user.save()

			player = Player(user=new_user)
			player.save()

			registered = True
		else:
			messages.error(request, processed_info[1])

	return render(request, 'elo_ladder/register.html', {'registered': registered})

def user_login(request):
		"""Page to allow logging in"""
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']

			user = authenticate(username=username, password=password)

			if user:
				if user.is_active:
					login(request, user)
					messages.success(request, "Welcome to the Erb Street Magic League, " + user.first_name)
					return HttpResponseRedirect(reverse('standings'))
				else:
					messages.error(request, "This account is disabled, try again.")
					return render(request, 'elo_ladder/login.html')
			else:
				messages.error(request, "Either your username or password is incorrect. Try again.")
				return render(request, 'elo_ladder/login.html')
		else:
			return render(request, 'elo_ladder/login.html')

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('standings'))

def make_report(request):
	"""Calculates change in rating based on data received from form. 
	   Returns back to report page if user gives invalid input (duplicate players).
	   After changes are done in database, send the user back to standings with a message regarding successful submission."""
	players = Player.objects.order_by('id')
	if request.user.is_authenticated():
		winner_id = request.POST['winner']
		loser_id = request.POST['loser']
		games = int(request.POST['games'])
		if winner_id == loser_id:
			messages.error(request, "You selected the same person to win and lose. Try again.")
			return render(request, 'elo_ladder/report.html', {'players': players})
		else:
			winner = get_object_or_404(Player, pk=winner_id)
			loser = get_object_or_404(Player, pk=loser_id)
			if not (winner.user == request.user or loser.user == request.user):
				messages.error(request, "You can only report a match that you are involved in.")
				return render(request, 'elo_ladder/report.html', {'players': players})
			else:
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
					  		winners_new_elo=winner.elo,
					  		reporter=request.user)
		
				loser.save()
				winner.save()
				match.save()

				messages.success(request, "Submission successful! " + winner.get_name() + " gained " + str(match.rating_change()) + " rating," + \
					" and " + loser.get_name() + " lost " + str(match.rating_change()) + " rating.")
				return HttpResponseRedirect(reverse('standings'))
	else:
		messages.error(request, "You must be logged in to report a match.")
		return render(request, 'elo_ladder/report.html', {'players': players})
