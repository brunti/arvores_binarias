
class No:
    def __init__(self, dado):
        self.dado = dado
        self.esquerda = None
        self.direita = None
        self.altura = 1


# BST convencional, usada para comparação
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

    def buscar_contando(self, dado):
        atual = self.raiz
        visitados = 0

        while atual is not None:
            visitados += 1

            if dado == atual.dado:
                return True, visitados

            if dado < atual.dado:
                atual = atual.esquerda
            else:
                atual = atual.direita

        return False, visitados

    def minimo(self):
        atual = self.raiz

        if atual is None:
            return None

        while atual.esquerda is not None:
            atual = atual.esquerda

        return atual.dado

    def maximo(self):
        atual = self.raiz

        if atual is None:
            return None

        while atual.direita is not None:
            atual = atual.direita

        return atual.dado

    def em_ordem(self, no):
        if no is not None:
            self.em_ordem(no.esquerda)
            print(no.dado, end=" ")
            self.em_ordem(no.direita)

    def altura_real(self, no):
        if no is None:
            return 0

        esquerda = self.altura_real(no.esquerda)
        direita = self.altura_real(no.direita)

        return 1 + max(esquerda, direita)


# Arvore AVL
class AVL(BST):
    def __init__(self):
        super().__init__()

    # Etapa 2: consultar altura
    def altura(self, no):
        if no is None:
            return 0

        return no.altura

    # Atualizar altura do no
    def atualizar_altura(self, no):
        altura_esquerda = self.altura(no.esquerda)
        altura_direita = self.altura(no.direita)

        no.altura = 1 + max(
            altura_esquerda,
            altura_direita
        )

    # Etapa 3: fator de balanceamento
    def fator_balanceamento(self, no):
        if no is None:
            return 0

        return (
            self.altura(no.esquerda)
            - self.altura(no.direita)
        )

    # Etapa 5: rotacao a direita
    def rotacao_direita(self, y):
        x = y.esquerda
        temp = x.direita

        x.direita = y
        y.esquerda = temp

        self.atualizar_altura(y)
        self.atualizar_altura(x)

        return x

    # Etapa 6: rotacao a esquerda
    def rotacao_esquerda(self, x):
        y = x.direita
        temp = y.esquerda

        y.esquerda = x
        x.direita = temp

        self.atualizar_altura(x)
        self.atualizar_altura(y)

        return y

    # Etapas 8 e 9: insercao recursiva com balanceamento
    def inserir_recursivo(self, no, dado):
        if no is None:
            return No(dado)

        if dado < no.dado:
            no.esquerda = self.inserir_recursivo(
                no.esquerda, dado
            )

        elif dado > no.dado:
            no.direita = self.inserir_recursivo(
                no.direita, dado
            )

        else:
            return no

        self.atualizar_altura(no)
        fb = self.fator_balanceamento(no)

        # Caso LL
        if fb > 1 and dado < no.esquerda.dado:
            return self.rotacao_direita(no)

        # Caso RR
        if fb < -1 and dado > no.direita.dado:
            return self.rotacao_esquerda(no)

        # Caso LR
        if fb > 1 and dado > no.esquerda.dado:
            no.esquerda = self.rotacao_esquerda(
                no.esquerda
            )
            return self.rotacao_direita(no)

        # Caso RL
        if fb < -1 and dado < no.direita.dado:
            no.direita = self.rotacao_direita(
                no.direita
            )
            return self.rotacao_esquerda(no)

        return no

    def inserir(self, dado):
        self.raiz = self.inserir_recursivo(
            self.raiz, dado
        )

    # Etapa 10: mostrar a arvore
    def mostrar(self, no, nivel=0):
        if no is None:
            return

        self.mostrar(no.direita, nivel + 1)

        print(
            "    " * nivel
            + str(no.dado)
            + f" (h={no.altura}, "
            + f"FB={self.fator_balanceamento(no)})"
        )

        self.mostrar(no.esquerda, nivel + 1)

    # Etapa 13: validar balanceamento, alturas e ordenacao
    def verificar_balanceamento(self, no):
        if no is None:
            return True

        altura_esquerda = self.altura_real(no.esquerda)
        altura_direita = self.altura_real(no.direita)

        altura_correta = 1 + max(
            altura_esquerda,
            altura_direita
        )

        fb = altura_esquerda - altura_direita

        if abs(fb) > 1 or no.altura != altura_correta:
            return False

        return (
            self.verificar_balanceamento(no.esquerda)
            and self.verificar_balanceamento(no.direita)
        )

    def verificar_ordenacao(
        self, no, minimo=None, maximo=None
    ):
        if no is None:
            return True

        if minimo is not None and no.dado <= minimo:
            return False

        if maximo is not None and no.dado >= maximo:
            return False

        return (
            self.verificar_ordenacao(
                no.esquerda, minimo, no.dado
            )
            and self.verificar_ordenacao(
                no.direita, no.dado, maximo
            )
        )


# Etapa 11: testar os quatro casos
def testar_rotacoes():
    testes = [
        ("LL", [30, 20, 10]),
        ("RR", [10, 20, 30]),
        ("LR", [30, 10, 20]),
        ("RL", [10, 30, 20])
    ]

    print("\n===== TESTES DAS ROTACOES =====")

    for caso, valores in testes:
        arvore = AVL()

        for valor in valores:
            arvore.inserir(valor)

        print(f"\nCaso {caso}: {valores}")
        print("Raiz esperada: 20")
        print("Raiz obtida:", arvore.raiz.dado)

        print("Em ordem:")
        arvore.em_ordem(arvore.raiz)
        print()

        print(
            "Balanceada:",
            arvore.verificar_balanceamento(arvore.raiz)
        )


# Teste com seis valores
def testar_seis_valores():
    arvore = AVL()
    valores = [10, 20, 30, 40, 50, 25]

    print("\n===== TESTE COM SEIS VALORES =====")

    for valor in valores:
        arvore.inserir(valor)

    print("Arvore:")
    arvore.mostrar(arvore.raiz)

    print("Raiz:", arvore.raiz.dado)
    print("Altura:", arvore.altura(arvore.raiz))

    print("Em ordem:")
    arvore.em_ordem(arvore.raiz)
    print()

    print(
        "Balanceamento valido:",
        arvore.verificar_balanceamento(arvore.raiz)
    )

    print(
        "Ordenacao valida:",
        arvore.verificar_ordenacao(arvore.raiz)
    )


# Etapa 14: comparar BST e AVL
def comparar_arvores():
    bst = BST()
    avl = AVL()

    valores = list(range(1, 101))

    for valor in valores:
        bst.inserir(valor)
        avl.inserir(valor)

    encontrado_bst, visitas_bst = bst.buscar_contando(100)
    encontrado_avl, visitas_avl = avl.buscar_contando(100)

    print("\n===== COMPARACAO BST E AVL =====")

    print("Quantidade de valores:", len(valores))

    print("Altura da BST:", bst.altura_real(bst.raiz))
    print("Altura da AVL:", avl.altura(avl.raiz))

    print("Busca de 100 na BST:")
    print("Encontrado:", encontrado_bst)
    print("Nos visitados:", visitas_bst)

    print("Busca de 100 na AVL:")
    print("Encontrado:", encontrado_avl)
    print("Nos visitados:", visitas_avl)


# Menu para testar a AVL
def menu():
    arvore = AVL()

    while True:
        print("\n===== MENU AVL =====")
        print("1 - Inserir valor")
        print("2 - Buscar valor")
        print("3 - Mostrar em ordem")
        print("4 - Mostrar minimo")
        print("5 - Mostrar maximo")
        print("6 - Mostrar arvore")
        print("7 - Verificar balanceamento")
        print("8 - Encerrar")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            try:
                valor = int(input("Valor para inserir: "))
                arvore.inserir(valor)
                print("Valor inserido.")
            except ValueError:
                print("Digite um numero inteiro.")

        elif opcao == "2":
            try:
                valor = int(input("Valor para buscar: "))
                print(
                    "Encontrado."
                    if arvore.buscar(valor)
                    else "Nao encontrado."
                )
            except ValueError:
                print("Digite um numero inteiro.")

        elif opcao == "3":
            print("Valores em ordem:")
            arvore.em_ordem(arvore.raiz)
            print()

        elif opcao == "4":
            print("Minimo:", arvore.minimo())

        elif opcao == "5":
            print("Maximo:", arvore.maximo())

        elif opcao == "6":
            if arvore.raiz is None:
                print("Arvore vazia.")
            else:
                arvore.mostrar(arvore.raiz)

        elif opcao == "7":
            print(
                "Balanceamento:",
                arvore.verificar_balanceamento(arvore.raiz)
            )
            print(
                "Ordenacao:",
                arvore.verificar_ordenacao(arvore.raiz)
            )

        elif opcao == "8":
            print("Programa encerrado.")
            break

        else:
            print("Opcao invalida.")


# RESPOSTAS DA ATIVIDADE
#
# 1. As alturas permitem identificar nos desbalanceados.
#
# 2. O fator de balanceamento e a altura esquerda
#    menos a altura direita.
#
# 3. A rotacao reorganiza os filhos sem alterar os dados.
#
# 4. LL usa rotacao direita; RR usa esquerda.
#    LR usa esquerda e depois direita.
#    RL usa direita e depois esquerda.
#
# 5. A insercao recursiva atualiza alturas e rebalanceia
#    os nos durante o retorno da recursao.
#
# 6. Busca, minimo, maximo e percurso em ordem continuam
#    funcionando porque as rotacoes mantem a ordenacao.
#
# 7. A BST pode chegar a altura 100 com 100 valores
#    inseridos em ordem. A AVL mantem altura logaritmica.
#
# 8. A busca custa O(h). Na AVL, h e O(log n).
#
# 9. As rotacoes mudam as referencias entre os nos,
#    nao os valores armazenados.
#
# 10. A remocao precisa de rebalanceamento proprio e
#     nao foi implementada neste tutorial.


if __name__ == "__main__":
    testar_rotacoes()
    testar_seis_valores()
    comparar_arvores()
    menu()
