# Grid Infinita - Projeto Django

Um projeto Django com uma grid infinita interativa e otimizada.

## 🚀 Características

- **Grid Infinita**: Renderiza apenas o que está visível na tela para máxima performance
- **Zoom**: Use a roda do mouse para dar zoom in/out (10% até 1000%)
- **Pan**: Clique e arraste para navegar pela grid
- **Imagem de Fundo**: Carregue mapas de RPG ou qualquer imagem como fundo
- **Sistema de Cenas por Sala**: 
  - **Cenas salvas no banco de dados** (não mais LocalStorage!)
  - Cada sala tem suas próprias cenas independentes
  - Auto-save automático a cada alteração
  - Troque entre cenas instantaneamente
  - Cada cena salva: tokens, mapa, posições, zoom, configurações
  - Persistência permanente no servidor
  - Imagens salvas em base64 dentro do JSON
  - Sincronização automática via WebSocket (mestre ↔ jogadores)
- **Sistema de Tokens**: 
  - Crie tokens circulares com imagem e nome
  - Arraste e solte tokens pelo mapa
  - Snap automático para a grid
  - Tokens de múltiplos tamanhos (1-10 células)
  - Seleção visual de tokens
  - Visualização da posição na grid
  - Toggle de visibilidade (ocultar/mostrar tokens)
  - Mostrar/ocultar todos os tokens de uma vez
- **Personalizável**: 
  - Carregar imagem de fundo (mapas de RPG, plantas, etc.)
  - Opacidade da imagem (0% - 100%)
  - Escala da imagem (0.1x - 3.0x)
  - Cor do background
  - Cor da grid
  - Opacidade da grid (0% - 100%)
  - Tamanho dos quadrados da grid (10px - 200px)
  - Espessura das linhas (0.5px - 5px)
- **Responsivo**: Funciona em desktop e dispositivos móveis
- **Performance**: Usa Canvas API e renderiza apenas linhas visíveis

## 📦 Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute as migrações:
```bash
python manage.py migrate
```

3. Crie um superusuário (opcional, para acessar o admin):
```bash
python manage.py createsuperuser
```

4. Inicie o servidor:
```bash
python manage.py runserver
```

5. Acesse no navegador:

**Login de Mestre:**
```
http://127.0.0.1:8000/login/
```

**Admin Django (gerenciar salas e cenas):**
```
http://127.0.0.1:8000/admin/
```

## 🎮 Controles

### Cenas
- **🎬 Painel de Cenas** (canto inferior esquerdo):
  - ➕ Criar nova cena/encontro
  - 📋 Lista de todas as cenas
  - ✅ Cena ativa destacada com borda verde
  - 🔄 Clique em uma cena para trocar instantaneamente
  - 🗑️ Deletar cenas não utilizadas
  - 💾 Auto-save automático (aparece indicador "Cena salva!")
- **O que é salvo em cada cena:**
  - Todos os tokens (posições, visibilidade, imagens)
  - Mapa de fundo (imagem completa)
  - Posição e zoom do canvas
  - Todas as configurações (cores, tamanhos, opacidades)

### Grid e Visualização
- **🖱️ Arrastar Canvas**: Clique e arraste em área vazia para mover a visualização
- **🔍 Scroll**: Use a roda do mouse para zoom
- **⚙️ Painel de Controles** (canto superior esquerdo):
  - 📁 Carregar imagem de fundo (mapas de RPG)
  - 🎨 Ajustar cores, opacidades e tamanhos
  - 📏 Escalar imagem independente da grid
- **🗑️ Remover Imagem**: Limpa a imagem de fundo
- **🔄 Resetar**: Botão para voltar à visualização inicial

### Tokens
- **🎭 Painel de Tokens** (canto superior direito):
  - ➕ Criar novo token com nome e imagem
  - 📏 Definir tamanho do token (1-10 células)
  - 📋 Lista de todos os tokens criados
  - 👁️ Botões para mostrar/ocultar todos os tokens
- **🖱️ Arrastar Tokens**: Clique e arraste um token para movê-lo
- **🎯 Snap to Grid**: Tokens se encaixam automaticamente na grid
- **✅ Seleção**: Clique em um token para selecioná-lo (borda verde)
- **👁️ Toggle Visibilidade**: Botão azul para ocultar/mostrar token individualmente
  - Token oculto aparece em cinza na lista e não aparece no mapa
  - Perfeito para preparar encontros e revelar inimigos aos poucos
- **🗑️ Deletar**: Botão vermelho em cada token para removê-lo
- **📍 Posição**: Visualize as coordenadas de cada token na grid

## 📱 Suporte Mobile

O projeto também suporta gestos touch:
- Arraste com um dedo para mover
- Pinch com dois dedos para zoom

## 🛠️ Tecnologias

- Django 5.0.2
- HTML5 Canvas
- JavaScript (Vanilla)
- CSS3

## 🎲 Casos de Uso

**Perfeito para RPG de Mesa:**
1. Crie cenas separadas para cada encontro/local
2. Carregue mapas específicos em cada cena
3. Ajuste a grid para cobrir os mapas perfeitamente
4. Adicione tokens de personagens e inimigos
5. Prepare encontros ocultando inimigos
6. Troque entre cenas durante o jogo
7. Tudo é salvo automaticamente!
8. Ideal para D&D, Pathfinder, Call of Cthulhu, etc.

**Fluxo de Trabalho Recomendado:**

**Preparação (antes da sessão):**
1. Crie uma cena para cada encontro:
   - "Taverna" - mapa da taverna + NPCs
   - "Floresta - Emboscada" - mapa + goblins ocultos
   - "Caverna do Dragão" - mapa + dragão + tesouro
2. Configure cada cena:
   - Carregue o mapa apropriado
   - Ajuste grid e zoom
   - Adicione todos os tokens
   - Oculte inimigos que devem ser surpresa
3. Tudo salvo automaticamente!

**Durante o Jogo:**
- Troque de cena com um clique
- Revele inimigos gradualmente (botão 👁️)
- Mova tokens durante combate
- Use zoom para focar
- Cada cena mantém seu estado independente

**Outros Usos:**
- Planejamento arquitetônico
- Design de níveis de jogos
- Visualização de plantas baixas
- Gerenciamento de espaços e layouts
- Qualquer projeto que necessite de uma grid sobre imagem

## 💡 Otimizações

O sistema é altamente otimizado para garantir performance fluida mesmo com muitos elementos:

**Grid Rendering:**
- Renderiza apenas as linhas visíveis na viewport atual
- Cálculo dinâmico de linhas verticais e horizontais
- Ajuste automático de espessura baseado no zoom

**Imagem de Fundo:**
- Renderizada com transformações otimizadas do Canvas
- Opacidade controlável sem impacto na performance

**Sistema de Tokens:**
- Detecção de colisão eficiente (hit testing circular)
- Snap to grid automático para movimentação precisa
- Renderização com clipping para imagens circulares
- Sombras e bordas renderizadas com hardware acceleration

**Sistema de Persistência:**
- **Banco de dados PostgreSQL/SQLite** para armazenamento permanente
- **Cenas por sala** - cada sala tem suas próprias cenas isoladas
- Auto-save com debounce (500ms) para evitar saves excessivos
- Imagens convertidas para base64 (armazenadas no JSON do banco)
- Serialização/deserialização eficiente de estado
- Cada cena é completamente independente
- **API REST** para criar/editar/deletar/trocar cenas
- **WebSocket** para sincronização em tempo real

**Performance Geral:**
- Canvas HTML5 com aceleração por hardware
- Event handling otimizado para pan e zoom
- Redraw apenas quando necessário
- Suporte a centenas de tokens sem lag
- Troca instantânea entre cenas

Isso garante performance constante independente do nível de zoom, posição, quantidade de tokens ou número de cenas.

## 📖 Documentação Adicional

- `MULTIPLAYER_SETUP.md` - Como configurar o sistema multiplayer
- `IMPLEMENTACAO_MULTIPLAYER.md` - Guia de implementação dos templates
- **`CENAS_POR_SALA.md`** - Sistema de cenas por sala
- **`SISTEMA_CONTROLE_TOKENS.md`** - Sistema de controle de tokens por jogador **(NOVO!)**
- **`CORRECAO_WEBSOCKET.md`** - Correção de sincronização
- `COMO_USAR.md` - Como usar o sistema completo
- `STATUS_FINAL.md` - Status final do projeto

## 🎯 Novidades

### ✨ Sistema de Cenas por Sala
Agora cada sala tem suas próprias cenas salvas no banco de dados:
- ✅ Persistência permanente (não depende do navegador)
- ✅ Compartilhamento automático entre mestre e jogadores
- ✅ API REST para gerenciamento de cenas
- ✅ Sincronização em tempo real via WebSocket
- ✅ Isolamento total entre salas
- ✅ Gerenciamento pelo Django Admin

📚 Veja `CENAS_POR_SALA.md` para mais detalhes!

### 🎮 Sistema de Controle de Tokens por Jogador **(NOVO!)**
Mestre pode atribuir tokens específicos para cada jogador:
- ✅ Painel de jogadores online em tempo real
- ✅ Atribuição visual de tokens por jogador
- ✅ Jogadores movem apenas seus tokens
- ✅ Indicador visual (badge) mostrando ownership
- ✅ Sincronização em tempo real via WebSocket
- ✅ Segurança no backend (verificação de permissões)

📚 Veja `SISTEMA_CONTROLE_TOKENS.md` para mais detalhes!

