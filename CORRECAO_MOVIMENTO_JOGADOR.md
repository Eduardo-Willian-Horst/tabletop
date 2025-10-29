# 🔧 Correção: Jogador não Conseguia Mover Token

## 🐛 Problema

Os jogadores não conseguiam mover seus tokens atribuídos pelo mestre.

---

## 🔍 Causas Identificadas

### 1. Conflito de Event Listeners

**Problema:**
Havia **dois** `addEventListener('mousedown')` e **dois** `addEventListener('mouseup')` no `player_room.html`, causando conflito.

**Código Problemático:**
```javascript
// Primeiro listener (linha ~1271)
canvas.addEventListener('mousedown', (e) => {
    // Lógica de arraste normal
});

// Segundo listener (linha ~1680) - CONFLITANTE!
canvas.addEventListener('mousedown', function(e) {
    if (token && !canPlayerMoveToken(token)) {
        e.stopPropagation();
        return false;
    }
    return; // Não fazia nada quando podia mover
}, true);
```

**Resultado:**
- O segundo listener bloqueava tokens alheios ✅
- Mas quando era token do jogador, apenas retornava sem fazer nada ❌
- O primeiro listener não executava o arraste corretamente ❌

### 2. Campo `controlledBy` Não Carregado

**Problema:**
A função `loadState()` no `player_room.html` não estava carregando o campo `controlledBy`.

**Código Problemático:**
```javascript
const token = {
    id: tokenData.id,
    name: tokenData.name,
    image: img,
    size: tokenData.size,
    gridX: tokenData.gridX,
    gridY: tokenData.gridY,
    visible: tokenData.visible !== undefined ? tokenData.visible : true
    // ❌ controlledBy estava faltando!
};
```

**Resultado:**
- `token.controlledBy` era sempre `undefined`
- `canPlayerMoveToken(token)` sempre retornava `false`
- Jogador não podia mover nenhum token

### 3. Indicador Visual Ausente

**Problema:**
O badge com iniciais do jogador não era renderizado no `player_room.html`.

**Resultado:**
- Jogador não sabia visualmente qual token era dele

---

## ✅ Soluções Implementadas

### 1. Corrigir Event Listeners

**Solução:**
- Removido o segundo `addEventListener('mouseup')`
- Substituído `canvas.onmouseup` diretamente
- Mantido um único `addEventListener('mousedown')` em capture phase

**Novo Código:**
```javascript
// Interceptar mousedown ANTES do listener original
canvas.addEventListener('mousedown', function(e) {
    const token = getTokenAtPosition(e.clientX, e.clientY);
    if (token && !canPlayerMoveToken(token)) {
        // Bloqueia token alheio
        console.log('⛔ Este token não é seu');
        e.stopPropagation();
        e.preventDefault();
        return false;
    }
    // Permite token próprio ou pan
    if (token && canPlayerMoveToken(token)) {
        console.log('✅ Você pode mover este token');
    }
}, true); // Capture phase = executa ANTES

// Substituir onmouseup para enviar via WebSocket
canvas.onmouseup = function(e) {
    if (draggingToken) {
        if (canPlayerMoveToken(draggingToken)) {
            sendTokenMove(draggingToken.id, draggingToken.gridX, draggingToken.gridY);
            console.log('📤 Token movido:', draggingToken.name);
        }
        canvas.style.cursor = 'grab';
        draggingToken = null;
    } else {
        isDragging = false;
    }
};
```

**Benefícios:**
- ✅ Bloqueia tokens alheios no mousedown
- ✅ Permite arraste de tokens próprios
- ✅ Envia movimentação via WebSocket no mouseup
- ✅ Sem conflitos entre listeners

### 2. Adicionar `controlledBy` no loadState

**Solução:**
Adicionar o campo `controlledBy` ao carregar tokens.

**Novo Código:**
```javascript
const token = {
    id: tokenData.id,
    name: tokenData.name,
    image: img,
    imageSrc: tokenData.imageSrc,
    size: tokenData.size,
    gridX: tokenData.gridX,
    gridY: tokenData.gridY,
    visible: tokenData.visible !== undefined ? tokenData.visible : true,
    controlledBy: tokenData.controlledBy || null // ✅ ADICIONADO
};
```

**Benefícios:**
- ✅ `canPlayerMoveToken()` funciona corretamente
- ✅ Jogador pode mover tokens atribuídos

### 3. Adicionar Indicador Visual (Badge)

**Solução:**
Renderizar badge com iniciais no canvas.

**Novo Código:**
```javascript
// Indicador de controle do jogador
if (token.controlledBy) {
    ctx.save();
    const badgeX = tokenX + tokenRadius * 2 - 10;
    const badgeY = tokenY - 5;
    const badgeRadius = 15;
    
    // Círculo do badge
    ctx.beginPath();
    ctx.arc(badgeX, badgeY, badgeRadius, 0, Math.PI * 2);
    
    // Verde se é seu token, azul se é de outro
    ctx.fillStyle = token.controlledBy === playerName ? '#4CAF50' : '#2196F3';
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Iniciais
    ctx.font = `bold ${10}px Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#fff';
    const initials = token.controlledBy.substring(0, 2).toUpperCase();
    ctx.fillText(initials, badgeX, badgeY);
    
    ctx.restore();
}
```

**Benefícios:**
- ✅ Jogador vê **VERDE** no seu token
- ✅ Vê **AZUL** nos tokens de outros
- ✅ Identificação visual clara

---

## 🔄 Fluxo Corrigido

### Antes (Quebrado):

```
Jogador clica no token
    ↓
Segundo mousedown intercepta
    ↓
canPlayerMoveToken(token) → FALSE (controlledBy undefined)
    ↓
return; (não faz nada)
    ↓
Primeiro mousedown não executa
    ↓
❌ Token não se move
```

### Depois (Funcionando):

```
Jogador clica no seu token
    ↓
mousedown em capture phase
    ↓
canPlayerMoveToken(token) → TRUE (controlledBy carregado)
    ↓
console.log('✅ Você pode mover este token')
    ↓
Permite evento continuar
    ↓
Primeiro mousedown executa (arraste normal)
    ↓
Jogador arrasta token
    ↓
mouseup dispara
    ↓
sendTokenMove() via WebSocket
    ↓
Consumer valida e atualiza
    ↓
Broadcast token_moved
    ↓
✅ Todos veem o movimento
```

---

## 🧪 Como Testar

### Teste 1: Verificar controlledBy

1. Mestre atribui token "Guerreiro" para "João"
2. Na aba do João, abra Console (F12)
3. Digite: `tokens[0].controlledBy`
4. **Esperado:** `"João"`

### Teste 2: Mover Token Próprio

1. Na aba do João
2. Veja badge **VERDE** com "JO" no Guerreiro
3. Arraste o Guerreiro
4. Console: `✅ Você pode mover este token`
5. Console: `📤 Token movido: Guerreiro`
6. **Esperado:** Token se move

### Teste 3: Bloquear Token Alheio

1. Mestre atribui "Maga" para "Maria"
2. Na aba do João
3. Veja badge **AZUL** com "MA" na Maga
4. Tente arrastar a Maga
5. Console: `⛔ Este token não é seu`
6. **Esperado:** Token não se move

### Teste 4: Sincronização

1. João move Guerreiro
2. Maria vê movimento em tempo real
3. Mestre vê movimento em tempo real
4. **Esperado:** Todos veem

---

## 📁 Arquivos Modificados

### `grid/templates/grid/player_room.html`

**Linhas modificadas:**

1. **~1060-1069:** Adicionado `controlledBy` no loadState
```javascript
controlledBy: tokenData.controlledBy || null
```

2. **~836-863:** Adicionado indicador visual (badge)
```javascript
// Indicador de controle do jogador
if (token.controlledBy) { ... }
```

3. **~1660-1698:** Corrigido event listeners
```javascript
// Mousedown em capture phase
canvas.addEventListener('mousedown', ..., true);

// Mouseup substituído
canvas.onmouseup = function(e) { ... };
```

---

## 🎨 Indicadores Visuais

### Token do Próprio Jogador
```
    🟢 JO    ← Badge VERDE
  ┌────────┐
  │[IMAGEN]│
  └────────┘
  Guerreiro
```

### Token de Outro Jogador
```
    🔵 MA    ← Badge AZUL
  ┌────────┐
  │[IMAGEN]│
  └────────┘
    Maga
```

### Token Sem Atribuição
```
  ┌────────┐
  │[IMAGEN]│
  └────────┘
   Ladino
```

---

## 📊 Console Logs

### Movimentação Bem-Sucedida
```
✅ Você pode mover este token
📤 Token movido: Guerreiro
📤 Movimentação enviada: {tokenId: 1, gridX: 5, gridY: 3}
```

### Tentativa Bloqueada
```
⛔ Este token não é seu
```

### Recebendo Movimentação
```
📨 Mensagem WebSocket recebida: {type: "token_moved", ...}
🎭 Token movido: {token_id: 1, gridX: 5, gridY: 3, moved_by: "João"}
```

---

## ✅ Resultado Final

Agora os jogadores:

1. ✅ **Veem** visualmente quais tokens são deles (badge verde)
2. ✅ **Podem mover** apenas seus tokens atribuídos
3. ✅ **São bloqueados** ao tentar mover tokens alheios
4. ✅ **Sincronizam** movimentos em tempo real via WebSocket
5. ✅ **Recebem feedback** no console sobre permissões

---

## 🚀 Status

**PROBLEMA RESOLVIDO!** 🎉

Os jogadores agora conseguem mover seus tokens corretamente!

