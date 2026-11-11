# PAIM IA PROSPECT VER46 GITHUB

Arquitetura:

- GitHub Pages: `index.html`, `config.js`
- Render Web Service: `app.py`, `paim_engine.py`, `requirements.txt`
- Fonte de dados: Overture Maps, sem Google Places e sem API Key

## 1. Subir todos os arquivos para o repositório GitHub

Coloque estes arquivos na raiz do repositório:

- index.html
- config.js
- app.py
- paim_engine.py
- requirements.txt
- render.yaml
- .gitignore

## 2. Publicar o backend no Render

1. Acesse https://dashboard.render.com
2. Clique em **New +** > **Blueprint**.
3. Conecte o repositório `PAIM-PROSPECT.IA-`.
4. Confirme o serviço `paim-prospect-api` no plano Free.
5. Aguarde o deploy concluir.
6. Copie a URL fornecida, por exemplo:
   `https://paim-prospect-api.onrender.com`
7. Teste no navegador:
   `https://paim-prospect-api.onrender.com/api/health`

A resposta precisa conter `"ok": true` e aproximadamente 5.570 municípios.

## 3. Configurar o GitHub Pages

Edite `config.js` e troque:

```js
window.PAIM_API_BASE = 'https://SEU-SERVICO.onrender.com';
```

pela URL real do Render, sem barra final. Faça commit.

Em **Settings > Pages**:

- Source: Deploy from a branch
- Branch: main
- Folder: / (root)

## 4. Testar

Abra:

`https://paimlab-coder.github.io/PAIM-PROSPECT.IA-/`

Primeiro teste recomendado:

- UF: AM
- Cidade: Manaus
- Segmento: Operador logístico
- Raio: 20 km
- Limite: 50

## Observações do plano Free do Render

O serviço pode dormir após inatividade e levar cerca de um minuto para acordar. O filesystem é temporário, portanto o cache Overture pode ser recriado após reinicialização.
