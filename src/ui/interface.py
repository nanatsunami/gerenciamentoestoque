import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

from src.core.lista_produtos import ListaProdutos
from src.core.fila_criticos import FilaCriticos
from src.service.estoque_service import EstoqueService

# ===== INICIALIZAÇÃO =====

lista = ListaProdutos()
fila = FilaCriticos()
service = EstoqueService(lista, fila)

service.carregar_de_arquivo()

# ===== FUNÇÕES =====

def mostrar_lista():
    frame_cadastro.pack_forget()
    frame_lista.pack()
    atualizar_lista()

def mostrar_cadastro():
    frame_lista.pack_forget()
    frame_cadastro.pack()

def toggle_validade():
    if perecivel_var.get():
        frame_validade.pack()
    else:
        frame_validade.pack_forget()

def atualizar_lista():
    lista_box.delete(0, tk.END)

    produtos = lista.exibir()
    criterio = dropdown_var.get()
    busca = entry_busca.get().lower()

    # 🔍 FILTRO POR NOME
    if busca:
        produtos = [p for p in produtos if busca in p["nome"].lower()]

    # 🔽 ORDENAÇÃO (COM FALLBACK)
    if criterio == "Quantidade":
        produtos = sorted(produtos, key=lambda x: x["quantidade"])

    elif criterio == "Valor (mais barato)":
        produtos = sorted(produtos, key=lambda x: x.get("preco", x.get("valor", 0)))

    elif criterio == "Valor (mais caro)":
        produtos = sorted(produtos, key=lambda x: x.get("preco", x.get("valor", 0)), reverse=True)

    elif criterio == "Data (mais antigo)":
        produtos = sorted(produtos, key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y"))

    elif criterio == "Data (mais recente)":
        produtos = sorted(produtos, key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y"), reverse=True)

    # 🧠 EXIBIÇÃO (COM FALLBACK)
    for p in produtos:
        prioridade = service.calcular_prioridade(p)

        custo = p.get("custo", p.get("valor", 0))
        preco = p.get("preco", custo * 1.5)

        texto = (
            f"{p['nome']} | Qtd: {p['quantidade']} | "
            f"Custo: R$ {custo:.2f} | Venda: R$ {preco:.2f} | "
            f"{p['data']} | Prioridade: {int(prioridade)}"
        )

        lista_box.insert(tk.END, texto)

def cadastrar():
    nome = entry_nome.get()
    qtd = entry_qtd.get()
    custo = entry_custo.get()
    preco = entry_preco.get()
    data = entry_data.get()

    if not nome or not qtd or not custo or not preco or not data:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return

    produto = {
        "nome": nome,
        "quantidade": int(qtd),
        "custo": float(custo),
        "preco": float(preco),
        "data": data
    }

    if perecivel_var.get():
        produto["validade"] = entry_validade.get()

    lista.inserir(produto)
    service.salvar_em_arquivo()

    messagebox.showinfo("Sucesso", "Produto cadastrado!")

    limpar_campos()
    mostrar_lista()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)
    entry_custo.delete(0, tk.END)
    entry_preco.delete(0, tk.END)

# ===== JANELA =====

root = tk.Tk()
root.title("Sistema de Estoque")
root.geometry("600x500")

# ===== FRAME LISTA =====

frame_lista = tk.Frame(root)

tk.Label(frame_lista, text="Produtos em Estoque", font=("Arial", 14)).pack()

# 🔍 BUSCA
tk.Label(frame_lista, text="Buscar por nome:").pack()
entry_busca = tk.Entry(frame_lista)
entry_busca.pack()

tk.Button(frame_lista, text="Buscar", command=atualizar_lista).pack()

# 🔽 DROPDOWN
dropdown_var = tk.StringVar(value="Quantidade")

dropdown = tk.OptionMenu(
    frame_lista,
    dropdown_var,
    "Quantidade",
    "Valor (mais barato)",
    "Valor (mais caro)",
    "Data (mais antigo)",
    "Data (mais recente)"
)
dropdown.pack()

tk.Button(frame_lista, text="Ordenar", command=atualizar_lista).pack()

# 📋 LISTA
lista_box = tk.Listbox(frame_lista, width=80)
lista_box.pack()

tk.Button(frame_lista, text="Cadastrar Novo Produto", command=mostrar_cadastro).pack()

# ===== FRAME CADASTRO =====

frame_cadastro = tk.Frame(root)

tk.Label(frame_cadastro, text="Cadastro de Produto", font=("Arial", 14)).pack()

tk.Label(frame_cadastro, text="Nome").pack()
entry_nome = tk.Entry(frame_cadastro)
entry_nome.pack()

tk.Label(frame_cadastro, text="Quantidade").pack()
entry_qtd = tk.Entry(frame_cadastro)
entry_qtd.pack()

tk.Label(frame_cadastro, text="Custo (R$)").pack()
entry_custo = tk.Entry(frame_cadastro)
entry_custo.pack()

tk.Label(frame_cadastro, text="Preço de Venda (R$)").pack()
entry_preco = tk.Entry(frame_cadastro)
entry_preco.pack()

tk.Label(frame_cadastro, text="Data de Entrada").pack()
entry_data = DateEntry(frame_cadastro, date_pattern="dd/mm/yyyy")
entry_data.pack()

# ✅ CHECKBOX
perecivel_var = tk.BooleanVar()

tk.Checkbutton(
    frame_cadastro,
    text="Produto perecível?",
    variable=perecivel_var,
    command=toggle_validade
).pack()

# 📅 VALIDADE
frame_validade = tk.Frame(frame_cadastro)

tk.Label(frame_validade, text="Data de Validade").pack()
entry_validade = DateEntry(frame_validade, date_pattern="dd/mm/yyyy")
entry_validade.pack()

# BOTÕES
tk.Button(frame_cadastro, text="Salvar", command=cadastrar).pack()
tk.Button(frame_cadastro, text="Voltar", command=mostrar_lista).pack()

# ===== INÍCIO =====

mostrar_lista()

root.mainloop()