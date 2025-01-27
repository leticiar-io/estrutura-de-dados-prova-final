import datetime
import locale

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.previous = self.tail
            self.tail = new_node

    def list(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def search(self, data, key=None):
        current = self.head

        while current:
            if key and getattr(current.data, key) == data:
                return current.data
            elif current.data == data:
                return current.data
            current = current.next

        return None

    def remove(self, data):
        current = self.head

        while current:
            if current.data == data:
                if current == self.head and current == self.tail:
                    self.head = self.tail = None
                elif current == self.head:
                    self.head = current.next
                    if self.head:
                        self.head.previous = None
                elif current == self.tail:
                    self.tail = current.previous
                    if self.tail:
                        self.tail.next = None
                else:
                    current.previous.next = current.next
                    current.next.previous = current.previous
                return True

            current = current.next

        return False


class Product:
    def __init__(self, id, name, price, category):
        self.id = id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"#{self.id} - {self.name} ({self.category}) - {locale.currency(self.price, grouping=True)}"


class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role  # client | employee
        self.cart = LinkedList()
        self.actions = []

    def list_cart_products(self):
        print("\n🛒 Seu Carrinho")

        for product in self.cart.list():
            print(product)

    def get_cart_total(self):
        products = []

        for product in self.cart.list():
            products.append(product)

        return sum(product.price for product in products)

    def register_action(self, action):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if len(self.actions) >= 5:
            self.actions.pop(0)

        self.actions.append(f"[{timestamp}] {action}")

    def view_action(self):
        return self.actions[::-1]


class PaperStore:
    def __init__(self):
        self.products = LinkedList()
        self.shopping_history = []

        self.init_products()

    def init_products(self):
        initial_products = [
            Product(1, "Caneta Azul", 2.50, "Escrita"),
            Product(2, "Caderno 100 folhas", 10.00, "Cadernos"),
            Product(3, "Mochila Escolar", 120.00, "Mochilas"),
            Product(4, "Lápis de Cor", 15.00, "Arte"),
            Product(5, "Borracha", 1.50, "Escrita"),
        ]

        for product in initial_products:
            self.products.append(product)

    def list_products(self):
        print("\n📒 Lista de Produtos")

        for product in self.products.list():
            print(product)

    def add_product(self, product):
        if self.products.search(product.id, key="id"):
            print("\n❌ Erro: Já existe um produto com esse ID!")
        else:
            self.products.append(product)
            print("\nProduto adicionado com sucesso!")

    def edit_product(self, id, name=None, price=None, category=None):
        product = self.products.search(id, key="id")

        if product.id == id:
            if name:
                product.name = name
            if price:
                product.price = price
            if category:
                product.category = category

            return product

        return None

    def remove_product(self, id):
        product = self.products.search(id, key="id")

        if product:
            self.products.remove(product)
            print(f"\nProduto {id} removido com sucesso!")
        else:
            print("\n❌ Erro: Produto não encontrado.")

    def list_categories(self):
        categories = set()

        for product in self.products.list():
            categories.add(product.category)

        return categories

    def recommend_products(self, category):
        print("\n⭐ Recomendações")

        recommendations = []

        for product in self.products.list():
            if product.category == category:
                recommendations.append(product)

        return recommendations


def cliente_menu(store: PaperStore, user: User):
    while True:
        print(f"\nBem-vindo, cliente {user.name}! Escolha uma opção:")
        print("1. Visualizar produtos")
        print("2. Adicionar produto ao carrinho")
        print("3. Visualizar carrinho")
        print("4. Remover produto do carrinho")
        print("5. Visualizar recomendações")
        print("6. Finalizar pedido")
        print("7. Realizar pedido")
        print("8. Sair")

        choice = input("Digite sua escolha: ")

        if choice == "1":
            user.register_action("Visualizou produtos")
            store.list_products()

        elif choice == "2":
            product_id = int(
                input("\nDigite o ID do produto para adicionar ao carrinho: ")
            )
            product = store.products.search(product_id, key="id")

            if product:
                user.cart.append(product)
                user.register_action(f"Adicionou {product.name} ao carrinho")
                print(f"{product.name} foi adicionado ao carrinho!")
            else:
                print("❌ Produto não encontrado!")

        elif choice == "3":
            user.register_action("Visualizou carrinho")

            total = user.get_cart_total()

            if total == 0:
                print("\n❌ Erro: Seu carrinho está vazio.")
            else:
                user.list_cart_products()

        elif choice == "4":
            product_id = int(
                input("\nDigite o ID do produto para remover do carrinho: ")
            )
            product = user.cart.search(product_id, key="id")

            if product:
                user.cart.remove(product)
                user.register_action(f"Removeu {product.name} do carrinho")
                print(f"{product.name} foi removido do carrinho!")
            else:
                print("❌ Erro: Produto não encontrado no carrinho!")

        elif choice == "5":
            categories = store.list_categories()
            print("\nCategorias disponíveis:", ", ".join(categories))

            category = input("Digite a categoria que deseja explorar: ")
            recommendations = store.recommend_products(category)
            user.register_action(f"Visualizou recomendações para {category}")

            if not recommendations:
                print("\n❌ Nenhuma recomendação disponível.")
            else:
                for product in recommendations:
                    print(product)

        elif choice == "6":
            total = user.get_cart_total()

            if total == 0:
                print("\n❌ Erro: Seu carrinho está vazio!")
            else:
                print("🛍️ Produtos selecionados:")
                user.list_cart_products()

                print(f"O total do pedido é: {locale.currency(total, grouping=True)}")
                user.register_action("Finalizou pedido")

        elif choice == "7":
            total = user.get_cart_total()

            if total == 0:
                print("\n❌ Erro: Seu carrinho está vazio!")
            else:
                print("📦 Produtos do pedido:")
                user.list_cart_products()

                print(f"Valor total: {locale.currency(total, grouping=True)}")

                store.shopping_history.append(user.cart)
                user.cart = LinkedList()

                user.register_action("Realizou pedido")
                print("Você finalizou seu pedido!")

        elif choice == "8":
            break

        else:
            print("Escolha inválida!")


def employee_menu(store: PaperStore, user: User):
    while True:
        print(f"\nBem-vindo, funcionário {user.name}! Escolha uma opção:")
        print("1. Visualizar produtos")
        print("2. Adicionar produto")
        print("3. Editar produto")
        print("4. Remover produto")
        print("5. Sair")

        choice = input("Digite sua escolha: ")

        if choice == "1":
            user.register_action("Visualizou produtos")
            store.list_products()

        elif choice == "2":
            store.list_products()

            id = int(input("Digite o ID do novo produto: "))
            name = input("Digite o nome do produto: ")
            price = float(input("Digite o preço do produto: "))
            category = input("Digite a categoria do produto: ")

            store.add_product(Product(id, name, price, category))
            user.register_action(f"Adicionou o produto {name}")

        elif choice == "3":
            id = int(input("Digite o ID do produto a ser editado: "))
            name = input("Novo nome (ou Enter para manter): ")
            price = input("Novo preço (ou Enter para manter): ")
            category = input("Nova categoria (ou Enter para manter): ")
            price = float(price) if price else None
            product = store.edit_product(id, name or None, price, category or None)

            if product:
                user.register_action(f"Editou o produto {id}")
                print("Produto editado com sucesso!")
            else:
                print("Produto não encontrado!")

        elif choice == "4":
            id = int(input("Digite o ID do produto a ser removido: "))
            store.remove_product(id)

            user.register_action(f"Removeu o produto {id}")
            print("Produto removido com sucesso!")

        elif choice == "5":
            break

        else:
            print("Escolha inválida!")


# Programa principal
def main():
    store = PaperStore()

    while True:
        print("\nBem-vindo à Loja de Papelaria!")
        name = input("Digite seu nome: ")
        choice_role = input(
            "Você é cliente (c) ou funcionário (f)? (digite a inicial do seu cargo) "
        ).lower()

        if choice_role not in ["c", "f"]:
            print("Tipo inválido. Tente novamente.")
            continue

        roles = {
            "c": "client",
            "f": "employee",
        }

        role = roles[choice_role]

        user = User(name, role)

        if role == "client":
            cliente_menu(store, user)
        elif role == "employee":
            employee_menu(store, user)


if __name__ == "__main__":
    main()
