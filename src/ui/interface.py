import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

from src.core.lista_produtos import ListaProdutos
from src.core.fila_criticos import FilaCriticos
from src.service.estoque_service import EstoqueService

# ===== INSTÂNCIAS =====
lista = ListaProdutos()
fila = FilaCriticos()
service = EstoqueService(lista, fila)

service.carregar_de_arquivo()

produtos_filtrados = []
produto_em_edicao = None

# ===== FUNÇÕES =====

def mostrar_lista():
    global produto_em_edicao
    produto_em_edicao = None

    frame_cadastro.pack_forget()
    frame_lista.pack(fill="both", expand=True)

    atualizar_lista()


def mostrar_cadastro():
    frame_lista.pack_forget()
    frame_cadastro.pack(fill="both", expand=True)


def atualizar_lista():
    global produtos_filtrados

    lista_box.delete(0, tk.END)

    produtos = lista.exibir()
    criterio = dropdown_var.get()
    busca = entry_busca.get().lower()

    if busca:
        produtos = [p for p in produtos if busca in p["nome"].lower()]

    if criterio == "Quantidade":
        produtos = sorted(produtos, key=lambda x: x["quantidade"])

    elif criterio == "Valor (mais barato)":
        produtos = sorted(produtos, key=lambda x: x.get("preco", 0))

    elif criterio == "Valor (mais caro)":
        produtos = sorted(produtos, key=lambda x: x.get("preco", 0), reverse=True)

    elif criterio == "Data (mais antigo)":
        produtos = sorted(produtos, key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y"))

    elif criterio == "Data (mais recente)":
        produtos = sorted(produtos, key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y"), reverse=True)

    elif criterio == "Prioridade":
        produtos = sorted(produtos, key=lambda x: service.calcular_prioridade(x), reverse=True)

    produtos_filtrados = produtos

    for p in produtos:
        prioridade = service.calcular_prioridade(p)

        texto = (
            f"{p['nome']} | Qtd: {p['quantidade']} | "
            f"Custo: R$ {p.get('custo', 0):.2f} | "
            f"Venda: R$ {p.get('preco', 0):.2f} | "
            f"{p['data']} | Prioridade: {int(prioridade)}"
        )

        lista_box.insert(tk.END, texto)


def cadastrar():
    global produto_em_edicao

    nome = entry_nome.get()
    qtd = entry_qtd.get()
    custo = entry_custo.get()
    preco = entry_preco.get()
    data = entry_data.get_date().strftime("%d/%m/%Y")

    if not nome or not qtd or not custo or not preco:
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
        produto["validade"] = entry_validade.get_date().strftime("%d/%m/%Y")

    if produto_em_edicao:
        index = lista.produtos.index(produto_em_edicao)
        lista.produtos[index] = produto
        produto_em_edicao = None
    else:
        lista.inserir(produto)

    service.salvar_em_arquivo()

    messagebox.showinfo("Sucesso", "Produto salvo!")

    limpar_campos()
    mostrar_lista()


def excluir():
    selecionado = lista_box.curselection()

    if not selecionado:
        messagebox.showerror("Erro", "Selecione um produto")
        return

    produto = produtos_filtrados[selecionado[0]]

    lista.produtos.remove(produto)
    service.salvar_em_arquivo()

    atualizar_lista()


def editar():
    global produto_em_edicao

    selecionado = lista_box.curselection()

    if not selecionado:
        messagebox.showerror("Erro", "Selecione um produto")
        return

    produto = produtos_filtrados[selecionado[0]]
    produto_em_edicao = produto

    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, produto["nome"])

    entry_qtd.delete(0, tk.END)
    entry_qtd.insert(0, produto["quantidade"])

    entry_custo.delete(0, tk.END)
    entry_custo.insert(0, produto.get("custo", 0))

    entry_preco.delete(0, tk.END)
    entry_preco.insert(0, produto.get("preco", 0))

    entry_data.set_date(datetime.strptime(produto["data"], "%d/%m/%Y"))

    if "validade" in produto:
        perecivel_var.set(True)
        toggle_validade()
        entry_validade.set_date(datetime.strptime(produto["validade"], "%d/%m/%Y"))
    else:
        perecivel_var.set(False)
        toggle_validade()

    mostrar_cadastro()


def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)
    entry_custo.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    perecivel_var.set(False)
    toggle_validade()


def toggle_validade():
    if perecivel_var.get():
        frame_validade.pack()
    else:
        frame_validade.pack_forget()


# ===== JANELA =====
root = tk.Tk()
root.title("Gerenciamento de Estoque")

# tela cheia adaptável
root.state("zoomed")

# ===== FRAME LISTA =====
frame_lista = tk.Frame(root)

# TÍTULO
tk.Label(frame_lista, text="Gerenciamento de Estoque", font=("Arial", 18)).pack(pady=10)

# TOPO (BUSCA + ORDENAÇÃO)
frame_topo = tk.Frame(frame_lista)
frame_topo.pack(pady=5)

entry_busca = tk.Entry(frame_topo)
entry_busca.pack(side=tk.LEFT, padx=5)

tk.Button(frame_topo, text="Buscar", command=atualizar_lista).pack(side=tk.LEFT)

dropdown_var = tk.StringVar(value="Quantidade")

dropdown = tk.OptionMenu(
    frame_topo,
    dropdown_var,
    "Quantidade",
    "Valor (mais barato)",
    "Valor (mais caro)",
    "Data (mais antigo)",
    "Data (mais recente)",
    "Prioridade"
)
dropdown.pack(side=tk.LEFT, padx=5)

tk.Button(frame_topo, text="Ordenar", command=atualizar_lista).pack(side=tk.LEFT)

# LISTA
lista_box = tk.Listbox(frame_lista, width=100)
lista_box.pack(pady=10)

# BOTÕES CRUD
frame_botoes = tk.Frame(frame_lista)
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Cadastrar", command=mostrar_cadastro).pack(side=tk.LEFT, padx=10)
tk.Button(frame_botoes, text="Editar", command=editar).pack(side=tk.LEFT, padx=10)
tk.Button(frame_botoes, text="Excluir", command=excluir).pack(side=tk.LEFT, padx=10)

# ===== FRAME CADASTRO =====
frame_cadastro = tk.Frame(root)

tk.Label(frame_cadastro, text="Cadastro de Produto", font=("Arial", 16)).pack(pady=10)

entry_nome = tk.Entry(frame_cadastro)
entry_nome.pack()

entry_qtd = tk.Entry(frame_cadastro)
entry_qtd.pack()

entry_custo = tk.Entry(frame_cadastro)
entry_custo.pack()

entry_preco = tk.Entry(frame_cadastro)
entry_preco.pack()

entry_data = DateEntry(frame_cadastro, date_pattern="dd/mm/yyyy")
entry_data.pack()

perecivel_var = tk.BooleanVar()

tk.Checkbutton(
    frame_cadastro,
    text="Produto perecível?",
    variable=perecivel_var,
    command=toggle_validade
).pack()

frame_validade = tk.Frame(frame_cadastro)

entry_validade = DateEntry(frame_validade, date_pattern="dd/mm/yyyy")
entry_validade.pack()

tk.Button(frame_cadastro, text="Salvar", command=cadastrar).pack(pady=5)
tk.Button(frame_cadastro, text="Voltar", command=mostrar_lista).pack()

# ===== INÍCIO =====
mostrar_lista()
root.mainloop()