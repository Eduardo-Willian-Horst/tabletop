# Grid Infinita - Projeto Django

Um projeto Django com uma grid infinita interativa e otimizada.

## 🚀 Características

- **Grid Infinita**: Renderiza apenas o que está visível na tela para máxima performance
- **Zoom**: Use a roda do mouse para dar zoom in/out (10% até 1000%)
- **Pan**: Clique e arraste para navegar pela grid
- **Imagem de Fundo**: Carregue mapas de RPG ou qualquer imagem como fundo
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

2. Execute as migrações (opcional, não há models neste projeto):
```bash
python manage.py migrate
```

3. Inicie o servidor:
```bash
python manage.py runserver
```

4. Acesse no navegador:
```
http://localhost:8000
```

## 🎮 Controles

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
1. Carregue um mapa de RPG como imagem de fundo
2. Ajuste a grid para cobrir o mapa perfeitamente
3. Crie tokens para personagens, monstros e NPCs
4. Prepare encontros ocultando tokens de inimigos
5. Revele inimigos gradualmente durante o jogo
6. Arraste tokens pelo mapa durante o combate
7. Use zoom para focar em áreas específicas
8. Ajuste a opacidade da grid conforme necessário
9. Ideal para sessões online de D&D, Pathfinder, Call of Cthulhu, etc.

**Fluxo de Trabalho Recomendado:**
- **Preparação**: Carregue e ajuste escala/posição da imagem
- **Configure a grid**: Ajuste tamanho para alinhar com o mapa
- **Crie tokens**: Adicione personagens e inimigos antes da sessão
- **Prepare encontros**: Oculte tokens de inimigos usando o botão 👁️
- **Durante o jogo**: 
  - Revele inimigos aos poucos
  - Mova tokens conforme os personagens se movem
  - Ajuste zoom para focar em combates
  - Acompanhe posições em tempo real

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

**Performance Geral:**
- Canvas HTML5 com aceleração por hardware
- Event handling otimizado para pan e zoom
- Redraw apenas quando necessário
- Suporte a centenas de tokens sem lag

Isso garante performance constante independente do nível de zoom, posição ou quantidade de tokens.

