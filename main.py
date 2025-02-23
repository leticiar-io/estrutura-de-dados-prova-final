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
        self.head: Node | None = None
        self.tail: Node | None = None

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


class Stack:
    def __init__(self):
        self.top: Node | None = None
        self.bottom: Node | None = None
        self.size = 0

    def push(self, data):
        new_node = Node(data)

        if not self.top:
            self.top = self.bottom = new_node
        else:
            self.bottom.next = new_node
            new_node.previous = self.bottom
            self.bottom = new_node

        self.size += 1

    def list(self):
        current = self.top
        while current:
            yield current.data
            current = current.next

    def search(self, data):
        current = self.top

        while current:
            if current.data == data:
                return current.data
            current = current.next

        return None

    def pop(self):
        if not self.top:
            return None

        data = self.bottom.data

        if self.top == self.bottom:
            self.top = self.bottom = None
        else:
            self.bottom = self.bottom.previous
            self.bottom.next = None

        self.size -= 1

        return data


class Queue:
    def __init__(self):
        self.front: Node | None = None
        self.rear: Node | None = None
        self.size = 0

    def enqueue(self, data):
        new_node = Node(data)

        if not self.front:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            new_node.previous = self.rear
            self.rear = new_node

        self.size += 1

    def list(self):
        current = self.front
        while current:
            yield current.data
            current = current.next

    def search(self, data):
        current = self.front

        while current:
            if current.data == data:
                return current.data
            current = current.next

        return None

    def dequeue(self):
        if not self.front:
            return None

        data = self.front.data

        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.front = self.front.next
            self.front.previous = None

        self.size -= 1

        return data


class TreeNodeAVL:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        def _insert(node, data):
            if not node:
                return TreeNodeAVL(data)
            if data < node.data:
                node.left = _insert(node.left, data)
            else:
                node.right = _insert(node.right, data)

            node.height = 1 + max(self._height(node.left), self._height(node.right))
            balance = self._balance_factor(node)

            # Rotações
            if balance > 1:
                if data < node.left.data:
                    return self._rotate_right(node)
                else:
                    node.left = self._rotate_left(node.left)
                    return self._rotate_right(node)
            if balance < -1:
                if data > node.right.data:
                    return self._rotate_left(node)
                else:
                    node.right = self._rotate_right(node.right)
                    return self._rotate_left(node)
            return node

        self.root = _insert(self.root, data)

    def _height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def search(self, data):
        current = self.root

        while current:
            if current.data == data:
                return current.data
            elif data < current.data:
                current = current.left
            else:
                current = current.right

        return None

    def pre_order(self):
        def traverse(node):
            if node:
                yield node.data
                yield from traverse(node.left)
                yield from traverse(node.right)

        yield from traverse(self.root)

    def in_order(self):
        def traverse(node):
            if node:
                yield from traverse(node.left)
                yield node.data
                yield from traverse(node.right)

        yield from traverse(self.root)

    def post_order(self):
        def traverse(node):
            if node:
                yield from traverse(node.left)
                yield from traverse(node.right)
                yield node.data

        yield from traverse(self.root)

    def remove(self, data):
        def _remove(node, data):
            if not node:
                return None
            if data < node.data:
                node.left = _remove(node.left, data)
            elif data > node.data:
                node.right = _remove(node.right, data)
            else:
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                temp = self._min_value_node(node.right)
                node.data = temp.data
                node.right = _remove(node.right, temp.data)

            node.height = 1 + max(self._height(node.left), self._height(node.right))
            balance = self._balance_factor(node)

            # Rotações após remoção
            if balance > 1:
                if self._balance_factor(node.left) >= 0:
                    return self._rotate_right(node)
                else:
                    node.left = self._rotate_left(node.left)
                    return self._rotate_right(node)
            if balance < -1:
                if self._balance_factor(node.right) <= 0:
                    return self._rotate_left(node)
                else:
                    node.right = self._rotate_right(node.right)
                    return self._rotate_left(node)
            return node

        self.root = _remove(self.root, data)

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current


class Product:
    def __init__(self, id, name, price, category):
        self.id = id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"#{self.id} - {self.name} ({self.category}) - {locale.currency(self.price, grouping=True)}"


class Action:
    def __init__(self, action, timestamp):
        self.action = action
        self.timestamp = timestamp

    def __str__(self):
        return f"[{self.timestamp}] {self.action}"


class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role  # client | employee
        self.cart = LinkedList()
        self.actions = Stack()

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

        if self.actions.size >= 5:
            self.actions.pop()

        action = Action(action, timestamp)

        self.actions.push(action)

    def list_actions(self):
        return self.actions.list()


class PaperStore:
    def __init__(self):
        self.products = LinkedList()
        self.shopping_history = Queue()
        self.categories = AVLTree()

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

            if not self.categories.search(product.category):
                self.categories.insert(product.category)

    def list_products(self):
        print("\n📒 Lista de Produtos")

        for product in self.products.list():
            print(product)

    def add_product(self, product):
        if self.products.search(product.id, key="id"):
            print("\n❌ Erro: Já existe um produto com esse ID!")
        else:
            self.products.append(product)

            if not self.categories.search(product.category):
                self.categories.insert(product.category)

            print("\nProduto adicionado com sucesso!")

    def edit_product(self, id, name=None, price=None, category=None):
        product = self.products.search(id, key="id")

        if product.id == id:
            if name:
                product.name = name
            if price:
                product.price = price
            if category:
                last_category = product.category
                product.category = category

                if not self.categories.search(category):
                    self.categories.insert(category)

                if last_category:
                    self.categories.remove(last_category)

            return product

        return None

    def remove_product(self, id):
        product = self.products.search(id, key="id")

        if product:
            self.products.remove(product)

            if not any(product.category == p.category for p in self.products.list()):
                self.categories.remove(product.category)

            print(f"\nProduto {id} removido com sucesso!")
        else:
            print("\n❌ Erro: Produto não encontrado.")

    def list_categories(self):
        return list(self.categories.in_order())

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
            print("\nCategorias disponíveis:")

            for category in categories:
                print(f"- {category}")

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

                store.shopping_history.enqueue(user.cart)
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
