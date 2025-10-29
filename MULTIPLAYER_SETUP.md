# Setup Multiplayer - Instruções Finais

## ✅ O que já foi feito:

1. ✅ Dependências adicionadas (channels, channels-redis, daphne)
2. ✅ Models criados (Room, RoomMember)
3. ✅ WebSocket Consumer implementado
4. ✅ Django Channels configurado
5. ✅ Views criadas (login, register, dashboard, salas)
6. ✅ URLs configuradas

## 📋 Próximos Passos Necessários:

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar Migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Criar Templates

Precisa criar os seguintes templates em `grid/templates/grid/`:

#### `login.html` - Tela de Login
- Formulário com username e password
- Link para registro
- Link para "Entrar como Jogador"

#### `register.html` - Registro de Mestre  
- Formulário com username, email, password, confirm password
- Link para login

#### `player_join.html` - Entrada de Jogador
- Formulário com nome do jogador e código da sala
- Não precisa criar conta

#### `dashboard.html` - Dashboard do Mestre
- Lista de salas do mestre
- Botão para criar nova sala
- Link para cada sala com código
- Botão de deletar sala

#### `master_room.html` - Sala do Mestre
- Mesma interface do `infinite_grid.html` atual
- Adicionar WebSocket connection
- Enviar updates para jogadores em tempo real

#### `player_room.html` - Sala do Jogador  
- Mesma interface mas SEM controles de edição
- Apenas visualização
- Recebe updates via WebSocket em tempo real

### 4. Atualizar JavaScript para Multiplayer

No `master_room.html`, adicionar:

```javascript
// Conectar WebSocket
const roomCode = "{{ room.code }}";
const ws = new WebSocket(`ws://${window.location.host}/ws/room/${roomCode}/`);

ws.onopen = () => {
    console.log('Conectado à sala');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'member_joined') {
        console.log('Jogador entrou:', data.member);
    } else if (data.type === 'member_left') {
        console.log('Jogador saiu:', data.member);
    }
};

// Modificar autoSaveCurrentScene para enviar via WebSocket
function autoSaveCurrentScene() {
    if (!currentScene) return;
    
    clearTimeout(autoSaveTimeout);
    autoSaveTimeout = setTimeout(() => {
        saveCurrentScene();
        showAutosaveIndicator();
        
        // Enviar update para jogadores
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                action: 'update_scene',
                scene_data: captureCurrentState()
            }));
        }
    }, 500);
}
```

No `player_room.html`, adicionar:

```javascript
// Conectar WebSocket
const roomCode = "{{ room.code }}";
const ws = new WebSocket(`ws://${window.location.host}/ws/room/${roomCode}/`);

ws.onopen = () => {
    console.log('Conectado à sala');
    // Pedir estado inicial
    ws.send(JSON.stringify({action: 'get_state'}));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'room_state') {
        // Carregar estado inicial
        loadState(data.data.scene_data);
    } else if (data.type === 'scene_update') {
        // Atualizar cena em tempo real
        loadState(data.scene_data);
    }
};

// Desabilitar todos os controles para jogadores
document.querySelectorAll('button, input').forEach(el => {
    if (!el.id || !el.id.includes('zoom')) {
        el.disabled = true;
    }
});

// Desabilitar arraste de tokens
canvas.style.pointerEvents = 'none';
// Mas manter pan e zoom
canvas.addEventListener('wheel', handleZoom);
canvas.addEventListener('mousedown', handlePan);
```

### 5. Executar com Daphne

Para WebSockets funcionarem, use:

```bash
daphne -b 0.0.0.0 -p 8000 infinite_grid.asgi:application
```

Ou para desenvolvimento:
```bash
python manage.py runserver
# Daphne é usado automaticamente se estiver instalado
```

## 🎮 Fluxo de Uso:

### Como Mestre:
1. Registrar conta em `/register/`
2. Login em `/login/`
3. Dashboard mostra suas salas
4. Criar nova sala - gera código único
5. Entrar na sala e preparar cenas
6. Compartilhar código com jogadores
7. Tudo que o mestre faz é transmitido em tempo real

### Como Jogador:
1. Acessar `/player/join/`
2. Digitar nome e código da sala
3. Entrar na sala em modo visualização
4. Ver tudo em tempo real conforme mestre altera

## 🔧 Recursos Implementados:

- ✅ Sistema de contas para mestres
- ✅ Geração automática de códigos de sala
- ✅ WebSocket para sincronização em tempo real
- ✅ Jogadores podem entrar sem conta
- ✅ Apenas mestre pode editar
- ✅ Jogadores veem tudo em tempo real
- ✅ Sistema de membros online/offline
- ✅ Persistência de estado da sala

## 📝 Observações:

- LocalStorage ainda funciona para salvar cenas localmente
- WebSocket sincroniza entre mestre e jogadores
- Para produção, use Redis como Channel Layer (não InMemory)
- Configure ALLOWED_HOSTS em produção
- Use HTTPS/WSS em produção

## 🚀 Para Produção:

Em `settings.py`, trocar:
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

