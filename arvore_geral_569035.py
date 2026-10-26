class NoGeral:
    def __init__(self, dado):
        self.dado = dado
        self.filhos = []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)


class ArvoreGeral:
    def __init__(self):
        self.raiz = None

    def criar_raiz(self, dado):
        if self.raiz is not None:
            raise ValueError("A arvore ja possui raiz.")
        self.raiz = NoGeral(dado)
        return self.raiz

    def inserir(self, pai, dado):
        if pai is None:
            raise ValueError("O no pai nao foi informado.")
        novo = NoGeral(dado)
        pai.adicionar_filho(novo)
        return novo

    def pre_ordem(self, no):
        if no is None:
            return
        print(no.dado)
        for filho in no.filhos:
            self.pre_ordem(filho)

    def mostrar(self, no, nivel=0):
        if no is None:
            return
        print("    " * nivel + str(no.dado))
        for filho in no.filhos:
            self.mostrar(filho, nivel + 1)

    def buscar(self, no, valor):
        if no is None:
            return None
        if no.dado == valor:
            return no
        for filho in no.filhos:
            encontrado = self.buscar(filho, valor)
            if encontrado is not None:
                return encontrado
        return None

    def contar_nos(self, no):
        if no is None:
            return 0
        total = 1
        for filho in no.filhos:
            total += self.contar_nos(filho)
        return total

    def altura(self, no):
        # Convencao do tutorial: arvore vazia = 0; folha = 1.
        if no is None:
            return 0
        maior_altura = 0
        for filho in no.filhos:
            altura_filho = self.altura(filho)
            if altura_filho > maior_altura:
                maior_altura = altura_filho
        return 1 + maior_altura

    def listar_folhas(self, no):
        if no is None:
            return
        if len(no.filhos) == 0:
            print(no.dado)
            return
        for filho in no.filhos:
            self.listar_folhas(filho)

    def contar_folhas(self, no):
        if no is None:
            return 0
        if len(no.filhos) == 0:
            return 1
        total = 0
        for filho in no.filhos:
            total += self.contar_folhas(filho)
        return total

    def grau_arvore(self, no):
        if no is None:
            return 0
        maior_grau = len(no.filhos)
        for filho in no.filhos:
            grau_filho = self.grau_arvore(filho)
            if grau_filho > maior_grau:
                maior_grau = grau_filho
        return maior_grau

    def inserir_por_valor(self, valor_pai, dado):
        pai = self.buscar(self.raiz, valor_pai)
        if pai is None:
            return None
        return self.inserir(pai, dado)


def montar_arvore_inicial():
    arvore = ArvoreGeral()
    instituicao = arvore.criar_raiz("Instituicao")
    graduacao = arvore.inserir(instituicao, "Graduacao")
    pos = arvore.inserir(instituicao, "Pos-graduacao")
    arvore.inserir(graduacao, "Ciencia da Computacao")
    arvore.inserir(graduacao, "Sistemas de Informacao")
    arvore.inserir(pos, "Mestrado")
    arvore.inserir_por_valor("Graduacao", "Engenharia de Software")
    return arvore


def montar_arvore_desafio():
    arvore = ArvoreGeral()
    instituicao = arvore.criar_raiz("Instituicao")

    graduacao = arvore.inserir(instituicao, "Graduacao")
    arvore.inserir(graduacao, "Ciencia da Computacao")
    arvore.inserir(graduacao, "Sistemas de Informacao")
    arvore.inserir(graduacao, "Engenharia de Software")

    pos = arvore.inserir(instituicao, "Pos-graduacao")
    arvore.inserir(pos, "Especializacao")
    arvore.inserir(pos, "Mestrado")

    administracao = arvore.inserir(instituicao, "Administracao")
    arvore.inserir(administracao, "Secretaria")
    arvore.inserir(administracao, "Biblioteca")

    return arvore


def executar_testes():
    print("===== TESTES DA ARVORE GERAL =====")
    arvore = montar_arvore_inicial()
    print("\nHierarquia inicial:")
    arvore.mostrar(arvore.raiz)
    print("Total de nos:", arvore.contar_nos(arvore.raiz))
    print("Altura:", arvore.altura(arvore.raiz))
    print("Filhos da raiz:", len(arvore.raiz.filhos))
    graduacao = arvore.buscar(arvore.raiz, "Graduacao")
    print("Filhos de Graduacao:", len(graduacao.filhos))
    print("Busca por Mestrado:", "Encontrado" if arvore.buscar(arvore.raiz, "Mestrado") else "Nao encontrado")
    print("Busca por Doutorado:", "Encontrado" if arvore.buscar(arvore.raiz, "Doutorado") else "Nao encontrado")
    print("Quantidade de folhas:", arvore.contar_folhas(arvore.raiz))

    print("\n===== DESAFIO PRATICO =====")
    desafio = montar_arvore_desafio()
    desafio.mostrar(desafio.raiz)
    print("Total de nos:", desafio.contar_nos(desafio.raiz))
    print("Altura:", desafio.altura(desafio.raiz))
    print("Quantidade de folhas:", desafio.contar_folhas(desafio.raiz))
    print("Grau da arvore:", desafio.grau_arvore(desafio.raiz))

    print("\n===== TESTES DE CASOS ESPECIAIS =====")
    vazia = ArvoreGeral()
    print("Arvore vazia - nos:", vazia.contar_nos(vazia.raiz))
    print("Arvore vazia - altura:", vazia.altura(vazia.raiz))
    unica = ArvoreGeral()
    unica.criar_raiz("Unica")
    print("Apenas raiz - nos:", unica.contar_nos(unica.raiz))
    print("Apenas raiz - altura:", unica.altura(unica.raiz))
    print("Apenas raiz - folhas:", unica.contar_folhas(unica.raiz))
    print("Insercao com pai inexistente:", arvore.inserir_por_valor("Pai inexistente", "Novo no"))


def menu():
    arvore = montar_arvore_inicial()

    while True:
        print("\n===== MENU - ARVORE GERAL =====")
        print("1 - Mostrar hierarquia")
        print("2 - Percurso em pre-ordem")
        print("3 - Buscar valor")
        print("4 - Inserir filho pelo nome do pai")
        print("5 - Contar nos")
        print("6 - Mostrar altura")
        print("7 - Listar folhas")
        print("8 - Contar folhas")
        print("9 - Mostrar grau da arvore")
        print("10 - Executar testes")
        print("0 - Encerrar")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            arvore.mostrar(arvore.raiz)
        elif opcao == "2":
            arvore.pre_ordem(arvore.raiz)
        elif opcao == "3":
            valor = input("Digite o valor para buscar: ").strip()
            resultado = arvore.buscar(arvore.raiz, valor)
            print("Encontrado:", resultado.dado if resultado else "Nao encontrado.")
        elif opcao == "4":
            pai = input("Nome do no pai: ").strip()
            dado = input("Nome do novo no: ").strip()
            if not pai or not dado:
                print("Os campos nao podem ficar vazios.")
            else:
                novo = arvore.inserir_por_valor(pai, dado)
                if novo is None:
                    print("No pai nao encontrado. A arvore nao foi alterada.")
                else:
                    print("No inserido com sucesso.")
        elif opcao == "5":
            print("Total de nos:", arvore.contar_nos(arvore.raiz))
        elif opcao == "6":
            print("Altura:", arvore.altura(arvore.raiz))
        elif opcao == "7":
            print("Folhas:")
            arvore.listar_folhas(arvore.raiz)
        elif opcao == "8":
            print("Quantidade de folhas:", arvore.contar_folhas(arvore.raiz))
        elif opcao == "9":
            print("Grau da arvore:", arvore.grau_arvore(arvore.raiz))
        elif opcao == "10":
            executar_testes()
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    executar_testes()
    menu()

    #
