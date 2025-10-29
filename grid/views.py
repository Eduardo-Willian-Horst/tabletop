from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Room, RoomMember, Scene
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import cloudinary.uploader
import base64
from io import BytesIO

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    
    return render(request, 'grid/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'As senhas não coincidem')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('dashboard')
    
    return render(request, 'grid/register.html')

def player_join_view(request):
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        room_code = request.POST.get('room_code')
        
        try:
            room = Room.objects.get(code=room_code.upper(), is_active=True)
            
            # Salva nome do jogador na sessão
            request.session['player_name'] = player_name
            request.session['room_code'] = room.code
            
            return redirect('player_room', room_code=room.code)
        except Room.DoesNotExist:
            messages.error(request, 'Sala não encontrada')
    
    return render(request, 'grid/player_join.html')

@login_required
def dashboard_view(request):
    # Salas do mestre
    master_rooms = Room.objects.filter(master=request.user).order_by('-updated_at')
    
    return render(request, 'grid/dashboard.html', {
        'master_rooms': master_rooms
    })

@login_required
def create_room_view(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        
        if room_name:
            room = Room.objects.create(
                name=room_name,
                master=request.user
            )
            
            # Cria membro mestre
            RoomMember.objects.create(
                room=room,
                user=request.user,
                player_name=request.user.username,
                role='master'
            )
            
            messages.success(request, f'Sala criada! Código: {room.code}')
            return redirect('master_room', room_code=room.code)
    
    return redirect('dashboard')

@login_required
def master_room_view(request, room_code):
    room = get_object_or_404(Room, code=room_code, master=request.user)
    
    return render(request, 'grid/master_room.html', {
        'room': room,
        'is_master': True
    })

def player_room_view(request, room_code):
    room = get_object_or_404(Room, code=room_code, is_active=True)
    
    player_name = request.session.get('player_name')
    if not player_name:
        messages.error(request, 'Você precisa entrar com um nome')
        return redirect('player_join')
    
    return render(request, 'grid/player_room.html', {
        'room': room,
        'is_master': False,
        'player_name': player_name
    })

@login_required
@require_http_methods(["POST"])
def delete_room_view(request, room_code):
    room = get_object_or_404(Room, code=room_code, master=request.user)
    room.delete()
    messages.success(request, 'Sala deletada com sucesso')
    return redirect('dashboard')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso')
    return redirect('login')

# ==================== API de Cenas ====================

@login_required
@require_http_methods(["GET"])
def list_scenes_api(request, room_code):
    """Lista todas as cenas de uma sala"""
    room = get_object_or_404(Room, code=room_code, master=request.user)
    scenes = room.scenes.all().values('id', 'name', 'scene_data', 'is_active', 'order', 'created_at', 'updated_at')
    return JsonResponse({'scenes': list(scenes)})

@login_required
@require_http_methods(["POST"])
def create_scene_api(request, room_code):
    """Cria uma nova cena"""
    room = get_object_or_404(Room, code=room_code, master=request.user)
    
    try:
        data = json.loads(request.body)
        name = data.get('name')
        scene_data = data.get('scene_data', {})
        
        if not name:
            return JsonResponse({'error': 'Nome da cena é obrigatório'}, status=400)
        
        # Verificar se já existe cena com esse nome
        if Scene.objects.filter(room=room, name=name).exists():
            return JsonResponse({'error': 'Já existe uma cena com esse nome'}, status=400)
        
        # Criar cena
        scene = Scene.objects.create(
            room=room,
            name=name,
            scene_data=scene_data,
            is_active=not room.scenes.exists(),  # Primeira cena é ativa
            order=room.scenes.count()
        )
        
        return JsonResponse({
            'id': scene.id,
            'name': scene.name,
            'scene_data': scene.scene_data,
            'is_active': scene.is_active,
            'order': scene.order,
            'created_at': scene.created_at.isoformat(),
            'updated_at': scene.updated_at.isoformat()
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

@login_required
@require_http_methods(["PUT"])
def update_scene_api(request, room_code, scene_id):
    """Atualiza uma cena existente"""
    room = get_object_or_404(Room, code=room_code, master=request.user)
    scene = get_object_or_404(Scene, id=scene_id, room=room)
    
    try:
        data = json.loads(request.body)
        
        if 'name' in data:
            scene.name = data['name']
        if 'scene_data' in data:
            scene.scene_data = data['scene_data']
        if 'is_active' in data:
            scene.is_active = data['is_active']
        if 'order' in data:
            scene.order = data['order']
        
        scene.save()
        
        return JsonResponse({
            'id': scene.id,
            'name': scene.name,
            'scene_data': scene.scene_data,
            'is_active': scene.is_active,
            'order': scene.order,
            'updated_at': scene.updated_at.isoformat()
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

@login_required
@require_http_methods(["DELETE"])
def delete_scene_api(request, room_code, scene_id):
    """Deleta uma cena"""
    room = get_object_or_404(Room, code=room_code, master=request.user)
    scene = get_object_or_404(Scene, id=scene_id, room=room)
    
    scene.delete()
    
    return JsonResponse({'success': True})

@login_required
@require_http_methods(["POST"])
def switch_scene_api(request, room_code, scene_id):
    """Troca para uma cena específica"""
    room = get_object_or_404(Room, code=room_code, master=request.user)
    scene = get_object_or_404(Scene, id=scene_id, room=room)
    
    # Marcar como ativa (o save do model cuida de desativar outras)
    scene.is_active = True
    scene.save()
    
    return JsonResponse({
        'id': scene.id,
        'name': scene.name,
        'scene_data': scene.scene_data,
        'is_active': scene.is_active
    })

@csrf_exempt
@require_http_methods(["POST"])
def upload_image_api(request):
    """Faz upload de imagem para o Cloudinary"""
    try:
        # Pode ser um arquivo direto ou base64
        if request.FILES.get('image'):
            # Upload de arquivo direto
            image_file = request.FILES['image']
            result = cloudinary.uploader.upload(
                image_file,
                folder="rpg_grid",
                resource_type="auto"
            )
        elif request.POST.get('image_data'):
            # Upload de base64
            image_data = request.POST.get('image_data')
            
            # Remove o prefixo data:image/...;base64, se existir
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            result = cloudinary.uploader.upload(
                f"data:image/png;base64,{image_data}",
                folder="rpg_grid",
                resource_type="auto"
            )
        else:
            return JsonResponse({'error': 'Nenhuma imagem fornecida'}, status=400)
        
        return JsonResponse({
            'success': True,
            'url': result['secure_url'],
            'public_id': result['public_id']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
