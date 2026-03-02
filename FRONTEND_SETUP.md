# 🎨 Frontend React - Guia de Setup

O projeto agora possui um **frontend moderno em React** separado da API, com gráficos profissionais e design atualizado.

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
cd frontend
npm install
```

### 2. Configurar Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` na pasta `frontend/`:

```env
VITE_API_URL=http://127.0.0.1:8888
```

### 3. Rodar o Frontend

```bash
npm run dev
```

O frontend estará disponível em: **<http://localhost:3000>**

### 4. Rodar a API Backend

Em outro terminal, na raiz do projeto:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8888
```

## 📦 Tecnologias Utilizadas

- **React 18** + **TypeScript** - Framework moderno com type safety
- **Vite** - Build tool ultra-rápida
- **Tailwind CSS** - Estilização utilitária e responsiva
- **Recharts** - Gráficos profissionais e interativos
- **Axios** - Cliente HTTP para comunicação com a API
- **Lucide React** - Ícones modernos e bonitos

## 🎨 Funcionalidades

### Gráficos Profissionais

- **Gráfico de Barras Horizontal**: Top 10 músicas por popularidade
- **Gráfico de Pizza**: Top 10 artistas com cores vibrantes
- **Cards de Estatísticas**: Total de músicas, artistas, popularidade média, tempo total
- **Grid de Capas**: Visualização das capas dos álbuns (clicáveis para abrir no Spotify)

### Design Moderno

- **Gradiente escuro** com tema Spotify
- **Glassmorphism** nos cards (efeito de vidro)
- **Animações suaves** em hover e transições
- **Totalmente responsivo** (mobile, tablet, desktop)
- **Cores do Spotify** integradas

### Interatividade

- **Filtros de tempo**: Últimas 4 semanas, últimos 6 meses, todos os tempos
- **Atualização em tempo real**: Botão para recarregar dados
- **Links diretos**: Clique nas capas para abrir no Spotify
- **Tooltips informativos**: Passe o mouse sobre os gráficos

## 📁 Estrutura do Projeto

```
frontend/
├── src/
│   ├── api/
│   │   └── client.ts          # Cliente Axios para API
│   ├── components/
│   │   ├── ArtistsChart.tsx   # Gráfico de pizza (artistas)
│   │   ├── AuthSection.tsx    # Tela de login
│   │   ├── LoadingSpinner.tsx # Indicador de carregamento
│   │   ├── StatsCards.tsx     # Cards de estatísticas
│   │   ├── TracksChart.tsx    # Gráfico de barras (músicas)
│   │   └── TracksGrid.tsx     # Grid de capas dos álbuns
│   ├── types/
│   │   └── index.ts           # Tipos TypeScript
│   ├── App.tsx                # Componente principal
│   ├── main.tsx               # Entry point
│   └── index.css              # Estilos globais (Tailwind)
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 🔧 Scripts Disponíveis

```bash
# Desenvolvimento (com hot reload)
npm run dev

# Build para produção
npm run build

# Preview da build de produção
npm run preview

# Lint do código
npm run lint
```

## 🎯 Como Usar

1. **Inicie a API backend** (porta 8888)
2. **Inicie o frontend** (porta 3000)
3. **Acesse** <http://localhost:3000>
4. **Faça login** com Spotify quando solicitado
5. **Explore** os gráficos e visualizações!

## 🎨 Personalização

### Cores

As cores do Spotify estão configuradas no `tailwind.config.js`:

```js
colors: {
  spotify: {
    green: '#1DB954',
    dark: '#191414',
    light: '#1ed760',
  }
}
```

### Gráficos

Os gráficos usam **Recharts**. Para personalizar, edite os componentes em `src/components/`:

- `TracksChart.tsx` - Gráfico de barras
- `ArtistsChart.tsx` - Gráfico de pizza

### Estilos

Os estilos globais estão em `src/index.css` usando Tailwind CSS.

## 🐛 Troubleshooting

### CORS Errors

O Vite está configurado para fazer proxy das requisições. Se ainda tiver problemas:

1. Verifique se a API está rodando em `http://127.0.0.1:8888`
2. Verifique o `vite.config.ts` - o proxy está configurado para `/api`

### Erro de Autenticação

Se aparecer erro de token:

1. Faça logout e login novamente
2. Verifique se a API backend está rodando
3. Verifique se o token foi salvo corretamente

### Porta já em uso

Se a porta 3000 estiver ocupada, o Vite tentará usar outra porta automaticamente. Verifique o terminal para ver qual porta foi usada.

## 📝 Próximos Passos

- [ ] Adicionar mais tipos de gráficos (linha, área, etc.)
- [ ] Implementar cache de dados
- [ ] Adicionar exportação de dados (PDF, CSV)
- [ ] Adicionar comparação entre períodos
- [ ] Implementar dark/light mode toggle
