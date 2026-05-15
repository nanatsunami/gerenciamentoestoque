import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

from src.core.lista_produtos import ListaProdutos
from src.core.fila_criticos import FilaCriticos
from src.service.estoque_service import EstoqueService

# ===== INSTÂNCIAS =====

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

def atualizar_lista():
    lista_box.delete(0, tk.END)

    produtos = lista.exibir()
    criterio = dropdown_var.get()

    # calcular prioridade para todos
    for p in produtos:
        p["prioridade"] = service.calcular_prioridade(p)

    # ordenar
    if criterio == "Quantidade":
        produtos = sorted(produtos, key=lambda x: x["quantidade"])
    elif criterio == "Valor":
        produtos = sorted(produtos, key=lambda x: x["valor"])
    elif criterio == "Data":
        produtos = sorted(produtos, key=lambda x: x["data"])
    elif criterio == "Prioridade":
        produtos = sorted(produtos, key=lambda x: x["prioridade"], reverse=True)

    # exibir
    for p in produtos:
        texto = (
            f"{p['nome']} | Qtd: {p['quantidade']} | "
            f"R$ {p['valor']} | {p['data']} | "
            f"Prioridade: {int(p['prioridade'])}"
        )

        if "validade" in p:
            texto += f" | Val: {p['validade']}"

        lista_box.insert(tk.END, texto)

def toggle_validade():
    if perecivel_var.get():
        label_validade.pack()
        date_validade.pack()
    else:
        label_validade.pack_forget()
        date_validade.pack_forget()

def cadastrar():
    nome = entry_nome.get()
    qtd = entry_qtd.get()
    valor = entry_valor.get()
    data = entry_data.get()

    if not nome or not qtd or not valor:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return

    try:
        produto = {
            "nome": nome,
            "quantidade": int(qtd),
            "valor": float(valor),
            "data": data
        }

        if perecivel_var.get():
            produto["validade"] = date_validade.get()

        lista.inserir(produto)
        service.salvar_em_arquivo()

        messagebox.showinfo("Sucesso", "Produto cadastrado!")

        limpar_campos()
        mostrar_lista()

    except ValueError:
        messagebox.showerror("Erro", "Quantidade e valor devem ser numéricos")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)
    entry_valor.delete(0, tk.END)
    perecivel_var.set(False)
    toggle_validade()

def mostrar_criticos():
    lista_box.delete(0, tk.END)

    produtos = lista.exibir()

    for p in produtos:
        p["prioridade"] = service.calcular_prioridade(p)

    criticos = [p for p in produtos if p["prioridade"] > 100]

    for p in criticos:
        texto = (
            f"{p['nome']} | Qtd: {p['quantidade']} | "
            f"R$ {p['valor']} | Prioridade: {int(p['prioridade'])}"
        )
        lista_box.insert(tk.END, texto)

# ===== JANELA =====

root = tk.Tk()
root.title("Sistema de Estoque")
root.geometry("550x450")

# ===== FRAME LISTA =====

frame_lista = tk.Frame(root)

tk.Label(frame_lista, text="Produtos em Estoque", font=("Arial", 14)).pack(pady=10)

dropdown_var = tk.StringVar(value="Quantidade")

dropdown = tk.OptionMenu(frame_lista, dropdown_var, "Quantidade", "Valor", "Data", "Prioridade")
dropdown.pack()

tk.Button(frame_lista, text="Ordenar", command=atualizar_lista).pack(pady=5)
tk.Button(frame_lista, text="Ver produtos críticos", command=mostrar_criticos).pack(pady=5)

lista_box = tk.Listbox(frame_lista, width=70)
lista_box.pack(pady=10)

tk.Button(frame_lista, text="Cadastrar Novo Produto", command=mostrar_cadastro).pack()

# ===== FRAME CADASTRO =====

frame_cadastro = tk.Frame(root)

tk.Label(frame_cadastro, text="Cadastro de Produto", font=("Arial", 14)).pack(pady=10)

# Nome
tk.Label(frame_cadastro, text="Nome").pack()
entry_nome = tk.Entry(frame_cadastro)
entry_nome.pack()

# Quantidade
tk.Label(frame_cadastro, text="Quantidade").pack()
entry_qtd = tk.Entry(frame_cadastro)
entry_qtd.pack()

# Valor
tk.Label(frame_cadastro, text="Valor").pack()
entry_valor = tk.Entry(frame_cadastro)
entry_valor.pack()

# Data de entrada (com calendário)
tk.Label(frame_cadastro, text="Data de entrada").pack()
entry_data = DateEntry(frame_cadastro, date_pattern="dd/mm/yyyy")
entry_data.pack()

# Checkbox perecível
perecivel_var = tk.BooleanVar()

check_perecivel = tk.Checkbutton(
    frame_cadastro,
    text="Produto perecível?",
    variable=perecivel_var,
    command=toggle_validade
)
check_perecivel.pack(pady=5)

# Validade (inicialmente escondido)
label_validade = tk.Label(frame_cadastro, text="Data de validade")
date_validade = DateEntry(frame_cadastro, date_pattern="dd/mm/yyyy")

# Botões
tk.Button(frame_cadastro, text="Salvar", command=cadastrar).pack(pady=5)
tk.Button(frame_cadastro, text="Voltar", command=mostrar_lista).pack()

# ===== INÍCIO =====

mostrar_lista()

root.mainloop()
