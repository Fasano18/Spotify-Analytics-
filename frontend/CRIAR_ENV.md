# 📝 Como Criar o Arquivo .env

Como o arquivo `.env` está protegido, você precisa criá-lo manualmente.

## 🚀 Passo a Passo

### 1. Crie o arquivo na pasta `frontend/`

```bash
cd frontend
touch .env
```

### 2. Adicione este conteúdo:

```env
VITE_API_URL=http://127.0.0.1:8888
```

### 3. Ou copie do exemplo:

```bash
cd frontend
cp env.example .env
```

## 📋 Conteúdo Completo do `.env`

```env
# URL da API Backend
# Se não definida, o Vite usará o proxy configurado em vite.config.ts
# Para desenvolvimento local, use: http://127.0.0.1:8888
VITE_API_URL=http://127.0.0.1:8888
```

## ✅ Verificar se Funcionou

Após criar o arquivo, reinicie o servidor:

```bash
npm run dev
```

O frontend vai usar a URL definida no `.env` para se conectar à API.
