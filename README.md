<div align="center">
  <img src="images/logo_metal_ceara.png" alt="Logo Metal Ceará" width="150" />
  
  # 🎸 Mapa & Agenda Metal Ceará 🤘
  
  **O guia definitivo de bares, shows e eventos da cena underground e heavy metal no estado do Ceará.** Construído com mapas interativos em tempo real para você nunca mais perder um bate-cabeça!
  
  ---
</div>

## LINK DO MAPA

http://andff.runasp.net/Agenda-de-Shows-Metal-Ceara/

## 🤘 Sobre o Projeto

O **Mapa Metal Ceará** é uma plataforma interativa de mapeamento focada exclusivamente na rota do rock e do metal cearense. Através de um mapa dinâmico provido pelo *Leaflet*, organizadores e o público em geral podem localizar bares temáticos, festivais e apresentações das bandas locais e internacionais que passam pelo estado.

### 🌟 Funcionalidades Principais
- 🗺️ **Mapa Interativo:** Navegue pelo Ceará para encontrar o role mais perto de você.
- ⚡ **Filtros Ágeis:** Busque atrações pelo nome, cidade, tipo (Bar, Show ou Evento) ou intervalo de datas.
- ⏳ **Status de Tempo Real:** Sistema progressivo que informa os dias restantes para o evento ou se o show acontece **HOJE**.
- 📍 **Integração GPS:** Trace rotas diretamente para o local usando a integração via clique com o Google Maps.
- 📱 **Mobile First:** Interface totalmente adaptada para uso nas mãos durante o trajeto pro bar!

---

## 🛠️ Tecnologias Utilizadas

Este ecossistema foi projetado para ser **rápido, leve e de custo zero** para hospedagem, utilizando uma arquitetura orientada a Front-End estático aliado a um CMS local.

- **Interface do Usuário (UI):** `HTML5`, `CSS3`, `JavaScript Vanilla`
- **Mapas & Clusters:** `Leaflet.js` e `Leaflet MarkerCluster`
- **Banco de Dados Estático:** `JSON` (`pontos.json`)
- **Gerenciador Administrativo Web:** Interface baseada no navegador (`admin.html`)
- **Gerenciador Desktop Profissional:** Construído em `Python 3` utilizando `Tkinter` na interface gráfica e `Pillow` para processamento das thumbnails.

---

## ⚙️ Como Executar o Projeto

Qualquer um pode rodar este projeto e usufruir da arquitetura, ou criar sua própria versão de mapa para outras temáticas!

### 1. Visualizando o Mapa (Usuário Padrão)
Não é necessário instalar nenhuma linguagem local no seu computador ou iniciar contêineres malucos. 
Basta abrir o arquivo **`index.html`** diretamente no seu navegador, ou hospedar o repositório no `GitHub Pages` / `Vercel`.

### 2. Cadastrando e Gerenciando os Locais (Administrador)
Você tem duas opções para modificar o sistema de pontos do mapa:

**Opção A: Gerenciador Web**
1. Abra o arquivo `admin.html` no navegador.
2. Adicione, edite ou exclua pontos graficamente.
3. Clique em "Baixar JSON", e substitua o arquivo original `pontos.json` da sua pasta pelo novo arquivo baixado.

**Opção B: App Desktop (Recomendado)**
1. Certifique-se de ter o Python 3 instalado no sistema.
2. Instale a biblioteca de imagem: `pip install Pillow`
3. Execute o programa administrativo:
   ```bash
   python gerenciador2.py
   ```
4. Essa versão atualiza o arquivo `pontos.json` automaticamente e já mostra um preview das imagens hospedadas na nuvem!

---

## 🤝 Como Contribuir

Achou um bug? O show mudou de local e o mapa está desatualizado? Ou você é desenvolvedor e tem uma dica para deixar a plataforma ainda mais insana?

1. Faça um Fork do projeto
2. Crie uma branch para a sua modificação: `git checkout -b feature/MoshPitFeature`
3. Faça o commit das suas alterações: `git commit -m 'Add: nova banda irada'`
4. Faça o push para a branch: `git push origin feature/MoshPitFeature`
5. Abra um **Pull Request** para avaliarmos!

---

<div align="center">
  <i>"Up the Irons!"</i> 🎸🍻<br>
  Desenvolvido com ódio, cerveja quente e muito código na veia por <b>Agenda-MetalCeara</b>.
</div>



<hr>

# 🛠️ Análise Técnica: Mapa Metal Ceará

## 📖 Visão Geral do Projeto
O **Mapa Metal Ceará** (ou Agenda Metal Ceará) é uma aplicação voltada para mapear e divulgar eventos, shows e bares focados no público e na cena do Heavy Metal e vertentes do rock no estado do Ceará. 

O sistema foi arquitetado de maneira **serverless (estática)** em sua camada principal de exibição, garantindo velocidade, segurança e altíssima facilidade de deploy (pode ser hospedado gratuitamente no GitHub Pages, Netlify ou Vercel).

---

## 🏗️ Arquitetura e Componentes

### 1. Front-end de Exibição (`index.html`)
- **Tecnologias:** HTML5, CSS3, JavaScript Vanilla.
- **Bibliotecas:** [Leaflet.js](https://leafletjs.com/) para renderização do mapa e `leaflet.markercluster` para agrupamento de pins.
- **Descrição:** Interface focada na UX, totalmente responsiva (mobile-first adaptado). Possui filtros avançados (por cidade, tipo de evento, intervalo de datas e busca textual).
- **Consumo de Dados:** Realiza um `fetch()` no arquivo local estático `pontos.json`. Não depende de requisições de backend, o que zera o tempo de latência em banco de dados.

### 2. Gerenciadores de Conteúdo (CMS)
O projeto apresenta **duas abordagens** para o gerenciamento de dados, o que é um ponto muito interessante:

#### A. Painel Web (`admin.html`)
- **Tecnologias:** HTML/JS Vanilla.
- **Dinâmica:** Lê o `pontos.json` e permite edição. Como é uma página estática local e navegadores não têm permissão nativa de reescrita de arquivos por segurança, a solução adotada foi gerar um download do aquivo `.json` atualizado. Isso é ideal para edições rápidas e pontuais.

#### B. Gerenciador Desktop (`gerenciador2.py`)
- **Tecnologias:** Python 3, `Tkinter` (GUI), `Pillow` (Processamento de Imagem).
- **Dinâmica:** Um aplicativo desktop robusto e completo para administrar o banco de dados. Permite operações CRUD diretas no arquivo `pontos.json` graças aos privilégios de execução no SO. 
- **Destaques:** Inclui carregamento em tempo real da preview de imagens hospedadas online, e integração direta com o Google Maps via coordenadas.

### 3. Banco de Dados (`pontos.json`)
- Arquivo NoSQL flat-file. Estrutura os eventos com geolocalização (latitude e longitude), links para redes sociais, datas e imagens. Extremamente leve e maleável.

---

## ✨ Pontos Fortes
1. **Performance e Custos:** Por não exigir um servidor rodando Node.js/PHP/Python no backend de exibição, o custo de manutenção da aplicação no ar é literalmente zero.
2. **Independência:** O app Python garante que a administração dos dados seja feita localmente com segurança e conforto, antes de um simples "git push" para o servidor.
3. **Usabilidade:** O sistema de filtros no front-end é instantâneo pois ocorre client-side com dados já cacheados. O sistema inteligente que calcula "dias restantes" para os eventos gera uma urgência positiva para o usuário.

---

## 🚀 Sugestões e Oportunidades de Evolução

- **Migração para BaaS (Backend as a Service):** Se o projeto escalar ou exigir que múltiplos promotores de eventos adicionem seus próprios shows (com logins), seria interessante trocar o `pontos.json` por um banco como o **Firebase / Firestore** ou **Supabase**. Isso eliminaria a necessidade do aplicativo Tkinter e permitiria atualizações em tempo real pelo `admin.html`.
- **PWA (Progressive Web App):** Como o projeto já tem o `site.webmanifest`, adicionar um arquivo `service-worker.js` básico permitiria que os usuários instalassem a Agenda Metal Ceará como um aplicativo nativo no celular, com direito a funcionamento parcial offline.
- **Melhoria no Tratamento de Erros de Imagem:** No front-end, adicionar um fallback visual caso o link da imagem retorne erro 404 seria ótimo para a estética da listagem.
- **Separar CSS/JS:** Futuramente, com o crescimento estrutural, separar as lógicas do `index.html` em `style.css` e `app.js` tornará a manutenção mais limpa.

---
*Análise técnica gerada de forma automatizada e especializada na arquitetura atual do repositório MapaMetalCeara.*
