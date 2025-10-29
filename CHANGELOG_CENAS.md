# 📝 Changelog - Sistema de Cenas por Sala

## Data: 29 de Outubro de 2025

---

## 🎯 Objetivo

Transformar o sistema de cenas de **LocalStorage (navegador)** para **Banco de Dados (servidor)**, permitindo que **cada sala tenha suas próprias cenas** persistentes e compartilhadas.

---

## ✅ Mudanças Implementadas

### 1. 🗄️ Banco de Dados

#### Novo Model: `Scene`

**Arquivo:** `grid/models.py`

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

**Características:**
- ✅ Cada cena pertence a uma sala (`room`)
- ✅ `scene_data` armazena todo o estado (tokens, background, settings)
- ✅ `is_active` indica qual cena está sendo exibida (apenas 1 por sala)
- ✅ `unique_together = ['room', 'name']` - nomes únicos por sala
- ✅ Auto-desativa outras cenas ao marcar uma como ativa

**Migração:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 2. 🌐 API REST de Cenas

**Arquivo:** `grid/views.py`

#### Endpoints Criados:

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/room/<code>/scenes/` | Lista todas as cenas da sala |
| `POST` | `/api/room/<code>/scenes/create/` | Cria nova cena |
| `PUT` | `/api/room/<code>/scenes/<id>/` | Atualiza cena existente |
| `DELETE` | `/api/room/<code>/scenes/<id>/delete/` | Deleta cena |
| `POST` | `/api/room/<code>/scenes/<id>/switch/` | Troca para outra cena |

**Segurança:**
- ✅ `@login_required` - Apenas mestres autenticados
- ✅ Verificação de propriedade da sala
- ✅ CSRF token em todas as operações POST/PUT/DELETE

---

### 3. 🎨 Frontend - master_room.html

**Arquivo:** `grid/templates/grid/master_room.html`

#### Mudanças Principais:

**Antes (LocalStorage):**
```javascript
function saveScenesToStorage() {
    localStorage.setItem('rpg_scenes', JSON.stringify(scenesData));
}

function loadScenesFromStorage() {
    const scenesData = localStorage.getItem('rpg_scenes');
    scenes = JSON.parse(scenesData);
}
```

**Depois (Banco de Dados):**
```javascript
async function loadScenesFromDatabase() {
    const response = await fetch(`${API_BASE}/scenes/`);
    const data = await response.json();
    scenes = data.scenes;
}

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

async function saveCurrentScene() {
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
```

**Funcionalidades:**
- ✅ Auto-save via API (debounce de 500ms)
- ✅ Criação assíncrona de cenas
- ✅ Troca de cenas com sincronização no banco
- ✅ Envio via WebSocket para jogadores após salvar

---

### 4. 👁️ Frontend - player_room.html

**Arquivo:** `grid/templates/grid/player_room.html`

**Mudanças:**
```javascript
// Desabilitar sistema local de cenas (usar apenas do servidor)
autoSaveCurrentScene = function() {}; // Desabilitar auto-save

// Desabilitar criação/edição de cenas
createScene = function() {};
deleteScene = function() {};
saveCurrentScene = function() {};
loadScenesFromStorage = function() {};
loadScenesFromDatabase = function() {};
```

**Comportamento:**
- ❌ Jogadores NÃO podem criar/editar/deletar cenas
- ✅ Jogadores recebem atualizações via WebSocket
- ✅ Visualização sincronizada em tempo real

---

### 5. 🔗 URLs

**Arquivo:** `infinite_grid/urls.py`

```python
# API de Cenas
path("api/room/<str:room_code>/scenes/", views.list_scenes_api, name="list_scenes"),
path("api/room/<str:room_code>/scenes/create/", views.create_scene_api, name="create_scene"),
path("api/room/<str:room_code>/scenes/<int:scene_id>/", views.update_scene_api, name="update_scene"),
path("api/room/<str:room_code>/scenes/<int:scene_id>/delete/", views.delete_scene_api, name="delete_scene"),
path("api/room/<str:room_code>/scenes/<int:scene_id>/switch/", views.switch_scene_api, name="switch_scene"),
```

---

### 6. 🛠️ Admin Django

**Arquivo:** `grid/admin.py`

```python
@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ['name', 'room', 'is_active', 'order', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'room']
    search_fields = ['name', 'room__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['room', 'order', 'created_at']
```

**Acesso:**
```
http://127.0.0.1:8000/admin/grid/scene/
```

**Funcionalidades:**
- ✅ Visualizar todas as cenas de todas as salas
- ✅ Filtrar por sala, ativa, data
- ✅ Buscar por nome
- ✅ Editar manualmente (avançado)
- ✅ Deletar cenas

---

## 🔄 Fluxo de Dados

### Criação de Cena

```
Mestre digita nome → createScene() → POST /api/.../scenes/create/
    ↓
Backend salva no DB → retorna cena criada
    ↓
Frontend adiciona à lista → switchToScene() → atualiza canvas
```

### Auto-Save

```
Mestre move token → autoSaveCurrentScene() (debounce 500ms)
    ↓
saveCurrentScene() → PUT /api/.../scenes/<id>/
    ↓
Backend atualiza scene_data no DB
    ↓
Envia via WebSocket para jogadores
    ↓
Jogadores atualizam canvas em tempo real
```

### Troca de Cena

```
Mestre clica em cena → switchToScene()
    ↓
Salva cena atual → POST /api/.../scenes/<id>/switch/
    ↓
Backend marca nova cena como ativa
    ↓
Frontend carrega scene_data da nova cena → loadState()
    ↓
WebSocket notifica jogadores → jogadores carregam mesma cena
```

---

## 📊 Comparação

### Antes (LocalStorage)

❌ Cenas salvas apenas no navegador do mestre
❌ Perdia tudo ao limpar cache/cookies
❌ Não sincronizava com jogadores
❌ Cada pessoa via cenas diferentes
❌ Sem backup
❌ Limitado pelo tamanho do LocalStorage (~5-10MB)

### Depois (Banco de Dados)

✅ Cenas salvas no servidor (PostgreSQL/SQLite)
✅ Persistência permanente
✅ Sincronização automática
✅ Todos veem as mesmas cenas
✅ Cada sala tem suas próprias cenas
✅ Backup automático do banco
✅ Sem limite prático de armazenamento
✅ Gerenciamento pelo admin Django
✅ API REST para integrações futuras

---

## 📁 Arquivos Modificados

1. ✅ `grid/models.py` - Adicionado model `Scene`
2. ✅ `grid/views.py` - Adicionadas views da API REST
3. ✅ `grid/admin.py` - Registrado `Scene` no admin
4. ✅ `infinite_grid/urls.py` - Adicionadas rotas da API
5. ✅ `grid/templates/grid/master_room.html` - JavaScript atualizado
6. ✅ `grid/templates/grid/player_room.html` - Desabilitado controles de cena
7. ✅ `grid/migrations/0002_scene.py` - Migração criada
8. ✅ `README.md` - Documentação atualizada
9. ✅ `CENAS_POR_SALA.md` - Nova documentação criada
10. ✅ `CHANGELOG_CENAS.md` - Este arquivo

---

## 🧪 Testes Realizados

✅ Criar cena via frontend
✅ Auto-save funciona (500ms debounce)
✅ Trocar entre cenas
✅ Deletar cena
✅ Sincronização via WebSocket (mestre → jogadores)
✅ Isolamento entre salas
✅ Admin Django funcional
✅ API REST endpoints

---

## 🚀 Como Usar

### 1. Executar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Iniciar Servidor

```bash
python manage.py runserver
```

### 3. Testar

1. Faça login como mestre
2. Crie uma sala
3. Entre na sala
4. Crie uma cena
5. Adicione tokens/background
6. Crie outra cena
7. Troque entre elas
8. Abra em outra aba como jogador e veja sincronização

### 4. Verificar no Admin

```
http://127.0.0.1:8000/admin/grid/scene/
```

---

## 📚 Documentação

- **README.md** - Documentação principal do projeto
- **CENAS_POR_SALA.md** - Documentação detalhada do sistema de cenas
- **MULTIPLAYER_SETUP.md** - Configuração do multiplayer
- **COMO_USAR.md** - Guia de uso completo

---

## 🎉 Resultado Final

Agora cada sala tem suas próprias cenas salvas permanentemente no banco de dados, com sincronização automática em tempo real para todos os jogadores! 🚀

**Benefícios:**
- 🎯 Persistência confiável
- 🔄 Sincronização automática
- 🔒 Isolamento entre salas
- 🛠️ Gerenciamento facilitado
- 📊 Escalabilidade
- 🌐 Pronto para produção

---

## ✅ Status

**100% Completo e Funcional!** 🎊

