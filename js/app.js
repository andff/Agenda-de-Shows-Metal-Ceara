// menu mobile
menuBtn.onclick = () => {
    sidebar.classList.toggle("ativo");
    menuBtn.innerHTML = sidebar.classList.contains("ativo") ? "✖" : "☰";
};

// toggle menu lateral
function toggleMenu(id, btn) {
    const content = document.getElementById(id);
    const isActive = content.classList.contains('active');

    document.querySelectorAll('.menu-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.menu-btn').forEach(el => el.classList.remove('active'));

    if (!isActive) {
        content.classList.add('active');
        btn.classList.add('active');
        if (id === 'estatisticas') renderEstatisticas(); // <-- linha nova
    }
}

// mapa
var map = L.map('map', {
    zoomControl: false
});

L.Icon.Default.imagePath = 'img/';

L.control.zoom({
    position: 'topright'
}).addTo(map);

// ── Tiles disponíveis ──
var tiles = {
    dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    positron: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    voyager: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    topo: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',

};

// ── Trocar tipo de mapa ──
function trocarMapa(tipo) {
    if (camadaTile) map.removeLayer(camadaTile);
    camadaTile = L.tileLayer(tiles[tipo], { attribution: '© OpenStreetMap' }).addTo(map);

    // Salva a preferência no localStorage
    localStorage.setItem('tipoMapa', tipo);

    document.querySelectorAll('#menuMapa button').forEach(b => {
        b.classList.toggle('selecionado', b.dataset.tile === tipo);
    });

    document.getElementById('menuMapa').classList.remove('aberto');
    document.getElementById('btnMapa').classList.remove('ativo');
}

// Inicia com o tile salvo ou o padrão 'dark'
var mapaSalvo = localStorage.getItem('tipoMapa') || 'dark';
var camadaTile;
trocarMapa(mapaSalvo);

// Abre/fecha o menu de mapas
document.getElementById('btnMapa').onclick = function () {
    var menu = document.getElementById('menuMapa');
    var aberto = menu.classList.toggle('aberto');
    this.classList.toggle('ativo', aberto);
};

// fechar menu ao clicar no mapa no mobile
map.on('click', () => {
    // fecha sidebar no mobile
    if (window.innerWidth < 768 && sidebar.classList.contains("ativo")) {
        sidebar.classList.remove("ativo");
        menuBtn.innerHTML = "☰";
    }
    // fecha menu de mapas
    document.getElementById('menuMapa').classList.remove('aberto');
    document.getElementById('btnMapa').classList.remove('ativo');
});

// camada de marcadores (sem cluster)
var markerLayer = L.featureGroup().addTo(map);

// ícones
var icones = {
    bar: L.icon({ iconUrl: "img/vermelho.png", iconSize: [32, 32], iconAnchor: [16, 32], popupAnchor: [0, -32] }),
    show: L.icon({ iconUrl: "img/amarelo.png", iconSize: [32, 32], iconAnchor: [16, 32], popupAnchor: [0, -32] }),
    evento: L.icon({ iconUrl: "img/azul.png", iconSize: [32, 32], iconAnchor: [16, 32], popupAnchor: [0, -32] })
};

var locais = [];

// carregar JSON
fetch("database/database.json")
    .then(r => {
        window.lastDatabaseUpdate = r.headers.get('Last-Modified');
        return r.json();
    })
    .then(data => {
        locais = data;
        popularCidades();
        render();

        if (markerLayer.getLayers().length > 0) {
            map.fitBounds(markerLayer.getBounds().pad(0.1));
        }
    });

// cidades
function popularCidades() {
    let cidades = [...new Set(locais.map(l => l.cidade))];
    cidades.forEach(c => {
        let o = document.createElement("option");
        o.value = c;
        o.textContent = c;
        cidadeFiltro.appendChild(o);
    });
}

// calcular dias
function diasRestantes(data) {
    let hoje = new Date();

    // 🔥 cria data LOCAL (corrige bug)
    let partes = data.split("-");
    let evento = new Date(partes[0], partes[1] - 1, partes[2]);

    hoje.setHours(0, 0, 0, 0);
    evento.setHours(0, 0, 0, 0);

    return Math.ceil((evento - hoje) / 86400000);
}

// badge
function badgeData(data) {
    if (!data) return "";

    let dias = diasRestantes(data);

    if (dias === 0) {
        return `<span style="font-size: 10px; background-color: darkgreen;color:#fff; text-align: center;font-weight:bold; padding: 5px; margin-top: 10px; display: block;  width: 90%;border-radius: 5px;" class="animate__animated animate__tada animate__delay-4s animate__infinite	animate__repeat-2">É HOJE</span>`;
    }

    if (dias > 0) {
        if (dias === 1) {
            return `<span style="color:orange;font-size:10px;">Falta 1 dia</span>`;
        } else {
            return `<span style="color:orange;font-size:10px;">Faltam ${dias} dias</span>`;
        }
    }

    if (dias < 0) {
        return `<span style="color:#777;font-size:11px;">ENCERRADO</span>`;
    }

    return "";
}

// filtros
function filtros() {
    let nome = busca.value.toLowerCase();
    let cidade = cidadeFiltro.value;
    let tipos = [...document.querySelectorAll("input[type=checkbox]:checked")].map(c => c.value);
    let di = dataInicio.value;
    let df = dataFim.value;

    return locais.filter(l => {
        // Se o evento tem data e ela já passou, não exibe (tira da lista e do mapa)
        if (l.data && diasRestantes(l.data) < 0) return false;

        if (nome && !(
            (l.nome && l.nome.toLowerCase().includes(nome)) ||
            (l.local && l.local.toLowerCase().includes(nome)) ||
            (l.endereco && l.endereco.toLowerCase().includes(nome))
        )) return false;
        if (cidade != "todas" && l.cidade != cidade) return false;
        if (!tipos.includes(l.tipo)) return false;

        if ((di || df) && l.data) {
            if (di && l.data < di) return false;
            if (df && l.data > df) return false;
        }

        if ((di || df) && !l.data) return false;

        return true;
    });
}

//extrair instagram da url e colocar no popup

function extrairInstagram(url) {
    if (!url) return "";

    try {
        let partes = url.split("/");
        let usuario = partes.filter(p => p.trim() !== "").pop();
        return usuario ? "@" + usuario : "";
    } catch {
        return "";
    }
}

function formatarWhatsAppLink(numero) {
    if (!numero) return "";
    let num = numero.replace(/\D/g, '');
    if (num.length >= 10 && !num.startsWith('55')) {
        num = '55' + num;
    }
    return `https://wa.me/${num}`;
}

function formatarWhatsAppExibicao(numero) {
    if (!numero) return "";
    let num = numero.replace(/\D/g, '');
    if (num.length === 11) {
        return `(${num.substring(0, 2)})${num.substring(2, 7)}.${num.substring(7)}`;
    } else if (num.length === 10) {
        return `(${num.substring(0, 2)})${num.substring(2, 6)}.${num.substring(6)}`;
    }
    return numero;
}

// render
function render() {
    verificarFiltrosAtivos();
    markerLayer.clearLayers();
    lista.innerHTML = "";

    let filtrados = filtros();

    filtrados.sort((a, b) => {
        if (!a.data && !b.data) return 0;
        if (!a.data) return 1;
        if (!b.data) return -1;
        return new Date(a.data) - new Date(b.data);
    });

    filtrados.forEach(p => {
        let dias = p.data ? diasRestantes(p.data) : null;

        let classe = "";
        if (dias === 0) classe = "hoje";
        else if (dias > 0 && dias <= 7) classe = "proximo";
        else if (dias < 0) classe = "passado";

        let dataFormatada = p.data ? p.data.split('-').reverse().join('/') : "";

        let popup = `
                    <div style="width:250px"> <!-- LARGURA DO POPUP-->
                    ${p.foto ? `
                    <a href="${p.foto}" target="_blank">
                        <img alt="${p.nome}" src="${p.foto}" style="width:100%;border-radius:8px;margin-bottom:6px;cursor:pointer">
                    </a>
                    ` : ""}
                    <b>${badgeData(p.data)}</b>
                    <h2>${p.nome}</h2>
                    <!--<b>Cidade:</b> ${p.cidade}<br>-->
                    
                    ${p.descricao}<br>
                    ${p.local ? `<b>Local:</b> ${p.local}<br>` : ""}
                    ${p.endereco ? `<b>Endereço:</b> ${p.endereco}<br>` : ""}

                    ${p.data ? `📅 ${dataFormatada} ${p.horario ? ` às ${p.horario}` : ""} <br>` : ""}

                    ${p.whatsapp && p.whatsapp.trim() !== "" ? `<img alt="WhatsApp logo" src="img/whatsapp_logo.png" style="width:16px;height:16px;">WhatsApp: <a target="_blank" href="${formatarWhatsAppLink(p.whatsapp)}">${formatarWhatsAppExibicao(p.whatsapp)}</a><br>` : ""}

                    ${p.instagram ? `
                    <img alt="Instagram logo" src="img/instagram_logo.png" style="width:16px;height:16px;">
                    Instagram: <a target="_blank" href="${p.instagram}">${extrairInstagram(p.instagram)}</a><br>
                    ` : ""}

                    ${p.linkingresso ? `<a target="_blank" href="${p.linkingresso}" style="display:block;background:orange;color:#fff;padding:5px;border-radius:5px;text-decoration:none;margin:10px;font-weight:bold;width:100\%;text-align:center;box-sizing:border-box">Comprar Ingresso</a>` : ""}
                    
                    <a target="_blank" href="https://www.google.com/maps/dir/?api=1&destination=${p.lat},${p.lng}">
                    <img alt="Google Maps logo" src="img/google_maps.svg" style="width:16px;height:16px;"> Abrir no Google Maps
                    </a>
                    </div>
                    `;

        let m = L.marker([p.lat, p.lng], { icon: icones[p.tipo] }).bindPopup(popup);

        // Centralizar o mapa deslocando a visão um pouco para cima (para focar no pop-up em si)
        m.on('click', function (e) {
            let px = map.project([p.lat, p.lng], 16);
            px.y -= 120; // offset (em pixels) para compensar a altura do popup
            map.setView(map.unproject(px, 16), 16);
        });

        markerLayer.addLayer(m);

        let div = document.createElement("div");
        div.className = "item " + classe;
        div.style.display = "flex";
        div.style.alignItems = "center";
        div.style.gap = "12px";

        let infoFotoLista = p.foto ? `<img alt="${p.nome}" src="${p.foto}" style="width:50px;height:50px;border-radius:8px;object-fit:cover;flex-shrink:0;">` : "";
        let infoDataLista = p.data ? `📅 ${dataFormatada} ${p.horario ? ` às ${p.horario}` : ""}<br>` : "";

        div.innerHTML = `
                    ${infoFotoLista}
                    <div style="flex-grow:1; font-size:14px;">
                        <b>${p.nome}</b><br>
                        ${p.cidade}${p.local ? ` - ${p.local}` : ""}<br>
                        ${infoDataLista}
                        ${p.data ? badgeData(p.data) : ""}
                    </div>
                `;

        div.onclick = () => {
            if (window.innerWidth < 768) {
                sidebar.classList.remove("ativo");
                menuBtn.innerHTML = "☰";
            }
            setTimeout(() => {
                let px = map.project([p.lat, p.lng], 16);
                px.y -= 120; // offset vertical para o popup ficar no meio
                map.setView(map.unproject(px, 16), 16);
                m.openPopup();
            }, 300); // dá um tempinho caso o menu mobile recolha e altere a dimensão da tela
        };

        lista.appendChild(div);
    });
}

// eventos
const clearSearchBtn = document.getElementById('clearSearch');

busca.oninput = () => {
    clearSearchBtn.style.display = busca.value ? 'block' : 'none';
    render();
};

clearSearchBtn.onclick = () => {
    busca.value = '';
    clearSearchBtn.style.display = 'none';
    render();
};

cidadeFiltro.onchange = render;
document.querySelectorAll("input[type=checkbox]").forEach(c => c.onchange = render);
dataInicio.onchange = render;
dataFim.onchange = render;

// Lógica para o botão de limpar filtros
function verificarFiltrosAtivos() {
    const btnLimpar = document.getElementById('btnLimparFiltros');
    if (!btnLimpar) return;

    const checkboxes = document.querySelectorAll("input[type=checkbox]");
    const allChecked = Array.from(checkboxes).every(c => c.checked);

    const isFiltered = busca.value !== "" ||
        cidadeFiltro.value !== "todas" ||
        !allChecked ||
        dataInicio.value !== "" ||
        dataFim.value !== "";

    btnLimpar.style.display = isFiltered ? 'block' : 'none';
}

document.getElementById('btnLimparFiltros').onclick = () => {
    busca.value = '';
    clearSearchBtn.style.display = 'none';
    cidadeFiltro.value = 'todas';
    document.querySelectorAll("input[type=checkbox]").forEach(c => c.checked = true);
    dataInicio.value = '';
    dataFim.value = '';
    render();
};



// =========================
// 🌍 CONTADOR DE VISITAS
// =========================
function atualizarContadorVisitas() {
    const spanVisitas = document.getElementById('contador-visitas');
    if (!spanVisitas) return;

    if (window.visitCount !== undefined) {
        spanVisitas.innerText = window.visitCount;
    } else {
        fetch('https://api.counterapi.dev/v1/agenda-metal-ceara/visitantes/up')
            .then(response => response.json())
            .then(data => {
                window.visitCount = data.count;
                spanVisitas.innerText = window.visitCount;
            })
            .catch(error => {
                console.error('Erro ao buscar visitas:', error);
                spanVisitas.innerText = 'Indisponível';
            });
    }
}

// Inicializa o contador ao carregar o script
atualizarContadorVisitas();

//GEOLOCALIZAÇÃO DO USUÁRIO
// SCRIPT PARA O BOTÃO DE LOCALIZAÇÃO DO DISPOSITIVO

var marcadorUsuario = null;
var circuloUsuario = null;

document.getElementById("btnLocalizacao").onclick = function () {
    var btn = this;

    if (!navigator.geolocation) {
        alert("Geolocalização não suportada pelo seu navegador.");
        return;
    }

    btn.innerHTML = "⏳";
    btn.disabled = true;

    navigator.geolocation.getCurrentPosition(
        function (pos) {
            var lat = pos.coords.latitude;
            var lng = pos.coords.longitude;
            var acc = pos.coords.accuracy;

            if (marcadorUsuario) {
                map.removeLayer(marcadorUsuario);
                map.removeLayer(circuloUsuario);
            }

            var iconeUsuario = L.divIcon({
                className: "",
                html: '<div style="width:16px;height:16px;background:#3498db;border:3px solid #fff;border-radius:50%;box-shadow:0 0 6px rgba(52,152,219,0.8)"></div>',
                iconSize: [16, 16],
                iconAnchor: [8, 8]
            });

            circuloUsuario = L.circle([lat, lng], {
                radius: acc,
                color: "#3498db",
                fillColor: "#3498db",
                fillOpacity: 0.1,
                weight: 1
            }).addTo(map);

            marcadorUsuario = L.marker([lat, lng], { icon: iconeUsuario })
                .bindPopup("<b>Você está aqui</b><br>Precisão: ~" + Math.round(acc) + "m")
                .addTo(map);

            map.setView([lat, lng], 14);
            marcadorUsuario.openPopup();

            btn.innerHTML = "<img alt='Localização' src='img/location.svg' width='34px' height='34px'>";
            btn.disabled = false;
            btn.classList.add("ativo");
        },
        function (err) {
            var msgs = {
                1: "Permissão de localização negada. Verifique se o site está em HTTPS e permita a localização no navegador.",
                2: "Localização indisponível.",
                3: "Tempo esgotado ao obter localização."
            };
            alert(msgs[err.code] || "Erro ao obter localização.");
            btn.innerHTML = "<img alt='Localização' src='img/location.svg' width='34px' height='34px'>";
            btn.disabled = false;
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
};