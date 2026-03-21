# 🌃 FortalezaNight — Mapa de Shows & Bares

Site estático com mapa interativo (Leaflet) para descobrir shows, bares, baladas, gastrobares, lounges e festivais em Fortaleza.

---

## 📁 Estrutura do Projeto

```
fortaleza-map/
├── index.html   — página principal (mapa + sidebar)
└── data.js      — base de dados dos locais (edite aqui!)
```

Nenhum backend necessário. Funciona 100% no navegador.

---

## ▶️ Como usar

1. Abra a pasta no navegador (ou use um servidor local simples):
   ```
   npx serve .
   ```
   ou arraste o `index.html` direto para o Chrome.

2. Para adicionar um local, edite o arquivo `data.js` e adicione um objeto no array `PLACES`.

---

## ➕ Adicionando um novo local

```js
{
  id: 16,                        // número único
  nome: "Nome do Local",
  categoria: "Bar",              // veja categorias abaixo
  endereco: "Rua X, 123 — Bairro",
  bairro: "Aldeota",
  instagram: "@handle",          // ou "" se não tiver
  lat: -3.7300,                  // latitude (Google Maps → copie o primeiro número)
  lng: -38.5100,                 // longitude (segundo número)
  dia_evento: "Sábados — 20h"   // texto livre
}
```

### Categorias disponíveis

| Categoria    | Cor       | Emoji |
|--------------|-----------|-------|
| Show         | Amarelo   | 🎵    |
| Bar          | Rosa      | 🍺    |
| Balada       | Azul      | 🪩    |
| Gastrobar    | Laranja   | 🍽️    |
| Roof/Lounge  | Roxo      | ✨    |
| Festival     | Verde     | 🎪    |

Para adicionar uma nova categoria, edite o objeto `CAT_CONFIG` no `index.html`.

---

## 🌍 Como pegar coordenadas GPS

1. Abra [maps.google.com](https://maps.google.com)
2. Clique com o botão direito no local
3. Os dois números que aparecem são `lat` e `lng`

---

## 🚀 Deploy gratuito

- **GitHub Pages**: suba os dois arquivos em um repositório público e ative o Pages.
- **Netlify / Vercel**: arraste a pasta no painel de deploy.
