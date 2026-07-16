from django.contrib import admin

from .models import Room, RoomMembership


class RoomMembershipInline(admin.TabularInline):
    model = RoomMembership
    extra = 0
    readonly_fields = ('joined_at',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'room_type', 'status', 'created_by', 'created_at', 'started_at')
    list_filter = ('room_type', 'status')
    search_fields = ('name', 'code', 'created_by__username')
    inlines = [RoomMembershipInline]


@admin.register(RoomMembership)
class RoomMembershipAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'joined_at')
    search_fields = ('room__name', 'room__code', 'user__username')
