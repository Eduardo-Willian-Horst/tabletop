from django.contrib import admin
from .models import Room, RoomMember, Scene

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'master', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'master__username']
    readonly_fields = ['code', 'created_at', 'updated_at']

@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ['player_name', 'room', 'role', 'is_online', 'joined_at']
    list_filter = ['role', 'is_online', 'joined_at']
    search_fields = ['player_name', 'room__name', 'user__username']

@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ['name', 'room', 'is_active', 'order', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'room']
    search_fields = ['name', 'room__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['room', 'order', 'created_at']
