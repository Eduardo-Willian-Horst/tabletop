from django.db import models
from django.contrib.auth.models import User
import secrets

class Room(models.Model):
    code = models.CharField(max_length=8, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='master_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    current_scene_data = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @staticmethod
    def generate_code():
        """Gera um código único de 6 caracteres"""
        while True:
            code = secrets.token_urlsafe(6)[:6].upper()
            if not Room.objects.filter(code=code).exists():
                return code
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

class RoomMember(models.Model):
    ROLE_CHOICES = [
        ('master', 'Mestre'),
        ('player', 'Jogador'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    player_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['room', 'user']
    
    def __str__(self):
        return f"{self.player_name} in {self.room.name} ({self.role})"

class Scene(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='scenes')
    name = models.CharField(max_length=100)
    scene_data = models.JSONField()  # Estado completo da cena
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)  # Cena ativa no momento
    order = models.IntegerField(default=0)  # Ordem das cenas
    
    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['room', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.room.name}"
    
    def save(self, *args, **kwargs):
        # Se esta cena está sendo marcada como ativa, desativar outras
        if self.is_active:
            Scene.objects.filter(room=self.room, is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
