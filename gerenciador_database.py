import tkinter as tk
from tkinter import ttk, messagebox
import json, os, webbrowser
from urllib.request import urlopen
from PIL import Image, ImageTk
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(BASE_DIR, "database.json")

# ---------- JSON ----------

def carregar():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

# ---------- DADOS ----------

dados = carregar()

# ---------- GUI ----------

root = tk.Tk()
root.title("Gerenciador PRO de Pontos")
root.geometry("1100x600")

# ---------- TOPO ----------

top = tk.Frame(root)
top.pack(fill="x")

tk.Label(top, text="Buscar:").pack(side="left")
busca = tk.Entry(top)
busca.pack(side="left", padx=5)

tk.Label(top, text="Tipo:").pack(side="left")
filtro_tipo = ttk.Combobox(top, values=["Todos","bar","show"])
filtro_tipo.set("Todos")
filtro_tipo.pack(side="left", padx=5)

# ---------- TABELA ----------

cols = ("nome","tipo","cidade","lat","lng")
tabela = ttk.Treeview(root, columns=cols, show="headings")
for c in cols:
    tabela.heading(c, text=c.upper())
    tabela.column(c, width=120)

tabela.pack(fill="both", expand=True)

# ---------- FORM ----------

form = tk.Frame(root)
form.pack(fill="x", pady=5)

campos_nomes = ["nome","tipo","cidade","lat","lng","descricao","telefone","instagram","data","horario","linkingresso","foto"]
campos = {}

for i,n in enumerate(campos_nomes):
    tk.Label(form,text=n).grid(row=i//5*2,column=i%5)
    e = tk.Entry(form,width=22)
    e.grid(row=i//5*2+1,column=i%5,padx=2)
    campos[n]=e

# ---------- PREVIEW IMAGEM ----------

img_label = tk.Label(root)
img_label.pack()

def mostrar_imagem(url):
    if not url: return
    try:
        raw = urlopen(url).read()
        im = Image.open(io.BytesIO(raw))
        im.thumbnail((250,250))
        foto = ImageTk.PhotoImage(im)
        img_label.config(image=foto)
        img_label.image=foto
    except:
        img_label.config(image="")

# ---------- FUNÇÕES ----------

def atualizar():
    tabela.delete(*tabela.get_children())

    termo = busca.get().lower()
    tipo = filtro_tipo.get()

    for i,item in enumerate(dados):

        if termo and termo not in str(item).lower():
            continue
        if tipo!="Todos" and item.get("tipo")!=tipo:
            continue

        tabela.insert("", "end", iid=i, values=(
            item.get("nome"),
            item.get("tipo"),
            item.get("cidade"),
            item.get("lat"),
            item.get("lng")
        ))

def selecionar(e):
    if not tabela.selection(): return
    idx = int(tabela.selection()[0])
    item = dados[idx]

    for k in campos:
        campos[k].delete(0,"end")
        if k in item:
            campos[k].insert(0,item[k])

    mostrar_imagem(item.get("foto"))

def novo():
    tabela.selection_remove(*tabela.selection())
    for c in campos.values():
        c.delete(0,"end")
    img_label.config(image="")

def salvar_reg():
    reg={}
    for k,e in campos.items():
        v=e.get().strip()
        if v: reg[k]=v

    try:
        if "lat" in reg: reg["lat"]=float(reg["lat"])
        if "lng" in reg: reg["lng"]=float(reg["lng"])
    except:
        messagebox.showerror("Erro","Lat/Lng inválidos")
        return

    if tabela.selection():
        dados[int(tabela.selection()[0])] = reg
    else:
        dados.append(reg)

    salvar()
    atualizar()

def excluir():
    if not tabela.selection(): return
    del dados[int(tabela.selection()[0])]
    salvar()
    atualizar()
    novo()

def abrir_maps():
    if not tabela.selection(): return
    item = dados[int(tabela.selection()[0])]
    if "lat" in item and "lng" in item:
        url=f"https://www.google.com/maps?q={item['lat']},{item['lng']}"
        webbrowser.open(url)

# ---------- BOTÕES ----------

botoes = tk.Frame(root)
botoes.pack(pady=5)

tk.Button(botoes,text="Novo",width=15,command=novo).grid(row=0,column=0,padx=5)
tk.Button(botoes,text="Salvar",width=15,command=salvar_reg).grid(row=0,column=1,padx=5)
tk.Button(botoes,text="Excluir",width=15,command=excluir).grid(row=0,column=2,padx=5)
tk.Button(botoes,text="Abrir no Maps",width=15,command=abrir_maps).grid(row=0,column=3,padx=5)

# ---------- EVENTOS ----------

tabela.bind("<<TreeviewSelect>>", selecionar)
busca.bind("<KeyRelease>", lambda e: atualizar())
filtro_tipo.bind("<<ComboboxSelected>>", lambda e: atualizar())

# ---------- START ----------

atualizar()
root.mainloop()