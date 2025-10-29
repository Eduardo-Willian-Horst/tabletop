# 🎮 Sistema de Controle de Tokens por Jogador

## 📋 Visão Geral

Sistema completo que permite ao **mestre atribuir tokens específicos para cada jogador**, e os **jogadores podem mover apenas os tokens que lhes foram atribuídos**.

---

## ✨ Funcionalidades Implementadas

### Para o Mestre 🎭

1. **Painel de Jogadores Online**
   - Lista todos os jogadores conectados
   - Indicador visual de status online/offline
   - Contador de jogadores conectados

2. **Atribuição de Tokens**
   - Dropdown para cada jogador com lista de tokens disponíveis
   - Atribuir/desatribuir tokens facilmente
   - Tokens já atribuídos aparecem como "(em uso)" para outros jogadores
   - Auto-save ao atribuir tokens

3. **Indicadores Visuais**
   - Badge azul nos tokens mostrando iniciais do jogador que controla
   - Borda verde no token selecionado
   - Atualização em tempo real de quem controla cada token

### Para os Jogadores 🎮

1. **Controle de Tokens Atribuídos**
   - Pode mover apenas tokens atribuídos pelo mestre
   - Indicador visual (badge) mostrando que o token é controlável
   - Feedback no console sobre permissões

2. **Movimentação em Tempo Real**
   - Arrasta tokens normalmente
   - Sincronização automática via WebSocket
   - Todos veem a movimentação em tempo real

3. **Restrições de Segurança**
   - Não pode mover tokens de outros jogadores
   - Não pode criar/deletar tokens
   - Não pode criar/deletar cenas
   - Apenas visualização e controle do próprio token

---

## 🏗️ Arquitetura

### Frontend (master_room.html)

**Painel de Jogadores:**
```html
<div class="players-panel">
    <h3>
        👥 Jogadores
        <span id="playerCount">(0)</span>
    </h3>
    <div id="playersList">
        <!-- Jogadores listados aqui -->
    </div>
</div>
```

**Estrutura de Token com controlledBy:**
```javascript
{
    id: 1,
    name: "Guerreiro",
    image: Image,
    imageSrc: "data:image/...",
    size: 1,
    gridX: 0,
    gridY: 0,
    visible: true,
    controlledBy: "JogadorX" // null = apenas mestre
}
```

**Funções Principais:**
- `updatePlayersList(players)` - Atualiza lista de jogadores
- `assignTokenToPlayer(tokenId, playerName)` - Atribui token
- `updatePlayerTokenSelects()` - Atualiza dropdowns
- `canPlayerMoveToken(token)` - Verifica permissão

### Backend (consumers.py)

**Nova Ação: `move_token`**
```python
elif action == 'move_token':
    token_id = data.get('token_id')
    grid_x = data.get('gridX')
    grid_y = data.get('gridY')
    player_name = self.scope['session'].get('player_name')
    
    # Verificar permissão
    can_move = await self.can_player_move_token(token_id, player_name)
    
    if can_move:
        # Atualizar no banco
        await self.update_token_position(token_id, grid_x, grid_y)
        
        # Broadcast para todos
        await self.channel_layer.group_send(...)
```

**Funções de Verificação:**
- `can_player_move_token(token_id, player_name)` - Verifica se jogador controla token
- `update_token_position(token_id, grid_x, grid_y)` - Atualiza posição no banco

---

## 🎨 Interface do Usuário

### Painel de Jogadores (Mestre)

```
┌─────────────────────────────────────┐
│  👥 Jogadores (2)                   │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │ 🟢 João                PLAYER│   │
│  │ Token controlado:            │   │
│  │ ┌──────────────────────┐    │   │
│  │ │ Guerreiro            │    │   │
│  │ └──────────────────────┘    │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 🟢 Maria               PLAYER│   │
│  │ Token controlado:            │   │
│  │ ┌──────────────────────┐    │   │
│  │ │ Maga (em uso)        │    │   │
│  │ └──────────────────────┘    │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### Token com Indicador

```
        ╭─────────╮
        │   JO    │ ← Badge azul com iniciais
    ╭───┴─────────┴───╮
    │                 │
    │    [IMAGEM]     │ ← Token circular
    │                 │
    ╰─────────────────╯
       Guerreiro        ← Nome do token
```

---

## 🔄 Fluxo de Dados

### 1. Mestre Atribui Token

```
Mestre seleciona token no dropdown
    ↓
assignTokenToPlayer(tokenId, playerName)
    ↓
token.controlledBy = playerName
    ↓
updatePlayerTokenSelects()
    ↓
autoSaveCurrentScene()
    ↓
WebSocket → scene_update
    ↓
Jogador recebe atualização
    ↓
loadState() atualiza tokens
```

### 2. Jogador Move Token

```
Jogador arrasta token
    ↓
mouseup → sendTokenMove()
    ↓
WebSocket → move_token action
    ↓
Consumer verifica permissão
    ↓
can_player_move_token()?
    ↓ SIM
update_token_position()
    ↓
Broadcast token_moved
    ↓
Todos recebem (mestre + jogadores)
    ↓
Atualizam posição localmente
    ↓
Mestre faz auto-save
```

### 3. WebSocket Messages

**Tipos de Mensagens:**

1. **room_state** (inicial)
```json
{
  "type": "room_state",
  "data": {
    "scene_data": {...},
    "members": [...]
  }
}
```

2. **token_moved** (movimentação)
```json
{
  "type": "token_moved",
  "token_id": 1,
  "gridX": 5,
  "gridY": 3,
  "moved_by": "João"
}
```

3. **scene_update** (mestre atualiza)
```json
{
  "type": "scene_update",
  "scene_data": {
    "tokens": [...],
    ...
  }
}
```

---

## 🔒 Segurança

### Verificações no Backend

1. **Autenticação:**
   - Mestre: Django User autenticado
   - Jogador: Nome na sessão

2. **Autorização:**
   - `can_player_move_token()` verifica ownership no banco
   - Apenas mestre pode fazer `update_scene`
   - Jogadores só movem tokens com `controlledBy === playerName`

3. **Isolamento:**
   - Cada sala tem seus próprios tokens
   - Verificações por room_code
   - Cenas isoladas por sala

### Validações no Frontend

```javascript
// Jogador
function canPlayerMoveToken(token) {
    return token.controlledBy === playerName;
}

// Se tentar mover token de outro
if (!canPlayerMoveToken(token)) {
    console.log('⛔ Este token não é seu');
    return false;
}
```

---

## 📦 Estrutura de Dados

### Token no Banco (scene_data.tokens)

```json
{
  "id": 1,
  "name": "Guerreiro",
  "imageSrc": "data:image/png;base64,...",
  "size": 1,
  "gridX": 5,
  "gridY": 3,
  "visible": true,
  "controlledBy": "João"
}
```

### Jogador no Banco (RoomMember)

```python
{
    "room": Room instance,
    "player_name": "João",
    "role": "player",
    "is_online": True,
    "user": None  # ou User instance para mestre
}
```

---

## 🎯 Casos de Uso

### Caso 1: Sessão de RPG

**Cenário:**
- Mestre cria sala "Calabouço do Dragão"
- 4 jogadores entram
- Mestre atribui 1 token para cada jogador

**Resultado:**
- Cada jogador vê todos os tokens
- Cada jogador pode mover apenas o seu
- Mestre pode mover qualquer token
- Todos veem movimentações em tempo real

### Caso 2: Jogador Tenta Mover Token Alheio

**Cenário:**
- João tenta arrastar token da Maria

**Resultado:**
```
Console: ⛔ Este token não é seu
Token não se move
Sem mensagem enviada ao servidor
```

### Caso 3: Mestre Reatribui Token

**Cenário:**
- Token estava com João
- Mestre atribui para Maria

**Resultado:**
```
João: Perde controle do token
Maria: Ganha controle do token
Todos veem atualização instantânea
Badge muda de "JO" para "MA"
```

---

## 🎨 CSS Classes

```css
.players-panel         /* Painel principal */
.player-item           /* Item de jogador */
.player-item.online    /* Jogador online */
.player-item.offline   /* Jogador offline */
.player-status         /* Indicador de status */
.player-status.online  /* Status online (verde) */
.player-name           /* Nome do jogador */
.player-role           /* Badge do role */
.player-role.master    /* Badge laranja (mestre) */
.player-token-control  /* Controle de token */
.controlled-token-badge /* Badge no token */
```

---

## 🧪 Como Testar

### Teste 1: Atribuição de Token

1. Faça login como mestre
2. Crie uma sala
3. Crie 2 tokens: "Guerreiro", "Maga"
4. Abra em aba anônima como jogador "João"
5. No painel de jogadores, atribua "Guerreiro" para João
6. Verifique badge azul "JO" no token

### Teste 2: Movimentação pelo Jogador

1. Na aba do jogador "João"
2. Arraste o token "Guerreiro"
3. Verifique console: `✅ Você pode mover este token`
4. Token deve se mover
5. Na aba do mestre, veja o token se movendo

### Teste 3: Restrição de Movimento

1. Na aba do jogador "João"
2. Tente arrastar "Maga" (não atribuído)
3. Verifique console: `⛔ Este token não é seu`
4. Token não deve se mover

### Teste 4: Sincronização em Tempo Real

1. Abra 3 abas:
   - Mestre
   - Jogador "João"
   - Jogador "Maria"
2. Mestre atribui tokens
3. João move seu token
4. Todos veem movimento instantâneo

---

## 📁 Arquivos Modificados

1. ✅ `grid/templates/grid/master_room.html`
   - Painel de jogadores
   - Sistema de atribuição
   - Indicadores visuais
   - WebSocket handlers

2. ✅ `grid/templates/grid/player_room.html`
   - Controle de movimentação
   - Verificação de permissões
   - WebSocket para enviar moves

3. ✅ `grid/consumers.py`
   - Ação `move_token`
   - `can_player_move_token()`
   - `update_token_position()`
   - Handler `token_moved`

---

## 🚀 Tecnologias Utilizadas

- **Django Channels** - WebSocket real-time
- **JavaScript ES6+** - Frontend interativo
- **Canvas API** - Renderização de tokens
- **CSS3** - Interface responsiva
- **JSON** - Serialização de dados

---

## 📊 Performance

- **WebSocket** mantém conexão persistente
- **Broadcast eficiente** para room groups
- **Verificação no backend** previne trapaças
- **Debounce** no auto-save do mestre (500ms)
- **Renderização otimizada** apenas quando necessário

---

## 🎉 Resumo

Sistema completo de controle de tokens por jogador implementado:

✅ Mestre vê lista de jogadores online
✅ Mestre atribui tokens aos jogadores
✅ Indicadores visuais de ownership
✅ Jogadores movem apenas seus tokens
✅ Sincronização em tempo real via WebSocket
✅ Segurança no backend
✅ Interface intuitiva e responsiva
✅ Persistência no banco de dados

**Pronto para jogar RPG online!** 🎲🎭

