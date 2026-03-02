# Spotify Analytics - Frontend

Frontend moderno em React + TypeScript para visualização de dados do Spotify.

## 🚀 Tecnologias

- **React 18** - Biblioteca UI
- **TypeScript** - Type safety
- **Vite** - Build tool moderna e rápida
- **Tailwind CSS** - Estilização utilitária
- **Recharts** - Gráficos profissionais e interativos
- **Axios** - Cliente HTTP
- **Lucide React** - Ícones modernos

## 📦 Instalação

```bash
cd frontend
npm install
```

## 🏃 Desenvolvimento

```bash
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

**Importante:** Certifique-se de que a API backend está rodando em `http://127.0.0.1:8888`

## 🏗️ Build para Produção

```bash
npm run build
```

Os arquivos compilados estarão em `dist/`

## 📁 Estrutura

```
frontend/
├── src/
│   ├── api/          # Cliente API (Axios)
│   ├── components/   # Componentes React
│   ├── types/        # Tipos TypeScript
│   ├── App.tsx       # Componente principal
│   ├── main.tsx      # Entry point
│   └── index.css     # Estilos globais
├── package.json
└── vite.config.ts
```

## 🎨 Componentes

- **App.tsx** - Componente principal com estado e lógica
- **TracksChart** - Gráfico de barras para top músicas
- **ArtistsChart** - Gráfico de pizza para top artistas
- **StatsCards** - Cards de estatísticas
- **TracksGrid** - Grid com capas dos álbuns
- **AuthSection** - Tela de autenticação
- **LoadingSpinner** - Indicador de carregamento

## 🔧 Configuração

A URL da API pode ser configurada através da variável de ambiente:

```bash
VITE_API_URL=http://127.0.0.1:8888 npm run dev
```

Ou criar um arquivo `.env`:

```
VITE_API_URL=http://127.0.0.1:8888
```

## 📝 Notas

- O frontend faz proxy das requisições através do Vite para evitar problemas de CORS
- Todos os componentes são tipados com TypeScript
- Design responsivo e moderno com Tailwind CSS
- Gráficos interativos com Recharts
