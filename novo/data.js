// ═══════════════════════════════════════════════════════════════
//  FORTALEZA NIGHT — BASE DE DADOS
//  Edite este arquivo para adicionar/remover locais.
//
//  CAMPOS:
//    id        : número único (não repita)
//    nome      : nome do local
//    categoria : 'Show' | 'Bar' | 'Balada' | 'Gastrobar' | 'Roof/Lounge' | 'Festival'
//    endereco  : endereço completo
//    bairro    : bairro
//    instagram : @handle (ou "" se não tiver)
//    lat / lng : coordenadas GPS
//    dia_evento: texto livre — ex: "Sábados a partir das 22h"
// ═══════════════════════════════════════════════════════════════

const PLACES = [

  // ── SHOWS ──────────────────────────────────────────────────
  {
    id: 1,
    nome: "Centro Dragão do Mar",
    categoria: "Show",
    endereco: "Rua Dragão do Mar, 81 — Praia de Iracema",
    bairro: "Praia de Iracema",
    instagram: "@dragaodomar",
    lat: -3.7196,
    lng: -38.5317,
    dia_evento: "Programação variada — consulte o site"
  },
  {
    id: 2,
    nome: "Teatro Via Sul",
    categoria: "Show",
    endereco: "Av. Washington Soares, 4335 — Edson Queiroz",
    bairro: "Edson Queiroz",
    instagram: "@teatroviasul",
    lat: -3.7789,
    lng: -38.4710,
    dia_evento: "Sextas e Sábados — 20h"
  },
  {
    id: 3,
    nome: "O Plenário",
    categoria: "Show",
    endereco: "Av. Abolição, 2400 — Meireles",
    bairro: "Meireles",
    instagram: "@oplenario",
    lat: -3.7248,
    lng: -38.4970,
    dia_evento: "Sábados — 19h às 02h"
  },

  // ── BARES ─────────────────────────────────────────────────
  {
    id: 4,
    nome: "Bar do Gerson",
    categoria: "Bar",
    endereco: "Rua Osvaldo Cruz, 1 — Praia de Iracema",
    bairro: "Praia de Iracema",
    instagram: "@bardogerson_fortaleza",
    lat: -3.7202,
    lng: -38.5296,
    dia_evento: "Ter–Dom a partir das 18h"
  },
  {
    id: 5,
    nome: "Órbita Bar",
    categoria: "Bar",
    endereco: "Rua dos Pacajus, 20 — Praia de Iracema",
    bairro: "Praia de Iracema",
    instagram: "@orbitabar",
    lat: -3.7212,
    lng: -38.5280,
    dia_evento: "Qui–Dom a partir das 20h"
  },
  {
    id: 6,
    nome: "Chopperia Atlântico",
    categoria: "Bar",
    endereco: "Av. Beira Mar, 3500 — Meireles",
    bairro: "Meireles",
    instagram: "@chopperia.atlantico",
    lat: -3.7268,
    lng: -38.5065,
    dia_evento: "Todos os dias — 11h às 01h"
  },
  {
    id: 7,
    nome: "Adega Portuguesa",
    categoria: "Bar",
    endereco: "Rua Pereira Valente, 550 — Meireles",
    bairro: "Meireles",
    instagram: "@adegaportuguesafortaleza",
    lat: -3.7310,
    lng: -38.5010,
    dia_evento: "Seg–Sáb — 18h às 02h"
  },

  // ── BALADAS ────────────────────────────────────────────────
  {
    id: 8,
    nome: "Carioca Club",
    categoria: "Balada",
    endereco: "Av. Dom Luís, 1000 — Aldeota",
    bairro: "Aldeota",
    instagram: "@cariocaclubfor",
    lat: -3.7368,
    lng: -38.5082,
    dia_evento: "Sex e Sáb — 23h às 06h"
  },
  {
    id: 9,
    nome: "Maison de España",
    categoria: "Balada",
    endereco: "Rua Leonardo Mota, 800 — Meireles",
    bairro: "Meireles",
    instagram: "@maisondespana",
    lat: -3.7322,
    lng: -38.5025,
    dia_evento: "Sábados — 22h às 05h"
  },

  // ── GASTROBARES ────────────────────────────────────────────
  {
    id: 10,
    nome: "Tábua de Carne",
    categoria: "Gastrobar",
    endereco: "Av. Heráclito Graça, 230 — Centro",
    bairro: "Centro",
    instagram: "@tabuadecarne",
    lat: -3.7285,
    lng: -38.5345,
    dia_evento: "Seg–Sáb — 12h às 23h"
  },
  {
    id: 11,
    nome: "Botequim Glamouroso",
    categoria: "Gastrobar",
    endereco: "Rua Silva Paulet, 1234 — Aldeota",
    bairro: "Aldeota",
    instagram: "@botequimglamouroso",
    lat: -3.7352,
    lng: -38.5097,
    dia_evento: "Ter–Dom — 18h às 01h"
  },

  // ── ROOF / LOUNGE ──────────────────────────────────────────
  {
    id: 12,
    nome: "Rooftop Mucuripe",
    categoria: "Roof/Lounge",
    endereco: "Av. Historiador Raimundo Girão, 1500 — Mucuripe",
    bairro: "Mucuripe",
    instagram: "@rooftopmucuripe",
    lat: -3.7196,
    lng: -38.4750,
    dia_evento: "Sex e Sáb — 19h às 02h"
  },
  {
    id: 13,
    nome: "Sky Lounge Meireles",
    categoria: "Roof/Lounge",
    endereco: "Av. Beira Mar, 2600 — Meireles",
    bairro: "Meireles",
    instagram: "@skyloungemeireles",
    lat: -3.7242,
    lng: -38.5013,
    dia_evento: "Qui–Dom — 20h às 03h"
  },

  // ── FESTIVAIS ──────────────────────────────────────────────
  {
    id: 14,
    nome: "Ateliê de Ideias",
    categoria: "Festival",
    endereco: "Rua Dragão do Mar, 207 — Praia de Iracema",
    bairro: "Praia de Iracema",
    instagram: "@ateliedeideias",
    lat: -3.7204,
    lng: -38.5308,
    dia_evento: "Programação mensal — siga o instagram"
  },
  {
    id: 15,
    nome: "Mercado dos Pinhões",
    categoria: "Festival",
    endereco: "Rua Senador Pompeu, 600 — Centro",
    bairro: "Centro",
    instagram: "@mercadodospinhoes",
    lat: -3.7270,
    lng: -38.5380,
    dia_evento: "Fins de semana — 09h às 22h"
  }

];
