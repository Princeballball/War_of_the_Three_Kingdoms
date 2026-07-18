from django.contrib import admin

from .models import Game, GameCard, GamePlayer


class GamePlayerInline(admin.TabularInline):
    model = GamePlayer
    extra = 0
    readonly_fields = ('joined_at',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'status', 'current_turn', 'created_at', 'started_at')
    list_filter = ('status',)
    search_fields = ('room__name', 'room__code')
    inlines = [GamePlayerInline]


@admin.register(GamePlayer)
class GamePlayerAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'seat_order', 'identity_card', 'selected_general', 'current_health', 'max_health', 'is_alive')
    list_filter = ('is_alive', 'identity_card')
    search_fields = ('game__room__code', 'user__username')
    filter_horizontal = ('general_candidates',)


@admin.register(GameCard)
class GameCardAdmin(admin.ModelAdmin):
    list_display = ('game', 'card', 'owner', 'zone', 'position')
    list_filter = ('zone', 'card__faction')
    search_fields = ('game__room__code', 'card__name', 'owner__user__username')
