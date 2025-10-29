# Grid Infinita - Projeto Django

Um projeto Django com uma grid infinita interativa e otimizada.

## 🚀 Características

- **Grid Infinita**: Renderiza apenas o que está visível na tela para máxima performance
- **Zoom**: Use a roda do mouse para dar zoom in/out (10% até 1000%)
- **Pan**: Clique e arraste para navegar pela grid
- **Imagem de Fundo**: Carregue mapas de RPG ou qualquer imagem como fundo
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

- **🖱️ Arrastar**: Clique e arraste para mover a visualização
- **🔍 Scroll**: Use a roda do mouse para zoom
- **⚙️ Painel de Controles**: No canto superior esquerdo para personalizar
  - 📁 Carregar imagem de fundo (mapas de RPG)
  - 🎨 Ajustar cores, opacidades e tamanhos
  - 📏 Escalar imagem independente da grid
- **🗑️ Remover Imagem**: Limpa a imagem de fundo
- **🔄 Resetar**: Botão para voltar à visualização inicial

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

**Perfect para RPG de Mesa:**
1. Carregue um mapa de RPG como imagem de fundo
2. Ajuste a grid para cobrir o mapa perfeitamente
3. Use zoom para focar em áreas específicas
4. Ajuste a opacidade da grid conforme necessário
5. Perfeito para sessões online de D&D, Pathfinder, etc.

**Outros Usos:**
- Planejamento arquitetônico
- Design de níveis de jogos
- Visualização de plantas baixas
- Qualquer projeto que necessite de uma grid sobre imagem

## 💡 Otimizações

O sistema renderiza apenas as linhas da grid que estão visíveis na viewport atual, calculando dinamicamente:
- Apenas linhas verticais visíveis
- Apenas linhas horizontais visíveis
- Imagem renderizada com transformações otimizadas
- Ajuste de espessura baseado no zoom

Isso garante performance constante independente do nível de zoom ou posição.

