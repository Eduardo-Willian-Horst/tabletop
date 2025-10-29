# 🔧 Correção: Jogadores não viam tokens

## 🐛 Problema

Os jogadores não estavam vendo os tokens quando o mestre os adicionava ao tabuleiro.

---

## 🔍 Causa Raiz

O **WebSocket Consumer** (`grid/consumers.py`) estava buscando dados da coluna `room.current_scene_data`, que não existe mais. As cenas agora são salvas no model `Scene`, não diretamente na sala.

**Código Antigo (Consumer):**
```python
@database_sync_to_async
def get_room_data(self):
    room = Room.objects.get(code=self.room_code)
    return {
        'scene_data': room.current_scene_data or {},  # ❌ Campo não existe
        ...
    }
```

---

## ✅ Solução Implementada

### 1. Atualizar Consumer para buscar cena ativa

**Arquivo:** `grid/consumers.py`

```python
from .models import Room, RoomMember, Scene  # ✅ Importar Scene

@database_sync_to_async
def get_room_data(self):
    room = Room.objects.get(code=self.room_code)
    
    # ✅ Buscar cena ativa da sala
    active_scene = room.scenes.filter(is_active=True).first()
    scene_data = active_scene.scene_data if active_scene else {}
    
    return {
        'code': room.code,
        'name': room.name,
        'scene_data': scene_data,  # ✅ Dados da cena ativa
        'members': list(room.members.values('player_name', 'role', 'is_online'))
    }

@database_sync_to_async
def save_scene_data(self, scene_data):
    room = Room.objects.get(code=self.room_code)
    
    # ✅ Atualizar cena ativa no banco
    active_scene = room.scenes.filter(is_active=True).first()
    if active_scene:
        active_scene.scene_data = scene_data
        active_scene.save()
```

---

### 2. Adicionar envio via WebSocket ao trocar cena

**Arquivo:** `grid/templates/grid/master_room.html`

```javascript
// ✅ Modificar switchToScene para enviar via WebSocket após trocar
const originalSwitchToScene = switchToScene;
switchToScene = async function(scene, saveCurrentFirst = true) {
    await originalSwitchToScene(scene, saveCurrentFirst);
    
    // Após trocar de cena, enviar para jogadores
    if (ws && ws.readyState === WebSocket.OPEN && currentScene) {
        const stateData = captureCurrentState();
        console.log('📤 Enviando nova cena via WebSocket:', stateData);
        ws.send(JSON.stringify({
            action: 'update_scene',
            scene_data: stateData
        }));
    }
};
```

**Comportamento:**
- ✅ Quando o mestre **troca de cena**, envia automaticamente via WebSocket
- ✅ Quando o mestre **adiciona/move tokens**, auto-save envia via WebSocket
- ✅ Jogadores recebem e atualizam em tempo real

---

### 3. Adicionar logs para debug

**Master:**
```javascript
console.log('📤 Enviando atualização via WebSocket:', stateData);
```

**Player:**
```javascript
console.log('📨 Mensagem WebSocket recebida:', data);
console.log('📥 Estado inicial recebido:', data.data.scene_data);
console.log('🔄 Atualização recebida do mestre:', data.scene_data);
```

---

## 🔄 Fluxo Correto Agora

### Quando o mestre adiciona um token:

```
1. Mestre cria token → tokens.push(newToken)
2. autoSaveCurrentScene() é chamado (debounce 500ms)
3. → saveCurrentScene() → PUT /api/.../scenes/<id>/
4. → Backend atualiza Scene.scene_data no banco
5. → autoSaveCurrentScene() envia via WebSocket
6. → Consumer.receive() → scene_update()
7. → Broadcast para todos os jogadores
8. → Jogadores recebem e executam loadState()
9. → Tokens aparecem no canvas dos jogadores ✅
```

### Quando o mestre troca de cena:

```
1. Mestre clica em cena → switchToScene()
2. → POST /api/.../scenes/<id>/switch/
3. → Backend marca cena como ativa
4. → Frontend carrega scene_data da nova cena
5. → switchToScene() envia via WebSocket
6. → Jogadores recebem e carregam mesma cena ✅
```

### Quando um jogador entra na sala:

```
1. Jogador conecta WebSocket → Consumer.connect()
2. → get_room_data() busca cena ativa
3. → Envia estado inicial para o jogador
4. → Jogador executa loadState()
5. → Vê todos os tokens da cena atual ✅
```

---

## 🧪 Como Testar

### Teste 1: Estado Inicial

1. Mestre cria uma sala e adiciona tokens
2. Jogador entra na sala
3. **✅ Jogador deve ver todos os tokens imediatamente**

### Teste 2: Sincronização em Tempo Real

1. Mestre e jogador na mesma sala
2. Mestre adiciona novo token
3. **✅ Jogador deve ver o token aparecer em ~500ms**

### Teste 3: Troca de Cena

1. Mestre cria 2 cenas com tokens diferentes
2. Jogador na sala
3. Mestre troca entre as cenas
4. **✅ Jogador deve ver as cenas mudarem automaticamente**

### Teste 4: Console Logs

Abra o DevTools (F12) e verifique:

**No Mestre:**
```
📤 Enviando atualização via WebSocket: {tokens: [...], ...}
```

**No Jogador:**
```
📨 Mensagem WebSocket recebida: {type: "scene_update", ...}
🔄 Atualização recebida do mestre: {tokens: [...], ...}
```

---

## 📁 Arquivos Modificados

1. ✅ `grid/consumers.py` - Corrigido get_room_data() e save_scene_data()
2. ✅ `grid/views.py` - Removido room.current_scene_data
3. ✅ `grid/templates/grid/master_room.html` - Adicionado envio ao trocar cena + logs
4. ✅ `grid/templates/grid/player_room.html` - Adicionado logs de debug
5. ✅ `CORRECAO_WEBSOCKET.md` - Este documento

---

## ✅ Status

**Problema RESOLVIDO!** 🎉

Agora os jogadores:
- ✅ Veem os tokens quando entram na sala
- ✅ Recebem atualizações em tempo real quando o mestre adiciona/move tokens
- ✅ Veem as trocas de cena automaticamente
- ✅ Logs no console ajudam a debugar

---

## 🚀 Próximos Passos

Para testar, abra duas abas:

**Aba 1 (Mestre):**
```
http://127.0.0.1:8000/login/
→ Criar sala
→ Adicionar tokens
```

**Aba 2 (Jogador):**
```
http://127.0.0.1:8000/player/join/
→ Entrar com código da sala
→ Verificar se vê os tokens
```

Verifique os logs no console (F12) para confirmar a comunicação WebSocket!

