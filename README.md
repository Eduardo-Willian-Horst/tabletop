# 🎲 Grid Infinita - Sistema de RPG Multiplayer

Um sistema completo de RPG online com grid infinita, sincronização em tempo real e controle de tokens por jogador.

## ✨ Características Principais

### 🎮 Sistema Multiplayer Completo
- **Salas com código único** - Cada mesa de RPG tem seu próprio código de 6 caracteres
- **Autenticação de Mestres** - Sistema de login e registro para mestres
- **Entrada de Jogadores sem conta** - Jogadores entram apenas com nome
- **Sincronização em tempo real** - WebSocket para atualização instantânea
- **Controle de tokens por jogador** - Mestre atribui tokens específicos para cada jogador

### 🎬 Sistema de Cenas
- **Cenas salvas no banco de dados** - Persistência permanente no servidor
- **Cenas independentes por sala** - Cada sala tem suas próprias cenas
- **Auto-save automático** - Salva automaticamente a cada alteração (debounce 500ms)
- **Troca instantânea de cenas** - Mude entre cenas com um clique
- **Sincronização via WebSocket** - Mestre e jogadores veem as mesmas cenas
- **O que é salvo**: tokens, mapa, posições, zoom, todas as configurações

### 🎭 Sistema de Tokens
- **Imagens circulares** com nome
- **Drag and drop** - Arraste e solte tokens pelo mapa
- **Snap to grid** - Encaixe automático na grid
- **Múltiplos tamanhos** (1-10 células)
- **Toggle de visibilidade** - Ocultar/mostrar tokens individualmente
- **Controle por jogador** - Badge visual mostrando quem controla cada token
- **Movimentação sincronizada** - Todos veem os movimentos em tempo real

### 📐 Grid Infinita e Otimizada
- **Renderização inteligente** - Apenas o que está visível na tela
- **Zoom** - Use a roda do mouse (10% até 1000%)
- **Pan** - Clique e arraste para navegar
- **Canvas HTML5** - Performance com aceleração por hardware
- **Responsivo** - Funciona em desktop e mobile

### 🖼️ Sistema de Imagens
- **Integração com Cloudinary** - Armazenamento em nuvem (25 GB grátis)
- **CDN global** - Carregamento rápido de imagens
- **Upload de mapas** - Carregue mapas de RPG como fundo
- **Otimização automática** - Cloudinary comprime e otimiza as imagens
- **Imagens de tokens** - Upload de avatares para tokens

### ⚙️ Personalizável
- **Imagem de fundo** - Mapas de RPG, plantas, etc.
- **Opacidade da imagem** (0% - 100%)
- **Escala da imagem** (0.1x - 3.0x)
- **Cor do background**
- **Cor da grid**
- **Opacidade da grid** (0% - 100%)
- **Tamanho dos quadrados** (10px - 200px)
- **Espessura das linhas** (0.5px - 5px)

## 📦 Instalação

### 1. Instalar as dependências:
```bash
pip install -r requirements.txt
```

### 2. Executar as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Criar um superusuário (opcional, para acessar o admin):
```bash
python manage.py createsuperuser
```

### 4. Iniciar o servidor:
```bash
python manage.py runserver
```

### 5. Acessar no navegador:

**Página inicial:**
```
http://127.0.0.1:8000/
```

**Admin Django (gerenciar salas e cenas):**
```
http://127.0.0.1:8000/admin/
```

## 🎮 Como Usar

### Como Mestre 🎭

1. **Registrar e Fazer Login**
   - Acesse: `http://127.0.0.1:8000/register/`
   - Crie uma conta (username, email, senha)
   - Faça login em: `http://127.0.0.1:8000/login/`

2. **Criar Sala**
   - No dashboard, digite o nome da sala
   - Clique em "Criar Nova Sala"
   - **Anote o código gerado** (ex: ABC123)

3. **Preparar a Sessão**
   - Entre na sala
   - Crie cenas para diferentes encontros/locais
   - Carregue mapas específicos em cada cena
   - Adicione tokens de personagens e inimigos
   - Oculte inimigos que devem ser surpresa

4. **Durante o Jogo**
   - Compartilhe o código da sala com os jogadores
   - Troque entre cenas conforme a narrativa avança
   - Mova tokens durante combate
   - Revele inimigos gradualmente (botão 👁️)
   - Atribua tokens específicos para cada jogador
   - Tudo sincroniza automaticamente!

### Como Jogador 🎮

1. **Entrar na Sala**
   - Acesse: `http://127.0.0.1:8000/player/join/`
   - Digite seu nome (ex: João)
   - Digite o código da sala (fornecido pelo mestre)
   - Clique em "Entrar na Sala"

2. **Durante o Jogo**
   - Veja tudo que o mestre faz em tempo real
   - Navegue pelo mapa (zoom e pan)
   - Mova apenas os tokens que o mestre atribuiu para você
   - Não pode criar/deletar tokens ou cenas (apenas visualização + controle de tokens próprios)

## 🎯 Fluxo de Trabalho Recomendado

### Preparação (antes da sessão):
1. **Crie cenas para cada encontro:**
   - "Taverna" - mapa da taverna + NPCs
   - "Floresta - Emboscada" - mapa + goblins ocultos
   - "Caverna do Dragão" - mapa + dragão + tesouro

2. **Configure cada cena:**
   - Carregue o mapa apropriado
   - Ajuste grid e zoom
   - Adicione todos os tokens
   - Oculte inimigos que devem ser surpresa

3. **Tudo salvo automaticamente!**

### Durante o Jogo:
- Troque de cena com um clique
- Atribua tokens para cada jogador
- Jogadores movem seus próprios tokens
- Revele inimigos gradualmente
- Use zoom para focar
- Cada cena mantém seu estado independente

## 🎭 Controle de Tokens por Jogador

### Painel de Jogadores (Mestre)
- Lista todos os jogadores conectados em tempo real
- Dropdown para atribuir tokens a cada jogador
- Indicador visual (badge) mostrando quem controla cada token
- Auto-save ao atribuir tokens

### Para os Jogadores
- **Badge VERDE** com suas iniciais no token atribuído
- **Badge AZUL** nos tokens de outros jogadores
- Pode mover apenas tokens atribuídos pelo mestre
- Movimentação sincronizada em tempo real
- Feedback visual e no console sobre permissões

### Segurança
- Verificação no backend de permissões
- Jogadores só movem tokens com `controlledBy` correspondente
- Isolamento por sala
- Mestre pode reatribuir tokens a qualquer momento

## 🛠️ Tecnologias Utilizadas

- **Django 5.0.2** - Framework web
- **Django Channels** - WebSockets para tempo real
- **Daphne** - ASGI server
- **Cloudinary** - Armazenamento de imagens na nuvem
- **HTML5 Canvas** - Renderização do tabuleiro
- **JavaScript (Vanilla)** - Frontend interativo
- **WebSocket** - Sincronização em tempo real
- **SQLite/PostgreSQL** - Banco de dados

## 🎲 Casos de Uso

### RPG de Mesa Online
Perfeito para D&D, Pathfinder, Call of Cthulhu, etc.:
- Prepare cenas para cada encontro
- Atribua tokens de personagens para os jogadores
- Jogadores movem seus próprios personagens
- Mestre controla NPCs e inimigos
- Troque entre locais/cenas durante a sessão
- Oculte/revele inimigos conforme necessário

### Outros Usos
- Planejamento arquitetônico
- Design de níveis de jogos
- Visualização de plantas baixas
- Gerenciamento de espaços e layouts
- Qualquer projeto que necessite de uma grid sobre imagem

## 📊 Estrutura do Projeto

```
eduardo_proj/
├── grid/                          # App principal
│   ├── models.py                  # Room, RoomMember, Scene
│   ├── consumers.py               # WebSocket handler
│   ├── views.py                   # Views e API REST
│   ├── routing.py                 # WebSocket routing
│   ├── admin.py                   # Admin Django
│   ├── templates/grid/            # Templates HTML
│   │   ├── login.html             # Login do mestre
│   │   ├── register.html          # Registro
│   │   ├── player_join.html       # Entrada de jogador
│   │   ├── dashboard.html         # Dashboard do mestre
│   │   ├── master_room.html       # Sala do mestre
│   │   ├── player_room.html       # Sala do jogador
│   │   └── infinite_grid.html     # Grid standalone
│   └── migrations/                # Migrações do banco
├── infinite_grid/                 # Configurações Django
│   ├── settings.py                # Settings + Cloudinary config
│   ├── urls.py                    # URLs principais
│   ├── asgi.py                    # ASGI para WebSocket
│   └── wsgi.py                    # WSGI padrão
├── requirements.txt               # Dependências Python
├── manage.py                      # Django management
└── README.md                      # Este arquivo
```

## 🔌 API REST de Cenas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/room/<code>/scenes/` | Lista todas as cenas da sala |
| `POST` | `/api/room/<code>/scenes/create/` | Cria nova cena |
| `PUT` | `/api/room/<code>/scenes/<id>/` | Atualiza cena existente |
| `DELETE` | `/api/room/<code>/scenes/<id>/delete/` | Deleta cena |
| `POST` | `/api/room/<code>/scenes/<id>/switch/` | Troca para outra cena |
| `POST` | `/api/upload/image/` | Upload de imagem para Cloudinary |

## 💡 Otimizações

### Grid Rendering
- Renderiza apenas as linhas visíveis na viewport
- Cálculo dinâmico de linhas verticais e horizontais
- Ajuste automático de espessura baseado no zoom

### Sistema de Tokens
- Detecção de colisão eficiente
- Snap to grid automático
- Renderização otimizada com clipping circular
- Sombras e bordas com hardware acceleration

### Sistema de Persistência
- Banco de dados (PostgreSQL/SQLite) para cenas
- Auto-save com debounce (500ms)
- Cloudinary para imagens (não LocalStorage)
- API REST para gerenciamento
- WebSocket para sincronização

### Performance Geral
- Canvas HTML5 com aceleração por hardware
- Event handling otimizado
- Redraw apenas quando necessário
- Suporta centenas de tokens sem lag

## 🔧 Configuração do Cloudinary

As credenciais do Cloudinary já estão configuradas em `infinite_grid/settings.py`:

```python
cloudinary.config(
    cloud_name = "di0zoi7ru",
    api_key = "126586338643965",
    api_secret = "14ILPQN14MciqjmImF79910dV_I"
)
```

**Plano Gratuito:**
- ✅ 25 GB de armazenamento
- ✅ 25 GB de bandwidth/mês
- ✅ 25,000 transformações/mês

## 🎨 Controles

### Cenas
- **➕ Criar nova cena** - Painel inferior esquerdo
- **🔄 Trocar cena** - Clique em uma cena na lista
- **🗑️ Deletar cena** - Botão de lixeira em cada cena
- **✅ Cena ativa** - Destacada com borda verde
- **💾 Auto-save** - Indicador "Cena salva!" aparece automaticamente

### Grid e Visualização
- **🖱️ Arrastar Canvas** - Clique e arraste em área vazia
- **🔍 Scroll** - Roda do mouse para zoom
- **⚙️ Painel de Controles** - Canto superior esquerdo
- **🔄 Resetar** - Volta à visualização inicial

### Tokens
- **➕ Criar token** - Painel superior direito
- **🖱️ Arrastar tokens** - Clique e arraste
- **👁️ Toggle visibilidade** - Botão azul em cada token
- **🗑️ Deletar token** - Botão vermelho em cada token
- **👥 Atribuir a jogador** - Dropdown no painel de jogadores (apenas mestre)

## 📱 Suporte Mobile

O projeto suporta gestos touch:
- Arraste com um dedo para mover
- Pinch com dois dedos para zoom

## 🐛 Troubleshooting

### WebSocket não conecta
- Verifique se o servidor está rodando
- Verifique console do navegador (F12)
- Deve aparecer: "✅ WebSocket conectado à sala"

### Jogador não vê updates
- Recarregue a página (F5)
- Verifique o código da sala
- Verifique console (F12) por erros
- Certifique-se que o mestre está na mesma sala

### Imagens não aparecem
- Verifique credenciais do Cloudinary
- Abra Console do navegador (F12)
- Veja se há erros de CORS
- Verifique se o URL do Cloudinary está correto

### Jogador não consegue mover token
- Verifique se o mestre atribuiu o token para o jogador
- Veja se o badge verde aparece no token
- Console deve mostrar: "✅ Você pode mover este token"

## 🚀 Para Produção

### Usar Redis para Channel Layer
Em `settings.py`:
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

### Outras Configurações
- Configure `ALLOWED_HOSTS`
- Use HTTPS/WSS
- Configure backup do banco de dados
- Monitore uso do Cloudinary

## 💡 Melhorias Futuras (Opcional)

### Recursos Extras
- Chat entre jogadores
- Dice roller integrado
- HP bars nos tokens
- Sistema de iniciativa de combate
- Fog of war dinâmico
- Histórico de ações
- Sistema de convites por email
- Medidor de distância
- Anotações no mapa

### Integrações
- Discord bot para notificações
- Roll20 import/export
- D&D Beyond integration

## 📄 Licença

Este projeto é de código aberto.

## 🎉 Status

**100% Funcional e Pronto para Uso!** 

- ✅ Sistema multiplayer completo
- ✅ Sincronização em tempo real
- ✅ Controle de tokens por jogador
- ✅ Cenas salvas no banco de dados
- ✅ Integração com Cloudinary
- ✅ Interface intuitiva e responsiva
- ✅ Performance otimizada
- ✅ Documentado

**Divirta-se jogando RPG online!** 🎲🎭🗺️✨
