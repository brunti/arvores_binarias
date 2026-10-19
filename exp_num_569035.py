class No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


def tokenizar(expressao):
    tokens = []
    numero = ""

    for caractere in expressao:

        if caractere.isdigit() or caractere == ".":
            numero += caractere

        elif caractere == " ":
            continue

        elif caractere in "+-*/^()":

            if numero:
                tokens.append(numero)
                numero = ""

            tokens.append(caractere)

        else:
            raise ValueError(
                f"Caractere não aceito: {caractere}"
            )

    if numero:
        tokens.append(numero)

    return tokens


def precedencia(operador):

    if operador in ("+", "-"):
        return 1

    elif operador in ("*", "/"):
        return 2

    elif operador == "^":
        return 3

    return 0


def para_posfixa(tokens):
    saida = []
    pilha = []

    for token in tokens:

        if token.replace(".", "", 1).isdigit():

            saida.append(token)

        elif token == "(":

            pilha.append(token)

        elif token == ")":

            while pilha and pilha[-1] != "(":
                saida.append(pilha.pop())

            if not pilha:
                raise ValueError(
                    "Parênteses incompatíveis."
                )

            pilha.pop()

        elif token in ("+", "-", "*", "/", "^"):

            while (
                pilha
                and pilha[-1] != "("
                and (
                    precedencia(pilha[-1]) > precedencia(token)
                    or (
                        precedencia(pilha[-1]) == precedencia(token)
                        and token != "^"
                    )
                )
            ):
                saida.append(pilha.pop())

            pilha.append(token)

    while pilha:

        if pilha[-1] == "(":
            raise ValueError(
                "Parênteses incompatíveis."
            )

        saida.append(pilha.pop())

    return saida


def construir_arvore(posfixa):
    pilha = []

    for token in posfixa:

        if token.replace(".", "", 1).isdigit():

            pilha.append(No(token))

        else:

            if len(pilha) < 2:
                raise ValueError(
                    "Expressão matemática inválida."
                )

            direita = pilha.pop()
            esquerda = pilha.pop()

            novo = No(token)

            novo.esquerda = esquerda
            novo.direita = direita

            pilha.append(novo)

    if len(pilha) != 1:
        raise ValueError(
            "Expressão matemática inválida."
        )

    return pilha.pop()


def pre_ordem(no):

    if no is None:
        return []

    return (
        [str(no.valor)]
        + pre_ordem(no.esquerda)
        + pre_ordem(no.direita)
    )


def em_ordem(no):

    if no is None:
        return []

    return (
        em_ordem(no.esquerda)
        + [str(no.valor)]
        + em_ordem(no.direita)
    )


def pos_ordem(no):

    if no is None:
        return []

    return (
        pos_ordem(no.esquerda)
        + pos_ordem(no.direita)
        + [str(no.valor)]
    )


def gerar_expressao(no):

    if no.esquerda is None and no.direita is None:
        return str(no.valor)

    esquerda = gerar_expressao(no.esquerda)
    direita = gerar_expressao(no.direita)

    return f"({esquerda} {no.valor} {direita})"


def calcular(no):

    if no.esquerda is None and no.direita is None:
        return float(no.valor)

    esquerda = calcular(no.esquerda)
    direita = calcular(no.direita)

    if no.valor == "+":
        return esquerda + direita

    elif no.valor == "-":
        return esquerda - direita

    elif no.valor == "*":
        return esquerda * direita

    elif no.valor == "/":

        if direita == 0:
            raise ZeroDivisionError(
                "Erro: divisão por zero."
            )

        return esquerda / direita

    elif no.valor == "^":
        return esquerda ** direita


def main():

    expressao = input(
        "Digite uma expressão matemática: "
    )

    if not expressao.strip():
        print("Erro: expressão vazia.")
        return

    try:

        tokens = tokenizar(expressao)

        posfixa = para_posfixa(tokens)

        raiz = construir_arvore(posfixa)

        print("\nTokens:")
        print(tokens)

        print("\nExpressão pós-fixa:")
        print(" ".join(posfixa))

        print("\nPré-ordem:")
        print(" ".join(pre_ordem(raiz)))

        print("\nEm ordem:")
        print(" ".join(em_ordem(raiz)))

        print("\nPós-ordem:")
        print(" ".join(pos_ordem(raiz)))

        print("\nExpressão reconstruída:")
        print(gerar_expressao(raiz))

        print("\nResultado:")
        print(calcular(raiz))

    except Exception as erro:
        print(f"\nErro: {erro}")


main()

# 1- Porque a expressão precisa ser tokenizada?
# ---
# A tokenização separa a expressão em pequenas unidades chamadas tokens. Isso facilita o processamento da expressão fazendo com que o programa consiga identificar corretamente cada elemento e aplicar as logicas de precedência e construção.
# ---
# 2- Porque uma pilha é adequada para operadores e parênteses?
# ---
# Por conta da regra LIFO, ou seja, o último elemento inserido é o primeiro a ser removido. E por conta dessa característica os operadores e os parenteses podem ser analisados e verificar a sua precedência para que asssim o calculo e as regras matematicas sejam realizadas de forma correta.
# ---
# 3- Por que o primeiro pop na construção da árvore corresponde ao filho direito?*
# ---
# Pois na notação pós-fixa, os operandos aparecem antes do operador. Assim quando um operador for encontrado, os dois últimos operandos empilhados pertencem a ele. O primeiro elemento removido da pilha corresponde ao operando que estava mais à direita na expressão, tornando-se o filho direito. O segundo elemento removido torna-se o filho esquerdo.
# ---
# 4- Qual a relação entre pós-ordem e notação pós-fixa?
# ---
# O percurso pós-ordem segue os nós na sequência:
#
# 1- Subárvore esquerda
# 2- Subárvore direita
# 3- Raiz
#
# Essa ordem produz exatamente a notação pós-fixa da expressão. Por consta disso, ao percorrer uma árvore de expressão em pós-ordem, obtemos a mesma sequência usada para construir a árvore.
# ---
# 5- Para uma árvore com n nós, qual a complexidade de tempo para calcular toda a expressão? Justifique.
# ---
# A complexidade é O(n).
#
# Isso acontece porque cada nó da árvore é visitado exatamente uma vez durante a avaliação recursiva. Os nós folha retornam seus valores e os nós operadores executam apenas uma operação constante. Portanto o crescimento é linear.
# ---
# 6- O que determina a quantidade máxima de chamadas recursivas simultâneas?
# ---
# A quantidade máxima de chamadas recursivas simultâneas é determinada pela altura da árvore.

