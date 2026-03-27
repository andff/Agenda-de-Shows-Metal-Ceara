<div align="center">
  <img src="img/logo_metal_ceara.png" alt="Logo Metal Ceará" width="250" />
  
  # 🎸 Agenda de Shows Metal Ceará 🤘
  
  **O guia definitivo de bares, shows e eventos da cena underground e heavy metal no estado do Ceará.** <br>
  Construído com mapas interativos em tempo real para você não perder nenhum role!

  [![Website](https://img.shields.io/badge/Acessar_Mapa-black?style=for-the-badge&logo=google-chrome&logoColor=white)](http://andff.runasp.net/Agenda-de-Shows-Metal-Ceara/)
  [![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white)](https://www.instagram.com/metal_ceara/)
  [![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://chat.whatsapp.com/LpPIObZx6MIEqFG444peFl)
</div>

---

## 📖 Sobre o Projeto

O **Agenda de Shows Metal Ceará** é uma plataforma interativa de mapeamento focada exclusivamente na rota do rock e do metal cearense. Através de um mapa dinâmico provido pelo *Leaflet*, organizadores e o público em geral podem localizar bares temáticos, festivais e apresentações das bandas locais e internacionais que passam pelo estado do Ceará.

---

## 🌟 Funcionalidades Principais

- 🗺️ **Mapa Interativo:** Navegue pelo estado do Ceará para encontrar o rolê mais perto de você.
- ⚡ **Filtros Ágeis:** Busque atrações pelo nome, cidade, tipo (Bar, Show ou Evento) ou intervalo de datas.
- ⏳ **Status Local:** Sistema progressivo que informa os dias restantes para o evento ou destaca se o show acontece **HOJE**.
- 📍 **Integração GPS:** Trace rotas diretamente para o local via clique com integração ao Google Maps.
- 📱 **Design Responsivo:** Interface fluida para celular e desktop.

---

## 🛠️ Tecnologias Utilizadas

O sistema foi projetado para ser **rápido, leve e de custo zero** na hospedagem, utilizando uma arquitetura orientada a Front-End estático em conjunto com um CMS local.

**Frontend:**
- `HTML5`, `CSS3` e `JavaScript Vanilla`
- `Leaflet.js` e `Leaflet MarkerCluster` (Mapas interativos e agrupamento de ícones)

**Banco de Dados:**
- Arquitetura Serverless armazenando os dados em `database/database.json`.

**Administração (CMS Local):**
- Gerenciador Desktop Profissional construído em `Python 3` utilizando `Tkinter` para a interface gráfica e `Pillow` para o processamento otimizado de miniaturas.

---

## 🚀 Como Rodar o Projeto

1. Faça o clone deste repositório:
   ```bash
   git clone https://github.com/SeuUsuario/Agenda-de-Shows-Metal-Ceara.git
   ```
2. Abra a pasta do projeto:
   ```bash
   cd Agenda-de-Shows-Metal-Ceara
   ```
3. Inicie um servidor web local. Se tiver o Python instalado, você pode usar:
   ```bash
   python -m http.server 8000
   ```
4. Acesse em seu navegador: [http://localhost:8000](http://localhost:8000)

> **Nota:** É essencial rodar através de um servidor web local (Live Server, Python HTTP) para que o navegador não bloqueie o carregamento do arquivo local `database.json` via restrições de CORS.

---

## 🤝 Como Contribuir

Achou um bug? O show mudou de local e o mapa está desatualizado? Ou você é desenvolvedor e tem uma dica para deixar a plataforma melhor?

**EM BREVE 🤘** - Mais informações sobre pull requests e submissão de novos locais e eventos serão disponibilizadas!