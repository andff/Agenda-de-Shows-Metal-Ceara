import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, webbrowser
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
from datetime import datetime
from tkcalendar import DateEntry

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(BASE_DIR, "database.json")

PASTA_IMAGENS = os.path.join(BASE_DIR, "imagens")
os.makedirs(PASTA_IMAGENS, exist_ok=True)

def carregar():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

dados = carregar()

root = tk.Tk()
root.title("Gerenciador de Pontos no Mapa")
root.geometry("1400x700")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
    background="#2b2b2b",
    foreground="white",
    fieldbackground="#2b2b2b"
)
style.map('Treeview', background=[('selected', '#347083')])

# ---------- LAYOUT ----------
top_frame = tk.Frame(root, bg="#1e1e1e")
top_frame.pack(fill="x")

center_frame = tk.Frame(root)
center_frame.pack(fill="both", expand=True)

bottom_frame = tk.Frame(root, bg="#1e1e1e")
bottom_frame.pack(fill="x")

# ---------- TOPO ----------
tk.Label(top_frame, text="Buscar:", fg="white", bg="#1e1e1e").pack(side="left")
busca = tk.Entry(top_frame)
busca.pack(side="left", padx=5)

tk.Label(top_frame, text="Tipo:", fg="white", bg="#1e1e1e").pack(side="left")
filtro_tipo = ttk.Combobox(top_frame, values=["Todos","bar","show","evento"])
filtro_tipo.set("Todos")
filtro_tipo.pack(side="left", padx=5)

stats_label = tk.Label(top_frame, fg="white", bg="#1e1e1e")
stats_label.pack(side="right", padx=10)

# ---------- TABELA ----------
cols = ["nome","tipo","cidade","lat","lng","descricao","telefone","instagram","data","horario","linkingresso","foto"]

frame_tabela = tk.Frame(center_frame)
frame_tabela.pack(fill="both", expand=True)

scroll_y = tk.Scrollbar(frame_tabela, orient="vertical")
scroll_x = tk.Scrollbar(frame_tabela, orient="horizontal")

tabela = ttk.Treeview(
    frame_tabela,
    columns=cols,
    show="headings",
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

scroll_y.config(command=tabela.yview)
scroll_x.config(command=tabela.xview)

scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")
tabela.pack(fill="both", expand=True)

def ordenar_coluna(col, reverse):
    lista = [(tabela.set(k, col), k) for k in tabela.get_children('')]
    try:
        lista.sort(key=lambda x: float(x[0]), reverse=reverse)
    except:
        lista.sort(reverse=reverse)
    for index, (val, k) in enumerate(lista):
        tabela.move(k, '', index)
    tabela.heading(col, command=lambda: ordenar_coluna(col, not reverse))

for c in cols:
    tabela.heading(c, text=c.upper(), command=lambda _c=c: ordenar_coluna(_c, False))
    tabela.column(c, width=120)

# ---------- FORM ----------
frame_form = tk.Frame(bottom_frame, height=180, bg="#1e1e1e")
frame_form.pack(fill="x")
frame_form.pack_propagate(False)

campos = {}

for i,n in enumerate(cols):
    tk.Label(frame_form,text=n, fg="white", bg="#1e1e1e").grid(row=i//6*2,column=i%6)
    
    if n == "data":
        e = DateEntry(frame_form, date_pattern='yyyy-mm-dd')
    else:
        e = tk.Entry(frame_form,width=20)

    e.grid(row=i//6*2+1,column=i%6,padx=2)
    campos[n]=e

# ---------- IMAGEM ----------
img_label = tk.Label(bottom_frame, bg="#1e1e1e")
img_label.pack()

def mostrar_imagem(url):
    if not url: return
    try:
        if os.path.exists(url):
            raw = open(url, "rb").read()
        else:
            raw = urlopen(url).read()

        im = Image.open(io.BytesIO(raw))
        im = im.resize((100,100))
        foto = ImageTk.PhotoImage(im)

        img_label.config(image=foto)
        img_label.image=foto
    except:
        img_label.config(image="")

def abrir_imagem_grande(event):
    if not hasattr(img_label, "image"):
        return
    top = tk.Toplevel()
    top.title("Imagem")
    lbl = tk.Label(top)
    lbl.pack()
    lbl.config(image=img_label.image)
    lbl.image = img_label.image

img_label.bind("<Button-1>", abrir_imagem_grande)

# ---------- FUNÇÕES ----------
def atualizar():
    tabela.delete(*tabela.get_children())

    termo = busca.get().lower()
    tipo = filtro_tipo.get()

    tipos = {}

    for i,item in enumerate(dados):

        if termo and termo not in str(item).lower():
            continue
        if tipo!="Todos" and item.get("tipo")!=tipo:
            continue

        valores = [item.get(c,"") for c in cols]
        tabela.insert("", "end", iid=i, values=valores)

        t = item.get("tipo","outro")
        tipos[t] = tipos.get(t,0)+1

    stats = f"Total: {len(dados)} | " + " | ".join([f"{k}:{v}" for k,v in tipos.items()])
    stats_label.config(text=stats)

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

def upload_imagem():
    file = filedialog.askopenfilename(filetypes=[("Imagens","*.png *.jpg *.jpeg")])
    if not file: return

    nome = os.path.basename(file)
    destino = os.path.join(PASTA_IMAGENS, nome)

    with open(file, "rb") as f:
        with open(destino, "wb") as d:
            d.write(f.read())

    campos["foto"].delete(0,"end")
    campos["foto"].insert(0, destino)

    mostrar_imagem(destino)

# ---------- BOTÕES ----------
frame_botoes = tk.Frame(bottom_frame, bg="#1e1e1e")
frame_botoes.pack()

tk.Button(frame_botoes,text="Novo",width=15,command=novo).pack(side="left", padx=5)
tk.Button(frame_botoes,text="Salvar",width=15,command=salvar_reg).pack(side="left", padx=5)
tk.Button(frame_botoes,text="Excluir",width=15,command=excluir).pack(side="left", padx=5)
tk.Button(frame_botoes,text="Abrir no Maps",width=15,command=abrir_maps).pack(side="left", padx=5)
tk.Button(frame_botoes,text="Upload Imagem",width=15,command=upload_imagem).pack(side="left", padx=5)

# ---------- EVENTOS ----------
tabela.bind("<<TreeviewSelect>>", selecionar)
busca.bind("<KeyRelease>", lambda e: atualizar())
filtro_tipo.bind("<<ComboboxSelected>>", lambda e: atualizar())

# ---------- START ----------
atualizar()
root.mainloop()