# 🚀 Quick Start - Resolvendo Erros

## ⚠️ Erros Comuns

Os erros que você está vendo são porque **as dependências ainda não foram instaladas**.

## ✅ Solução Rápida

### 1. Instalar Dependências

```bash
cd frontend
npm install
```

Isso vai instalar:

- React e React DOM
- TypeScript e tipos
- Vite
- Tailwind CSS
- Recharts
- Axios
- Lucide React
- E todas as outras dependências

### 2. Verificar se funcionou

Após instalar, os erros de TypeScript devem desaparecer. Se ainda houver erros:

```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install
```

### 3. Rodar o Frontend

```bash
npm run dev
```

## 🔧 Se os Erros Persistirem

### Erro: "Cannot find module 'react'"

**Solução:** Execute `npm install` na pasta `frontend/`

### Erro: "Property 'env' does not exist on type 'ImportMeta'"

**Solução:** Já foi corrigido! O arquivo `src/vite-env.d.ts` foi criado.

### Erro: "JSX element implicitly has type 'any'"

**Solução:** Isso acontece quando o TypeScript não encontra os tipos do React. Execute:

```bash
npm install --save-dev @types/react @types/react-dom
```

## 📝 Checklist

- [ ] Executei `npm install` na pasta `frontend/`
- [ ] As dependências foram instaladas sem erros
- [ ] O arquivo `src/vite-env.d.ts` existe
- [ ] O TypeScript reconhece os tipos

## 🎯 Próximos Passos

1. **Instale as dependências:** `npm install`
2. **Rode o frontend:** `npm run dev`
3. **Rode a API:** `uvicorn app.main:app --reload --host 127.0.0.1 --port 8888`
4. **Acesse:** <http://localhost:3000>

## 💡 Dica

Se você usar VS Code, pode ser necessário:

1. Fechar e reabrir o editor
2. Ou executar: `Cmd+Shift+P` → "TypeScript: Restart TS Server"
