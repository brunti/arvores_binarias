class No:
    def __init__(self, dado):
        self.dado = dado
        self.esquerda = None
        self.direita = None


class BST:
    def __init__(self):
        self.raiz = None

    def inserir(self, dado):
        novo = No(dado)

        if self.raiz is None:
            self.raiz = novo
            return

        atual = self.raiz

        while True:
            if dado < atual.dado:
                if atual.esquerda is None:
                    atual.esquerda = novo
                    return
                atual = atual.esquerda

            elif dado > atual.dado:
                if atual.direita is None:
                    atual.direita = novo
                    return
                atual = atual.direita

            else:
                return

    def buscar(self, dado):
        atual = self.raiz

        while atual is not None:
            if dado == atual.dado:
                return True

            if dado < atual.dado:
                atual = atual.esquerda
            else:
                atual = atual.direita

        return False

    def minimo(self):
        if self.raiz is None:
            return None

        atual = self.raiz

        while atual.esquerda is not None:
            atual = atual.esquerda

        return atual.dado

    def maximo(self):
        if self.raiz is None:
            return None

        atual = self.raiz

        while atual.direita is not None:
            atual = atual.direita

        return atual.dado

    def em_ordem(self, no):
        if no is not None:
            self.em_ordem(no.esquerda)
            print(no.dado, end=" ")
            self.em_ordem(no.direita)

    def remover(self, no, dado):
        if no is None:
            return None

        if dado < no.dado:
            no.esquerda = self.remover(no.esquerda, dado)

        elif dado > no.dado:
            no.direita = self.remover(no.direita, dado)

        else:

            if no.esquerda is None:
                return no.direita


            if no.direita is None:
                return no.esquerda


            sucessor = no.direita

            while sucessor.esquerda is not None:
                sucessor = sucessor.esquerda

            no.dado = sucessor.dado
            no.direita = self.remover(
                no.direita, sucessor.dado
            )

        return no

    def excluir(self, dado):
        self.raiz = self.remover(self.raiz, dado)


def mostrar_arvore(arvore):
    if arvore.raiz is None:
        print("A árvore está vazia.")
    else:
        arvore.em_ordem(arvore.raiz)
        print()


def executar_testes():
    print("\n===== TESTES OBRIGATÓRIOS =====")

    arvore = BST()

    valores = [
        61, 43, 77, 16, 55, 69, 85,
        11, 31, 49, 59, 65, 73, 81, 89
    ]

    # Inserção dos valores obrigatórios
    for valor in valores:
        arvore.inserir(valor)

    print("\n1. Mostrar em ordem:")
    mostrar_arvore(arvore)

    print("\n2. Buscar 73:")
    print(arvore.buscar(73))

    print("\n3. Buscar 100:")
    print(arvore.buscar(100))

    print("\n4. Mostrar mínimo e máximo:")
    print("Mínimo:", arvore.minimo())
    print("Máximo:", arvore.maximo())

    print("\n5. Remover 31 (folha):")
    arvore.excluir(31)
    mostrar_arvore(arvore)

    print("\n6. Remover 16 (um filho):")
    arvore.excluir(16)
    mostrar_arvore(arvore)

    print("\n7. Remover 77 (dois filhos):")
    arvore.excluir(77)
    mostrar_arvore(arvore)

    print("\n8. Percurso em ordem final:")
    mostrar_arvore(arvore)


def menu():
    arvore = BST()

    while True:
        print("\n===== GERENCIADOR DE VALORES COM BST =====")
        print("1 - Inserir valor")
        print("2 - Buscar valor")
        print("3 - Mostrar em ordem")
        print("4 - Mostrar menor valor")
        print("5 - Mostrar maior valor")
        print("6 - Remover valor")
        print("7 - Executar testes obrigatórios")
        print("8 - Encerrar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                valor = int(input("Digite o valor para inserir: "))
                arvore.inserir(valor)
                print("Operação de inserção concluída.")
            except ValueError:
                print("Digite um número inteiro válido.")

        elif opcao == "2":
            try:
                valor = int(input("Digite o valor para buscar: "))

                if arvore.buscar(valor):
                    print("Valor encontrado.")
                else:
                    print("Valor não encontrado.")
            except ValueError:
                print("Digite um número inteiro válido.")

        elif opcao == "3":
            print("Valores em ordem:")
            mostrar_arvore(arvore)

        elif opcao == "4":
            minimo = arvore.minimo()

            if minimo is None:
                print("A árvore está vazia.")
            else:
                print("Menor valor:", minimo)

        elif opcao == "5":
            maximo = arvore.maximo()

            if maximo is None:
                print("A árvore está vazia.")
            else:
                print("Maior valor:", maximo)

        elif opcao == "6":
            try:
                valor = int(input("Digite o valor para remover: "))

                if arvore.buscar(valor):
                    arvore.excluir(valor)
                    print("Valor removido com sucesso.")
                else:
                    print("Valor não encontrado.")
            except ValueError:
                print("Digite um número inteiro válido.")

        elif opcao == "7":
            executar_testes()

        elif opcao == "8":
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida. Tente novamente.")


# (a) O percurso em ordem gera valores ordenados porque visita a esquerda, o nó atual e depois a direita.

# (b) O mínimo não precisa ser uma folha, pois pode ter um filho à direita.

# (c) O pior formato é uma árvore degenerada, em que cada nó possui apenas um filho, ficando parecida com uma lista.

# (d) Usa-se o mínimo da subárvore direita porque ele é o próximo valor maior que o nó removido, mantendo a ordem.


if __name__ == "__main__":
    menu()
