# 🎬 Sistema de Cenas por Sala

## 📋 Visão Geral

Cada **sala** agora possui suas **próprias cenas** salvas no **banco de dados**, não mais no LocalStorage do navegador. Isso significa:

✅ **Cenas persistentes** - Ficam salvas no servidor
✅ **Compartilhadas** - Mestre e jogadores veem as mesmas cenas
✅ **Por sala** - Cada sala tem seu próprio conjunto de cenas
✅ **Multiplayer real** - Troca de cena sincroniza para todos

---

## 🏗️ Estrutura do Banco de Dados

### Model `Scene`

```python
class Scene(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='scenes')
    name = models.CharField(max_length=100)
    scene_data = models.JSONField()  # Estado completo da cena
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)  # Cena ativa no momento
    order = models.IntegerField(default=0)  # Ordem das cenas
```

**Campos:**
- `room` - Sala à qual a cena pertence
- `name` - Nome da cena (único por sala)
- `scene_data` - JSON com estado completo (tokens, background, grid settings, etc.)
- `is_active` - Indica qual cena está ativa (apenas uma por sala)
- `order` - Ordem de exibição das cenas

---

## 🔌 API REST de Cenas

### Endpoints Disponíveis

#### 1. **Listar Cenas**
```
GET /api/room/<room_code>/scenes/
```
Retorna todas as cenas de uma sala.

**Resposta:**
```json
{
  "scenes": [
    {
      "id": 1,
      "name": "Taverna",
      "scene_data": {...},
      "is_active": true,
      "order": 0,
      "created_at": "2025-10-28T21:00:00Z",
      "updated_at": "2025-10-28T21:30:00Z"
    }
  ]
}
```

#### 2. **Criar Cena**
```
POST /api/room/<room_code>/scenes/create/
Content-Type: application/json

{
  "name": "Nova Cena",
  "scene_data": {...}
}
```

#### 3. **Atualizar Cena**
```
PUT /api/room/<room_code>/scenes/<scene_id>/
Content-Type: application/json

{
  "name": "Nome Atualizado",
  "scene_data": {...}
}
```

#### 4. **Deletar Cena**
```
DELETE /api/room/<room_code>/scenes/<scene_id>/delete/
```

#### 5. **Trocar Cena Ativa**
```
POST /api/room/<room_code>/scenes/<scene_id>/switch/
```

Marca a cena como ativa e desativa todas as outras da mesma sala.

---

## 🎮 Como Funciona

### Para o Mestre

1. **Criar Cena**
   - Digite o nome da cena
   - Clique em "Criar Cena"
   - A cena é salva no banco e aparece na lista

2. **Editar Cena**
   - Qualquer alteração (adicionar token, mover, mudar background) é **auto-salva** no banco
   - A cada 500ms de inatividade, o estado é enviado para o servidor

3. **Trocar de Cena**
   - Clique na cena desejada na lista
   - A cena atual é salva
   - A nova cena é carregada do banco
   - **Jogadores recebem a atualização via WebSocket** e veem a mesma cena

4. **Deletar Cena**
   - Clique no ícone 🗑️ ao lado da cena
   - Confirme a exclusão
   - Se for a cena ativa, troca automaticamente para outra

### Para os Jogadores

- **Visualização automática** - Recebem todas as atualizações em tempo real
- **Sem controles** - Não podem criar, editar ou deletar cenas
- **Sincronização** - Sempre veem o que o mestre está mostrando

---

## 🔄 Fluxo de Sincronização

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Mestre    │         │   Backend    │         │  Jogadores  │
│  (master)   │         │   Django     │         │  (players)  │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │                        │
      │  1. Edita cena         │                        │
      │────────────────────────>                        │
      │                        │                        │
      │  2. Auto-save (PUT)    │                        │
      │────────────────────────>                        │
      │                        │                        │
      │                        │ 3. Salva no DB         │
      │                        │────────┐               │
      │                        │        │               │
      │                        │<───────┘               │
      │                        │                        │
      │  4. Envia via WebSocket│                        │
      │────────────────────────>────────────────────────>
      │                        │                        │
      │                        │  5. Jogador atualiza   │
      │                        │        canvas          │
      │                        │                        │
```

---

## 🛠️ Implementação no Frontend

### Funções Principais

```javascript
// Carregar cenas do banco
async function loadScenesFromDatabase() {
    const response = await fetch(`${API_BASE}/scenes/`);
    const data = await response.json();
    scenes = data.scenes;
    // Carrega cena ativa
}

// Criar cena
async function createScene(name) {
    const response = await fetch(`${API_BASE}/scenes/create/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            name: name,
            scene_data: captureCurrentState()
        })
    });
}

// Salvar cena (auto-save)
async function saveCurrentScene() {
    if (!currentScene || !currentScene.id) return;
    
    await fetch(`${API_BASE}/scenes/${currentScene.id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            scene_data: captureCurrentState()
        })
    });
}

// Trocar cena
async function switchToScene(scene, saveCurrentFirst = true) {
    if (saveCurrentFirst && currentScene) {
        await saveCurrentScene();
    }
    
    const response = await fetch(`${API_BASE}/scenes/${scene.id}/switch/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    
    const data = await response.json();
    currentScene = data;
    loadState(currentScene.scene_data);
}
```

---

## 📦 O que é Salvo em `scene_data`

```json
{
  "tokens": [
    {
      "id": 1,
      "x": 100,
      "y": 200,
      "size": 50,
      "name": "Guerreiro",
      "imageSrc": "data:image/png;base64,...",
      "visible": true
    }
  ],
  "backgroundImage": "data:image/png;base64,...",
  "grid": {
    "gridSize": 50,
    "backgroundColor": "#2a2a2a",
    "gridColor": "#444444",
    "lineWidth": 1
  },
  "view": {
    "offsetX": 0,
    "offsetY": 0,
    "scale": 1
  }
}
```

---

## 🚀 Vantagens do Sistema

### Antes (LocalStorage)
❌ Cenas ficavam apenas no navegador do mestre
❌ Perdia tudo ao limpar cache
❌ Não sincronizava com jogadores
❌ Cada pessoa via cenas diferentes

### Agora (Banco de Dados)
✅ Cenas ficam no servidor (persistentes)
✅ Nunca perdem dados
✅ Sincronizam automaticamente
✅ Todos veem as mesmas cenas
✅ Cada sala tem suas próprias cenas
✅ Mestre pode gerenciar pelo admin Django

---

## 🎯 Casos de Uso

### 1. Preparação de Sessão
O mestre pode criar várias cenas antes da sessão:
- "Taverna do Dragão Vermelho"
- "Floresta Sombria"
- "Calabouço do Necromante"
- "Boss Final"

### 2. Durante a Sessão
O mestre troca entre as cenas conforme a narrativa avança, e os jogadores veem automaticamente.

### 3. Múltiplas Salas
Cada mesa de RPG (sala) tem suas próprias cenas independentes:
- **Sala "Campanha A"** → Cenas da Campanha A
- **Sala "Campanha B"** → Cenas da Campanha B

### 4. Persistência
Se o mestre fechar o navegador e voltar depois, todas as cenas estarão lá, exatamente como deixou.

---

## 🔐 Segurança

- **Autenticação** - Apenas o mestre da sala pode criar/editar/deletar cenas
- **CSRF Protection** - Todas as requisições POST/PUT/DELETE usam CSRF token
- **Isolamento** - Uma sala não pode acessar cenas de outra sala
- **Jogadores** - Apenas visualizam, não podem modificar

---

## 📊 Admin Django

Agora você pode gerenciar cenas pelo admin:

```
http://127.0.0.1:8000/admin/grid/scene/
```

**Recursos:**
- Ver todas as cenas de todas as salas
- Filtrar por sala, ativa, data
- Buscar por nome ou sala
- Editar scene_data manualmente (avançado)
- Deletar cenas

---

## 🎉 Resumo

Agora cada **sala tem suas próprias cenas** salvas no **banco de dados**:

1. ✅ Cenas persistem no servidor
2. ✅ Compartilhadas entre mestre e jogadores
3. ✅ Auto-save a cada alteração
4. ✅ Sincronização em tempo real via WebSocket
5. ✅ Isolamento entre salas
6. ✅ Gerenciamento pelo Django Admin

**Não é mais necessário usar LocalStorage!** 🎊

