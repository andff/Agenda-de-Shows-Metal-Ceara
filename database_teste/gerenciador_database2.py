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
root.title("FortalRolePlay - Gerenciador do database.json")
root.geometry("1100x600")

# ---------- TOPO ----------

top = tk.Frame(root)
top.pack(fill="x")

tk.Label(top, text="Buscar:").pack(side="left")
busca = tk.Entry(top)
busca.pack(side="left", padx=5)

tk.Label(top, text="cat:").pack(side="left")
filtro_cat = ttk.Combobox(top, values=["Todos","bar","show"])
filtro_cat.set("Todos")
filtro_cat.pack(side="left", padx=5)

# ---------- TABELA ----------

cols = ("name","desc","cat","color","lat","lon")
tabela = ttk.Treeview(root, columns=cols, show="headings")
for c in cols:
    tabela.heading(c, text=c.upper())
    tabela.column(c, width=120)

tabela.pack(fill="both", expand=True)

# ---------- FORM ----------

form = tk.Frame(root)
form.pack(fill="x", pady=5)

campos_names = ["name","desc","cat","color","lat","lon"]
campos = {}

for i, n in enumerate(campos_names):
    tk.Label(form, text=n).grid(row=0, column=i, padx=5, pady=2)

    e = tk.Entry(form, width=18)
    e.grid(row=1, column=i, padx=5, pady=2)

    campos[n] = e

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
    cat = filtro_cat.get()

    for i,item in enumerate(dados):

        if termo and termo not in str(item).lower():
            continue
        if cat!="Todos" and item.get("cat")!=cat:
            continue

        tabela.insert("", "end", iid=i, values=(
            item.get("name"),
            item.get("desc"),
            item.get("cat"),
            item.get("color"),
            item.get("lat"),
            item.get("lon")
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
        if "lon" in reg: reg["lon"]=float(reg["lon"])
    except:
        messagebox.showerror("Erro","Lat/lon inválidos")
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
    if "lat" in item and "lon" in item:
        url=f"https://www.google.com/maps?q={item['lat']},{item['lon']}"
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
filtro_cat.bind("<<ComboboxSelected>>", lambda e: atualizar())

# ---------- START ----------

atualizar()
root.mainloop()