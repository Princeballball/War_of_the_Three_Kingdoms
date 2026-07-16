from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PrivateRoomJoinForm, RoomCreateForm
from .models import Room
from .services import join_auto_room, join_room, leave_room


def home_view(request):
    public_rooms = (
        Room.objects
        .filter(room_type=Room.RoomType.PUBLIC, status=Room.Status.WAITING)
        .prefetch_related('memberships')
    )
    return render(
        request,
        'index.html',
        {
            'public_rooms': public_rooms,
            'room_form': RoomCreateForm(),
            'private_join_form': PrivateRoomJoinForm(),
        },
    )


@login_required
@require_POST
def create_room_view(request):
    form = RoomCreateForm(request.POST)
    if form.is_valid():
        room = form.save(commit=False)
        room.created_by = request.user
        if room.room_type == Room.RoomType.PRIVATE:
            room.code = form.cleaned_data['private_code']
        room.save()
        join_room(room, request.user)
        messages.success(request, f'已建立{room.get_room_type_display()}「{room.name}」，房號：{room.code}。')
        return redirect('room:detail', code=room.code)
    else:
        messages.error(request, '開房失敗，請確認房間名稱與類型。')
    return redirect('home')


@login_required
@require_POST
def join_public_room_view(request, room_id):
    room = get_object_or_404(Room, pk=room_id, room_type=Room.RoomType.PUBLIC)
    _, success, message = join_room(room, request.user)
    if success:
        messages.success(request, message)
        return redirect('room:detail', code=room.code)
    else:
        messages.error(request, message)
    return redirect('home')


@login_required
@require_POST
def join_private_room_view(request):
    form = PrivateRoomJoinForm(request.POST)
    if not form.is_valid():
        messages.error(request, '請輸入正確的房間號碼。')
        return redirect('home')

    room = Room.objects.filter(code=form.cleaned_data['code'], room_type=Room.RoomType.PRIVATE).first()
    if room is None:
        messages.error(request, '找不到這個私人房號。')
        return redirect('home')

    _, success, message = join_room(room, request.user)
    if success:
        messages.success(request, message)
        return redirect('room:detail', code=room.code)
    else:
        messages.error(request, message)
    return redirect('home')


@login_required
@require_POST
def auto_match_view(request):
    room, success, message = join_auto_room(request.user)
    if success:
        messages.success(request, message)
        return redirect('room:detail', code=room.code)
    else:
        messages.error(request, message)
    return redirect('home')


@login_required
def detail_view(request, code):
    room = get_object_or_404(
        Room.objects.prefetch_related('memberships__user'),
        code=code.upper(),
    )
    if not room.memberships.filter(user=request.user).exists():
        raise Http404('你不在這個房間裡。')

    memberships = list(room.memberships.all())
    seats = memberships + [None] * (room.max_players - len(memberships))
    return render(request, 'room/detail.html', {'room': room, 'seats': seats})


@login_required
@require_POST
def leave_view(request, code):
    room = get_object_or_404(Room, code=code.upper())
    deleted = leave_room(room, request.user)
    if deleted:
        messages.success(request, '你已離開房間，房間已無玩家並自動關閉。')
    else:
        messages.success(request, '你已離開房間。')
    return redirect('home')
