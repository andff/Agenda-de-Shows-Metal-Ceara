import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, webbrowser, base64
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
from datetime import datetime
from tkcalendar import DateEntry

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

dados = carregar()

# ---------- GUI ----------

root = tk.Tk()
root.title("Gerenciador PRO de Pontos")
root.geometry("1400x700")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
    background="#2b2b2b",
    foreground="white",
    rowheight=25,
    fieldbackground="#2b2b2b"
)

style.map('Treeview', background=[('selected', '#347083')])

# ---------- TOPO ----------

top = tk.Frame(root, bg="#1e1e1e")
top.pack(fill="x")

tk.Label(top, text="Buscar:", fg="white", bg="#1e1e1e").pack(side="left")
busca = tk.Entry(top)
busca.pack(side="left", padx=5)

tk.Label(top, text="Tipo:", fg="white", bg="#1e1e1e").pack(side="left")
filtro_tipo = ttk.Combobox(top, values=["Todos","bar","show","evento"])
filtro_tipo.set("Todos")
filtro_tipo.pack(side="left", padx=5)

stats_label = tk.Label(top, fg="white", bg="#1e1e1e")
stats_label.pack(side="right", padx=10)

# ---------- TABELA (AGORA COM TODOS OS CAMPOS)

cols = ["nome","tipo","cidade","lat","lng","descricao","telefone","instagram","data","horario","linkingresso","foto"]

tabela = ttk.Treeview(root, columns=cols, show="headings")

for c in cols:
    tabela.heading(c, text=c.upper())
    tabela.column(c, width=120)

tabela.tag_configure("vencido", background="#5c1e1e")
tabela.tag_configure("hoje", background="#5c5c1e")

tabela.pack(fill="both", expand=True)

# ---------- FORM ----------

form = tk.Frame(root, bg="#1e1e1e")
form.pack(fill="x", pady=5)

campos = {}

for i,n in enumerate(cols):
    tk.Label(form,text=n, fg="white", bg="#1e1e1e").grid(row=i//6*2,column=i%6)
    
    if n == "data":
        e = DateEntry(form, date_pattern='yyyy-mm-dd')
    else:
        e = tk.Entry(form,width=20)

    e.grid(row=i//6*2+1,column=i%6,padx=2)
    campos[n]=e

# ---------- PREVIEW ----------

img_label = tk.Label(root, bg="#1e1e1e")
img_label.pack()

def mostrar_imagem(url):
    if not url: return
    try:
        if url.startswith("data:image"):
            base64_data = url.split(",")[1]
            raw = base64.b64decode(base64_data)
        else:
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
    hoje = datetime.now().date()

    total = len(dados)
    tipos = {}

    for i,item in enumerate(dados):

        if termo and termo not in str(item).lower():
            continue
        if tipo!="Todos" and item.get("tipo")!=tipo:
            continue

        valores = [item.get(c,"") for c in cols]

        tag = ""

        data_str = item.get("data")
        if data_str:
            try:
                data_evento = datetime.strptime(data_str, "%Y-%m-%d").date()

                if data_evento < hoje:
                    tag = "vencido"
                elif data_evento == hoje:
                    tag = "hoje"
            except:
                pass

        tabela.insert("", "end", iid=i, values=valores, tags=(tag,))

        t = item.get("tipo","outro")
        tipos[t] = tipos.get(t,0)+1

    stats = f"Total: {total} | " + " | ".join([f"{k}:{v}" for k,v in tipos.items()])
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

    with open(file, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    campos["foto"].delete(0,"end")
    campos["foto"].insert(0, f"data:image/jpeg;base64,{b64}")

    mostrar_imagem(campos["foto"].get())

# ---------- BOTÕES ----------

botoes = tk.Frame(root, bg="#1e1e1e")
botoes.pack(pady=5)

tk.Button(botoes,text="Novo",width=15,command=novo).grid(row=0,column=0,padx=5)
tk.Button(botoes,text="Salvar",width=15,command=salvar_reg).grid(row=0,column=1,padx=5)
tk.Button(botoes,text="Excluir",width=15,command=excluir).grid(row=0,column=2,padx=5)
tk.Button(botoes,text="Abrir no Maps",width=15,command=abrir_maps).grid(row=0,column=3,padx=5)
tk.Button(botoes,text="Upload Imagem",width=15,command=upload_imagem).grid(row=0,column=4,padx=5)

# ---------- EVENTOS ----------

tabela.bind("<<TreeviewSelect>>", selecionar)
busca.bind("<KeyRelease>", lambda e: atualizar())
filtro_tipo.bind("<<ComboboxSelected>>", lambda e: atualizar())

# ---------- START ----------

atualizar()
root.mainloop()