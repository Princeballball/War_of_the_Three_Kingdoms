from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from card.models import Card

from .models import Game, GameCard
from .services import assign_missing_general_candidates, choose_general, draw_for_turn, end_turn, respond_with_card, use_hand_card


@login_required
def detail_view(request, game_id):
    game = get_object_or_404(
        Game.objects.select_related('room', 'current_turn').prefetch_related(
            'players__user',
            'players__identity_card',
            'players__selected_general',
            'players__general_candidates',
            'players__cards__card',
        ),
        pk=game_id,
    )
    assign_missing_general_candidates(game)
    current_player = (
        game.players
        .filter(user=request.user)
        .select_related('identity_card', 'selected_general')
        .prefetch_related('general_candidates')
        .first()
    )
    if current_player is None:
        raise Http404('你不在這場遊戲裡。')

    return render(
        request,
        'game/detail.html',
        {
            'game': game,
            'players': game.players.all(),
            'current_player': current_player,
            'hand_cards': current_player.cards.filter(zone=GameCard.Zone.HAND).select_related('card').order_by('position', 'id'),
            'equipment_cards': current_player.cards.filter(zone=GameCard.Zone.EQUIPMENT).select_related('card').order_by('position', 'id'),
            'judgment_cards': current_player.cards.filter(zone=GameCard.Zone.JUDGMENT).select_related('card').order_by('-position', '-id'),
            'target_players': game.players.filter(is_alive=True).exclude(user=request.user).select_related('user').order_by('seat_order'),
            'deck_count': game.game_cards.filter(zone=GameCard.Zone.DECK).count(),
            'discard_count': game.game_cards.filter(zone=GameCard.Zone.DISCARD).count(),
            'pending_action': game.pending_action or {},
            'has_dodge': current_player.cards.filter(zone=GameCard.Zone.HAND, card__name='閃').exists(),
            'has_peach': current_player.cards.filter(zone=GameCard.Zone.HAND, card__name='桃').exists(),
        },
    )


@login_required
@require_POST
def choose_general_view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    current_player = game.players.filter(user=request.user).first()
    if current_player is None:
        raise Http404('你不在這場遊戲裡。')

    general = get_object_or_404(Card, pk=request.POST.get('general_id'))
    _, success, message = choose_general(current_player, general)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('game:detail', game_id=game.id)


@login_required
@require_POST
def draw_cards_view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    current_player = game.players.filter(user=request.user).first()
    if current_player is None:
        raise Http404('你不在這場遊戲裡。')

    success, message = draw_for_turn(game, current_player)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('game:detail', game_id=game.id)


@login_required
@require_POST
def end_turn_view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    current_player = game.players.filter(user=request.user).first()
    if current_player is None:
        raise Http404('你不在這場遊戲裡。')

    success, message = end_turn(game, current_player)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('game:detail', game_id=game.id)


@login_required
@require_POST
def use_card_view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    current_player = game.players.filter(user=request.user).first()
    if current_player is None:
        raise Http404('你不在這場遊戲裡。')

    game_card = get_object_or_404(GameCard, pk=request.POST.get('game_card_id'), game=game)
    success, message = use_hand_card(
        game,
        current_player,
        game_card,
        target_player_id=request.POST.get('target_player_id') or None,
    )
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('game:detail', game_id=game.id)


@login_required
@require_POST
def respond_view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    current_player = game.players.filter(user=request.user).first()
    if current_player is None:
        raise Http404('你不在這場遊戲裡。')

    success, message = respond_with_card(game, current_player, request.POST.get('response'))
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('game:detail', game_id=game.id)
