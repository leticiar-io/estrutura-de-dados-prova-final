import datetime

class Produto:
    def __init__(self, id, nome, preco, categoria):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.categoria = categoria

    def __str__(self):
        return f"{self.id} - {self.nome} ({self.categoria}) - R${self.preco:.2f}"


class Usuario:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo  # cliente ou funcionario
        self.carrinho = []
        self.acoes = []

    def registrar_acao(self, acao):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(self.acoes) >= 5:
            self.acoes.pop(0)
        self.acoes.append(f"[{timestamp}] {acao}")

    def visualizar_acao(self):
        return self.acoes[::-1]


class LojaPapelaria:
    def __init__(self):
        self.produtos = [
            Produto(1, "Caneta Azul", 2.50, "Escrita"),
            Produto(2, "Caderno 100 folhas", 10.00, "Cadernos"),
            Produto(3, "Mochila Escolar", 120.00, "Mochilas"),
            Produto(4, "Lápis de Cor", 15.00, "Arte"),
            Produto(5, "Borracha", 1.50, "Escrita"),
        ]
        self.fila_compras = []

    def visualizar_produtos(self):
        for produto in self.produtos:
            print(produto)

    def adicionar_produto(self, produto):
        if any(p.id == produto.id for p in self.produtos):
            print("Erro: Já existe um produto com esse ID!")
        else:
            self.produtos.append(produto)
            print("Produto adicionado com sucesso!")

    def editar_produto(self, id, nome=None, preco=None, categoria=None):
        for produto in self.produtos:
            if produto.id == id:
                if nome:
                    produto.nome = nome
                if preco:
                    produto.preco = preco
                if categoria:
                    produto.categoria = categoria
                return produto
        return None

    def remover_produto(self, id):
        self.produtos = [produto for produto in self.produtos if produto.id != id]

    def listar_categorias(self):
        return set(produto.categoria for produto in self.produtos)

    def recomendar_produtos(self, categoria):
        return [produto for produto in self.produtos if produto.categoria == categoria]


# Funções para ações dos usuários
def cliente_menu(loja, usuario):
    while True:
        print(f"\nBem-vindo, cliente {usuario.nome}! Escolha uma opção:")
        print("1. Visualizar produtos")
        print("2. Adicionar produto ao carrinho")
        print("3. Visualizar carrinho")
        print("4. Remover produto do carrinho")
        print("5. Visualizar recomendações")
        print("6. Finalizar pedido")
        print("7. Realizar pedido")
        print("8. Sair")

        escolha = input("Digite sua escolha: ")

        if escolha == "1":
            usuario.registrar_acao("Visualizou produtos")
            loja.visualizar_produtos()

        elif escolha == "2":
            id_produto = int(input("Digite o ID do produto para adicionar ao carrinho: "))
            produto = next((p for p in loja.produtos if p.id == id_produto), None)
            if produto:
                usuario.carrinho.append(produto)
                usuario.registrar_acao(f"Adicionou {produto.nome} ao carrinho")
                print(f"{produto.nome} foi adicionado ao carrinho!")
            else:
                print("Produto não encontrado!")

        elif escolha == "3":
            usuario.registrar_acao("Visualizou carrinho")
            if not usuario.carrinho:
                print("Carrinho está vazio.")
            else:
                for item in usuario.carrinho:
                    print(item)

        elif escolha == "4":
            id_produto = int(input("Digite o ID do produto para remover do carrinho: "))
            produto = next((p for p in usuario.carrinho if p.id == id_produto), None)
            if produto:
                usuario.carrinho.remove(produto)
                usuario.registrar_acao(f"Removeu {produto.nome} do carrinho")
                print(f"{produto.nome} foi removido do carrinho!")
            else:
                print("Produto não encontrado no carrinho!")

        elif escolha == "5":
            categorias = loja.listar_categorias()
            print("Categorias disponíveis:", ", ".join(categorias))
            categoria = input("Digite a categoria que deseja explorar: ")
            recomendacoes = loja.recomendar_produtos(categoria)
            usuario.registrar_acao(f"Visualizou recomendações para {categoria}")
            if not recomendacoes:
                print("Nenhuma recomendação disponível.")
            else:
                for produto in recomendacoes:
                    print(produto)

        elif escolha == "6":
            if not usuario.carrinho:
                print("Erro: Seu carrinho está vazio!")
            else:
                total = sum(produto.preco for produto in usuario.carrinho)
                print("Produtos selecionados:")
                for item in usuario.carrinho:
                    print(item)
                print(f"O total do pedido é: R${total:.2f}")
                usuario.registrar_acao("Finalizou pedido")

        elif escolha == "7":
            if not usuario.carrinho:
                print("Erro: Seu carrinho está vazio!")
            else:
                print("Produtos do pedido:")
                for item in usuario.carrinho:
                    print(item)
                total = sum(produto.preco for produto in usuario.carrinho)
                print(f"Valor total: R${total:.2f}")
                loja.fila_compras.append(usuario.carrinho)
                usuario.carrinho = []
                usuario.registrar_acao("Realizou pedido")
                print("Você finalizou seu pedido!")

        elif escolha == "8":
            break

        else:
            print("Escolha inválida!")


def funcionario_menu(loja, usuario):
    while True:
        print(f"\nBem-vindo, funcionário {usuario.nome}! Escolha uma opção:")
        print("1. Visualizar produtos")
        print("2. Adicionar produto")
        print("3. Editar produto")
        print("4. Remover produto")
        print("5. Sair")

        escolha = input("Digite sua escolha: ")

        if escolha == "1":
            usuario.registrar_acao("Visualizou produtos")
            loja.visualizar_produtos()

        elif escolha == "2":
            loja.visualizar_produtos()
            id = int(input("Digite o ID do novo produto: "))
            nome = input("Digite o nome do produto: ")
            preco = float(input("Digite o preço do produto: "))
            categoria = input("Digite a categoria do produto: ")
            loja.adicionar_produto(Produto(id, nome, preco, categoria))
            usuario.registrar_acao(f"Adicionou o produto {nome}")

        elif escolha == "3":
            id = int(input("Digite o ID do produto a ser editado: "))
            nome = input("Novo nome (ou Enter para manter): ")
            preco = input("Novo preço (ou Enter para manter): ")
            categoria = input("Nova categoria (ou Enter para manter): ")
            preco = float(preco) if preco else None
            produto = loja.editar_produto(id, nome or None, preco, categoria or None)
            if produto:
                usuario.registrar_acao(f"Editou o produto {id}")
                print("Produto editado com sucesso!")
            else:
                print("Produto não encontrado!")

        elif escolha == "4":
            id = int(input("Digite o ID do produto a ser removido: "))
            loja.remover_produto(id)
            usuario.registrar_acao(f"Removeu o produto {id}")
            print("Produto removido com sucesso!")

        elif escolha == "5":
            break

        else:
            print("Escolha inválida!")


# Programa principal
def main():
    loja = LojaPapelaria()

    while True:
        print("\nBem-vindo à Loja de Papelaria!")
        nome = input("Digite seu nome: ")
        tipo = input("Você é cliente ou funcionário? ").lower()

        if tipo not in ["cliente", "funcionario"]:
            print("Tipo inválido. Tente novamente.")
            continue

        usuario = Usuario(nome, tipo)

        if tipo == "cliente":
            cliente_menu(loja, usuario)
        elif tipo == "funcionario":
            funcionario_menu(loja, usuario)


if __name__ == "__main__":
    main()