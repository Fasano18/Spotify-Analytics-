# 📚 Documentação dos Endpoints - Spotify Analytics API

**Base URL:** `http://127.0.0.1:8888`

**Swagger UI:** `http://127.0.0.1:8888/docs` (documentação interativa)

**Dashboard Web:** `http://127.0.0.1:8888/` (interface visual com gráficos)

---

## 🎨 Dashboard Web (Interface Visual)

A API inclui um **dashboard web interativo** com gráficos e visualizações dos seus dados do Spotify.

### Como acessar

1. **Inicie o servidor:**

   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8888
   ```

2. **Abra no navegador:**

   ```
   http://127.0.0.1:8888/
   ```

3. **Faça login:** O dashboard detectará automaticamente se você está autenticado. Se não estiver, clique no botão "Fazer Login com Spotify".

### Funcionalidades do Dashboard

- 📊 **Gráfico de Barras:** Top 10 músicas por popularidade
- 🎤 **Gráfico de Pizza:** Top 10 artistas
- 🎵 **Galeria de Capas:** Visualização das capas dos álbums das top músicas (clique para abrir no Spotify)
- 📈 **Estatísticas:** Total de músicas, artistas, popularidade média e tempo total
- ⏱️ **Filtros de Tempo:** Selecione entre últimas 4 semanas, últimos 6 meses ou todos os tempos

### Recursos

- **Design Responsivo:** Funciona em desktop e mobile
- **Atualização em Tempo Real:** Botão para atualizar os dados
- **Visualização Interativa:** Gráficos interativos usando Chart.js
- **Links Diretos:** Clique nas capas para abrir no Spotify

---

## 🔐 Autenticação

**IMPORTANTE:** Antes de usar qualquer endpoint de dados, você **DEVE** fazer login primeiro para obter um token de acesso.

### 1. Login (Iniciar autenticação)

**GET** `/auth/login`

Redireciona para a página de login do Spotify (fluxo OAuth2).

**Como usar:**

- Abra no navegador: `http://127.0.0.1:8888/auth/login`
- Faça login com sua conta Spotify
- Aceite as permissões solicitadas
- Você será redirecionado automaticamente para `/auth/callback`

**Exemplo:**

```bash
# No navegador:
http://127.0.0.1:8888/auth/login
```

---

### 2. Callback (Receber token)

**GET** `/auth/callback?code={code}`

Este endpoint é chamado automaticamente pelo Spotify após o login. Você não precisa chamá-lo manualmente.

**Resposta esperada:**

```json
{
  "access_token": "BQD...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "AQC...",
  "scope": "playlist-read-private playlist-read-collaborative user-read-email user-read-recently-played user-read-private user-top-read"
}
```

---

### 3. Logout

**GET** `/auth/logout`

Limpa o token armazenado em memória, efetivamente realizando o logout.

**Exemplo:**

```bash
curl -X GET http://127.0.0.1:8888/auth/logout -i
```

**Resposta:** `204 No Content`

---

## 🎵 Top Músicas

### Listar Top Músicas

**GET** `/top/tracks`

Retorna as músicas mais ouvidas pelo usuário em um determinado período.

**Parâmetros de Query:**

- `time_range` (opcional): `short_term` | `medium_term` | `long_term`
  - `short_term`: Últimas 4 semanas
  - `medium_term`: Últimos 6 meses (padrão)
  - `long_term`: Últimos anos
- `limit` (opcional): Número entre 1 e 50 (padrão: 20)

**Exemplos:**

```bash
# Top 20 músicas dos últimos 6 meses (padrão)
curl "http://127.0.0.1:8888/top/tracks"

# Top 10 músicas do último mês
curl "http://127.0.0.1:8888/top/tracks?time_range=short_term&limit=10"

# Top 30 músicas de todos os tempos
curl "http://127.0.0.1:8888/top/tracks?time_range=long_term&limit=30"
```

**Resposta esperada:**

```json
{
  "itens": [
    {
      "id": "2LXtyj95dK56ENS1QLt4IB",
      "nome": "Beach Baby",
      "artistas": ["Bon Iver"],
      "album": "Blood Bank",
      "popularidade": 69,
      "duracao_ms": 160093,
      "duracao_minutos": 2.67,
      "preview_url": null,
      "url_externa": "https://open.spotify.com/track/2LXtyj95dK56ENS1QLt4IB",
      "imagem_capa": "https://i.scdn.co/image/ab67616d0000b27333a839e8b2cf1512f3badabb"
    }
  ],
  "paginacao": {
    "limite": 20,
    "offset": 0,
    "total": 3926
  }
}
```

---

## 👤 Top Artistas

### Listar Top Artistas

**GET** `/top/artists`

Retorna os artistas mais ouvidos pelo usuário em um determinado período.

**Parâmetros de Query:**

- `time_range` (opcional): `short_term` | `medium_term` | `long_term` (padrão: `medium_term`)
- `limit` (opcional): Número entre 1 e 50 (padrão: 20)

**Exemplos:**

```bash
# Top 20 artistas dos últimos 6 meses (padrão)
curl "http://127.0.0.1:8888/top/artists"

# Top 10 artistas do último mês
curl "http://127.0.0.1:8888/top/artists?time_range=short_term&limit=10"

# Top 30 artistas de todos os tempos
curl "http://127.0.0.1:8888/top/artists?time_range=long_term&limit=30"
```

**Resposta esperada:**

```json
{
  "itens": [
    {
      "id": "4Z8W4fKeB5YxbusRsdQVPb",
      "nome": "Radiohead",
      "generos": ["alternative rock", "art rock", "britpop"],
      "popularidade": 85,
      "seguidores": 15000000,
      "url_externa": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb",
      "imagem_perfil": "https://i.scdn.co/image/..."
    }
  ],
  "paginacao": {
    "limite": 20,
    "offset": 0,
    "total": 150
  }
}
```

---

## 🕒 Histórico

### Histórico Recente de Músicas

**GET** `/history`

Retorna o histórico recente de músicas reproduzidas pelo usuário.

**Parâmetros de Query:**

- `limit` (opcional): Número entre 1 e 50 (padrão: 50)

**Exemplos:**

```bash
# Últimas 50 músicas reproduzidas (padrão)
curl "http://127.0.0.1:8888/history"

# Últimas 20 músicas reproduzidas
curl "http://127.0.0.1:8888/history?limit=20"
```

**Resposta esperada:**

```json
{
  "itens": [
    {
      "id": "2LXtyj95dK56ENS1QLt4IB",
      "nome": "Beach Baby",
      "artistas": ["Bon Iver"],
      "album": "Blood Bank",
      "popularidade": 69,
      "duracao_ms": 160093,
      "duracao_minutos": 2.67,
      "preview_url": null,
      "url_externa": "https://open.spotify.com/track/2LXtyj95dK56ENS1QLt4IB",
      "imagem_capa": "https://i.scdn.co/image/...",
      "reproduzida_em": "2024-01-15T10:30:00Z"
    }
  ],
  "paginacao": {
    "limite": 50,
    "offset": 0,
    "total": 50
  }
}
```

---

## 🔧 Infraestrutura

### Healthcheck

**GET** `/health`

Endpoint simples para verificar se a API está funcionando.

**Exemplo:**

```bash
curl http://127.0.0.1:8888/health
```

**Resposta esperada:**

```json
{
  "status": "ok"
}
```

---

## ⚠️ Erros Comuns

### Token não encontrado

**Erro:** `{"codigo": "token_expired", "mensagem": "Token não encontrado. Faça login para continuar."}`

**Solução:** Faça login novamente através de `/auth/login`

### Token expirado

**Erro:** `{"codigo": "token_expired", "mensagem": "Token expirado."}`

**Solução:** O token expira após 1 hora. Faça login novamente ou o sistema tentará renovar automaticamente usando o `refresh_token`.

### Validação de parâmetros

**Erro:** `{"codigo": "validation_error", "mensagem": "Os dados enviados são inválidos...", "detalhes": [...]}`

**Solução:** Verifique os parâmetros enviados. Por exemplo:

- `limit` deve estar entre 1 e 50
- `time_range` deve ser `short_term`, `medium_term` ou `long_term`

---

## 📝 Notas Importantes

1. **Token em memória:** O token é armazenado apenas em memória. Se você reiniciar o servidor, precisará fazer login novamente.

2. **Autenticação automática:** Após fazer login, o token é usado automaticamente em todas as requisições. Você não precisa enviar o token manualmente.

3. **Rate Limiting:** A API do Spotify tem limites de requisições. Se você receber um erro 429, aguarde alguns segundos antes de tentar novamente.

4. **Swagger UI:** Acesse `http://127.0.0.1:8888/docs` para ver a documentação interativa completa com todos os endpoints e poder testar diretamente pelo navegador.

---

## 🚀 Fluxo Completo de Uso

1. **Inicie o servidor:**

   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8888
   ```

2. **Faça login:**
   - Abra no navegador: `http://127.0.0.1:8888/auth/login`
   - Faça login com sua conta Spotify
   - Aceite as permissões

3. **Teste os endpoints:**

   ```bash
   # Top músicas
   curl "http://127.0.0.1:8888/top/tracks?time_range=medium_term&limit=20"
   
   # Top artistas
   curl "http://127.0.0.1:8888/top/artists?time_range=medium_term&limit=20"
   
   # Histórico
   curl "http://127.0.0.1:8888/history?limit=50"
   ```

4. **Logout (opcional):**

   ```bash
   curl -X GET http://127.0.0.1:8888/auth/logout
   ```

---

**Última atualização:** Janeiro 2024
