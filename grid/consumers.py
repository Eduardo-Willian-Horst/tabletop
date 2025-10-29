import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Room, RoomMember, Scene

class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'game_room_{self.room_code}'
        self.user = self.scope['user']
        
        # Verifica se o usuário pode entrar na sala
        can_join = await self.check_room_access()
        
        if not can_join:
            await self.close()
            return
        
        # Entra no grupo da sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Marca membro como online
        await self.set_member_online(True)
        
        # Envia estado atual da sala para o novo membro
        room_data = await self.get_room_data()
        await self.send(text_data=json.dumps({
            'type': 'room_state',
            'data': room_data
        }))
        
        # Notifica outros membros
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'member_joined',
                'member': await self.get_member_info()
            }
        )
    
    async def disconnect(self, close_code):
        # Marca membro como offline
        await self.set_member_online(False)
        
        # Notifica outros membros
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'member_left',
                'member': await self.get_member_info()
            }
        )
        
        # Sai do grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        # Verifica se é mestre
        is_master = await self.is_room_master()
        
        if action == 'update_scene' and is_master:
            # Mestre atualiza a cena
            scene_data = data.get('scene_data')
            await self.save_scene_data(scene_data)
            
            # Broadcast para todos os jogadores
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'scene_update',
                    'scene_data': scene_data
                }
            )
        
        elif action == 'get_state':
            # Jogador pede estado atual
            room_data = await self.get_room_data()
            await self.send(text_data=json.dumps({
                'type': 'room_state',
                'data': room_data
            }))
    
    # Handlers para mensagens do grupo
    async def scene_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'scene_update',
            'scene_data': event['scene_data']
        }))
    
    async def member_joined(self, event):
        await self.send(text_data=json.dumps({
            'type': 'member_joined',
            'member': event['member']
        }))
    
    async def member_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'member_left',
            'member': event['member']
        }))
    
    # Database queries
    @database_sync_to_async
    def check_room_access(self):
        try:
            room = Room.objects.get(code=self.room_code, is_active=True)
            
            # Se for usuário autenticado (mestre)
            if self.user.is_authenticated:
                # Verifica se é o mestre
                if room.master == self.user:
                    # Cria ou atualiza membro
                    RoomMember.objects.update_or_create(
                        room=room,
                        user=self.user,
                        defaults={
                            'player_name': self.user.username,
                            'role': 'master'
                        }
                    )
                    return True
            
            # Para jogadores anônimos, verificamos na sessão
            player_name = self.scope['session'].get('player_name')
            if player_name:
                # Cria membro como jogador
                RoomMember.objects.get_or_create(
                    room=room,
                    player_name=player_name,
                    defaults={'role': 'player'}
                )
                return True
            
            return False
        except Room.DoesNotExist:
            return False
    
    @database_sync_to_async
    def is_room_master(self):
        if not self.user.is_authenticated:
            return False
        try:
            room = Room.objects.get(code=self.room_code)
            return room.master == self.user
        except Room.DoesNotExist:
            return False
    
    @database_sync_to_async
    def get_room_data(self):
        try:
            room = Room.objects.get(code=self.room_code)
            
            # Buscar cena ativa da sala
            active_scene = room.scenes.filter(is_active=True).first()
            scene_data = active_scene.scene_data if active_scene else {}
            
            return {
                'code': room.code,
                'name': room.name,
                'scene_data': scene_data,
                'members': list(room.members.values('player_name', 'role', 'is_online'))
            }
        except Room.DoesNotExist:
            return None
    
    @database_sync_to_async
    def save_scene_data(self, scene_data):
        try:
            room = Room.objects.get(code=self.room_code)
            
            # Atualizar cena ativa
            active_scene = room.scenes.filter(is_active=True).first()
            if active_scene:
                active_scene.scene_data = scene_data
                active_scene.save()
            
            # Também salvar em current_scene_data para compatibilidade (se existir)
            if hasattr(room, 'current_scene_data'):
                room.current_scene_data = scene_data
                room.save()
        except Room.DoesNotExist:
            pass
    
    @database_sync_to_async
    def get_member_info(self):
        player_name = self.user.username if self.user.is_authenticated else self.scope['session'].get('player_name')
        return {
            'player_name': player_name,
            'role': 'master' if self.user.is_authenticated else 'player'
        }
    
    @database_sync_to_async
    def set_member_online(self, is_online):
        try:
            room = Room.objects.get(code=self.room_code)
            if self.user.is_authenticated:
                RoomMember.objects.filter(room=room, user=self.user).update(is_online=is_online)
            else:
                player_name = self.scope['session'].get('player_name')
                RoomMember.objects.filter(room=room, player_name=player_name).update(is_online=is_online)
        except Room.DoesNotExist:
            pass

