"""
================================================================================
  ÁRVORES BINÁRIAS E MUITO MAIS — Guia Completo em Python
================================================================================
  Autor  : Programador Python
  Versão : 1.0
  Temas  :
    1. Nó e Árvore Binária de Busca (BST)
    2. Traversals: In-order, Pre-order, Post-order, Level-order (BFS)
    3. Operações: Inserção, Busca, Remoção
    4. Propriedades: Altura, Profundidade, Balanceamento
    5. Árvore AVL (auto-balanceada)
    6. Árvore de Expressão Aritmética
    7. Visualização gráfica no terminal
    8. Testes automatizados
================================================================================
"""

# ── Importações necessárias ───────────────────────────────────────────────────
from __future__ import annotations          # Permite anotações de tipo forward
from collections import deque               # Fila eficiente para BFS (O(1) no início)
from typing import Optional, List, Any      # Tipagem estática para clareza
import textwrap                             # Formatação de texto


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  PARTE 1 — NÓ DA ÁRVORE BINÁRIA
# ╚══════════════════════════════════════════════════════════════════════════════

class No:
    """
    Representa um único nó de uma árvore binária.

    Cada nó armazena:
      - valor   : o dado guardado neste nó
      - esquerdo: referência ao filho esquerdo (ou None se não existir)
      - direito : referência ao filho direito  (ou None se não existir)

    Visualização de um nó com dois filhos:
           [10]          ← nó pai (valor = 10)
          /    \\
        [5]   [15]       ← filhos esquerdo e direito
    """

    def __init__(self, valor: int):
        # O valor/dado armazenado no nó
        self.valor: int = valor

        # Ponteiro para o filho esquerdo (valores MENORES que este nó, na BST)
        self.esquerdo: Optional[No] = None

        # Ponteiro para o filho direito (valores MAIORES que este nó, na BST)
        self.direito: Optional[No] = None

        # Fator de balanceamento — usado apenas na Árvore AVL (Parte 5)
        self.altura: int = 1

    def __repr__(self) -> str:
        """Representação legível do nó, útil para debug."""
        return f"No({self.valor})"


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  PARTE 2 — ÁRVORE BINÁRIA DE BUSCA (BST — Binary Search Tree)
# ╚══════════════════════════════════════════════════════════════════════════════

class ArvoreBinariaBusca:
    """
    Árvore Binária de Busca (BST).

    PROPRIEDADE FUNDAMENTAL:
      Para qualquer nó N:
        • Todos os nós na subárvore ESQUERDA têm valor < N.valor
        • Todos os nós na subárvore DIREITA  têm valor > N.valor

    COMPLEXIDADE DAS OPERAÇÕES:
      ┌─────────────┬────────────┬────────────┐
      │ Operação    │  Médio     │  Pior caso │
      ├─────────────┼────────────┼────────────┤
      │ Inserção    │  O(log n)  │  O(n)      │
      │ Busca       │  O(log n)  │  O(n)      │
      │ Remoção     │  O(log n)  │  O(n)      │
      └─────────────┴────────────┴────────────┘
      * O pior caso O(n) ocorre quando a árvore vira uma lista ligada
        (inserção em ordem crescente/decrescente sem balanceamento).
    """

    def __init__(self):
        # A raiz é o ponto de entrada da árvore; começa vazia (None)
        self.raiz: Optional[No] = None

    # ── 2.1 INSERÇÃO ─────────────────────────────────────────────────────────

    def inserir(self, valor: int) -> None:
        """
        Insere um valor na BST mantendo a propriedade da árvore.

        Algoritmo:
          1. Se a árvore está vazia, cria a raiz.
          2. Caso contrário, chama o auxiliar recursivo.
        """
        if self.raiz is None:
            self.raiz = No(valor)
        else:
            self._inserir_recursivo(self.raiz, valor)

    def _inserir_recursivo(self, no_atual: No, valor: int) -> None:
        """
        Auxiliar privado (prefixo '_') — percorre a árvore recursivamente
        até encontrar a posição correta para inserir o novo valor.

        Exemplo de inserção do valor 7 em: 10 → 5 → 15
                 10
                /  \\
               5   15
               ↓
          inserir 7: 7 > 5, vai para DIREITA de 5
                 10
                /  \\
               5   15
                \\
                 7
        """
        if valor < no_atual.valor:
            # O valor é MENOR → vai para a subárvore ESQUERDA
            if no_atual.esquerdo is None:
                no_atual.esquerdo = No(valor)          # Posição encontrada!
            else:
                self._inserir_recursivo(no_atual.esquerdo, valor)  # Desce mais
        elif valor > no_atual.valor:
            # O valor é MAIOR → vai para a subárvore DIREITA
            if no_atual.direito is None:
                no_atual.direito = No(valor)           # Posição encontrada!
            else:
                self._inserir_recursivo(no_atual.direito, valor)   # Desce mais
        # Se valor == no_atual.valor: ignora duplicatas (comportamento padrão)

    # ── 2.2 BUSCA ─────────────────────────────────────────────────────────────

    def buscar(self, valor: int) -> bool:
        """
        Verifica se um valor existe na BST.

        Retorna True se encontrado, False caso contrário.
        A busca aproveita a propriedade da BST: a cada nó visitado,
        descartamos metade da árvore restante — como a busca binária em arrays.
        """
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, no_atual: Optional[No], valor: int) -> bool:
        """
        Percorre recursivamente comparando o valor com cada nó.

        Casos base:
          - no_atual é None  → valor não existe na árvore
          - valor encontrado → retorna True

        Casos recursivos:
          - valor < no_atual.valor → busca na subárvore esquerda
          - valor > no_atual.valor → busca na subárvore direita
        """
        if no_atual is None:
            return False                               # Chegou ao fim: não achou
        if valor == no_atual.valor:
            return True                                # Encontrado!
        elif valor < no_atual.valor:
            return self._buscar_recursivo(no_atual.esquerdo, valor)
        else:
            return self._buscar_recursivo(no_atual.direito, valor)

    # ── 2.3 REMOÇÃO ──────────────────────────────────────────────────────────

    def remover(self, valor: int) -> None:
        """
        Remove um valor da BST mantendo a propriedade da árvore.

        Três casos possíveis:
          CASO 1: Nó é folha (sem filhos)         → simplesmente remove
          CASO 2: Nó tem apenas UM filho           → filho sobe no lugar do pai
          CASO 3: Nó tem DOIS filhos               → substitui pelo sucessor
                  (menor valor da subárvore direita)
        """
        self.raiz = self._remover_recursivo(self.raiz, valor)

    def _remover_recursivo(self, no_atual: Optional[No], valor: int) -> Optional[No]:
        """
        Auxiliar recursivo para remoção.

        Retorna o nó (possivelmente modificado) para reconectar a árvore.

        Exemplo — remover 10 de:
               10
              /  \\
             5   15
                /
               12

        Passo 1: 10 tem dois filhos → encontra sucessor = 12 (mínimo da direita)
        Passo 2: Copia 12 para onde estava 10
        Passo 3: Remove 12 da subárvore direita

        Resultado:
               12
              /  \\
             5   15
        """
        if no_atual is None:
            return None                                # Valor não encontrado

        if valor < no_atual.valor:
            # Valor está na subárvore ESQUERDA
            no_atual.esquerdo = self._remover_recursivo(no_atual.esquerdo, valor)

        elif valor > no_atual.valor:
            # Valor está na subárvore DIREITA
            no_atual.direito = self._remover_recursivo(no_atual.direito, valor)

        else:
            # ── ENCONTRAMOS o nó a remover ──────────────────────────────────

            # CASO 1 e 2: Sem filho esquerdo → filho direito (ou None) sobe
            if no_atual.esquerdo is None:
                return no_atual.direito

            # CASO 2: Sem filho direito → filho esquerdo sobe
            if no_atual.direito is None:
                return no_atual.esquerdo

            # CASO 3: Dois filhos → encontra o SUCESSOR IN-ORDER
            # (menor valor da subárvore DIREITA)
            sucessor = self._minimo(no_atual.direito)

            # Copia o valor do sucessor para o nó atual
            no_atual.valor = sucessor.valor

            # Remove o sucessor da subárvore direita (ele tem no máx. 1 filho)
            no_atual.direito = self._remover_recursivo(no_atual.direito, sucessor.valor)

        return no_atual

    def _minimo(self, no: No) -> No:
        """
        Encontra o nó com o MENOR valor em uma subárvore.
        Na BST, o mínimo está sempre no nó mais à ESQUERDA.
        """
        atual = no
        while atual.esquerdo is not None:
            atual = atual.esquerdo
        return atual

    # ── 2.4 PROPRIEDADES DA ÁRVORE ────────────────────────────────────────────

    def altura(self, no: Optional[No] = None) -> int:
        """
        Calcula a ALTURA da árvore (ou de uma subárvore).

        Altura = número de ARESTAS no caminho mais longo da raiz até uma folha.

        Exemplos:
          Árvore vazia           → altura = -1
          Apenas a raiz          → altura =  0
          Raiz com 1 filho       → altura =  1
          Raiz com 2 níveis      → altura =  2

        A altura é calculada como:
          altura(nó) = 1 + max(altura(esquerdo), altura(direito))
        """
        # Permite chamar sem argumento: arvore.altura() usa a raiz
        if no is None and self.raiz is None:
            return -1
        alvo = no if no is not None else self.raiz
        return self._altura_recursiva(alvo)

    def _altura_recursiva(self, no: Optional[No]) -> int:
        """Auxiliar recursivo para cálculo de altura."""
        if no is None:
            return -1                                  # Folha virtual: -1
        altura_esq = self._altura_recursiva(no.esquerdo)
        altura_dir = self._altura_recursiva(no.direito)
        return 1 + max(altura_esq, altura_dir)

    def contar_nos(self) -> int:
        """
        Conta o total de nós na árvore.
        Percorre cada nó uma vez → O(n).
        """
        return self._contar_recursivo(self.raiz)

    def _contar_recursivo(self, no: Optional[No]) -> int:
        """Conta: 0 se vazio, senão 1 (este nó) + filhos esq + filhos dir."""
        if no is None:
            return 0
        return 1 + self._contar_recursivo(no.esquerdo) + self._contar_recursivo(no.direito)

    def esta_balanceada(self) -> bool:
        """
        Verifica se a árvore está BALANCEADA.

        Uma árvore é balanceada se, para CADA nó, a diferença de altura
        entre a subárvore esquerda e a direita é no máximo 1.

        Árvore balanceada:        Árvore desbalanceada:
              10                        10
             /  \\                      /
            5   15                    5
           / \\                       /
          3   7                     3
        """
        return self._verificar_balanco(self.raiz) != -2

    def _verificar_balanco(self, no: Optional[No]) -> int:
        """
        Retorna a altura do nó se balanceado, ou -2 como código de erro.
        Combina verificação e cálculo em uma única passagem O(n).
        """
        if no is None:
            return -1
        alt_esq = self._verificar_balanco(no.esquerdo)
        if alt_esq == -2:
            return -2                                  # Já detectou desbalanceamento
        alt_dir = self._verificar_balanco(no.direito)
        if alt_dir == -2:
            return -2
        if abs(alt_esq - alt_dir) > 1:
            return -2                                  # Fator de balanceamento > 1
        return 1 + max(alt_esq, alt_dir)


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  PARTE 3 — TRAVERSALS (PERCURSOS)
# ╚══════════════════════════════════════════════════════════════════════════════

class Traversals:
    """
    Diferentes formas de PERCORRER uma árvore binária.

    Para a árvore:
              10
             /  \\
            5   15
           / \\    \\
          3   7   20

    Resultados:
      In-order    (Esq → Raiz → Dir) : [3, 5, 7, 10, 15, 20]  ← ordem crescente!
      Pre-order   (Raiz → Esq → Dir) : [10, 5, 3, 7, 15, 20]  ← útil p/ cópia
      Post-order  (Esq → Dir → Raiz) : [3, 7, 5, 20, 15, 10]  ← útil p/ deleção
      Level-order (nível por nível)   : [10, 5, 15, 3, 7, 20]  ← usa fila (BFS)
    """

    @staticmethod
    def in_order(no: Optional[No], resultado: Optional[List[int]] = None) -> List[int]:
        """
        IN-ORDER: Esquerda → Raiz → Direita

        Na BST, in-order produz os valores em ORDEM CRESCENTE.
        Isso ocorre porque na BST: esq < raiz < dir.

        Uso comum: imprimir elementos em ordem, verificar se BST é válida.
        """
        if resultado is None:
            resultado = []
        if no is not None:
            Traversals.in_order(no.esquerdo, resultado)   # 1. Visita esquerda
            resultado.append(no.valor)                    # 2. Processa raiz
            Traversals.in_order(no.direito, resultado)    # 3. Visita direita
        return resultado

    @staticmethod
    def pre_order(no: Optional[No], resultado: Optional[List[int]] = None) -> List[int]:
        """
        PRE-ORDER: Raiz → Esquerda → Direita

        O nó PAI é processado ANTES dos filhos.
        Uso comum: copiar/serializar a árvore (preserva estrutura para reconstrução).
        """
        if resultado is None:
            resultado = []
        if no is not None:
            resultado.append(no.valor)                    # 1. Processa raiz primeiro
            Traversals.pre_order(no.esquerdo, resultado)  # 2. Visita esquerda
            Traversals.pre_order(no.direito, resultado)   # 3. Visita direita
        return resultado

    @staticmethod
    def post_order(no: Optional[No], resultado: Optional[List[int]] = None) -> List[int]:
        """
        POST-ORDER: Esquerda → Direita → Raiz

        Os filhos são processados ANTES do pai.
        Uso comum: deletar uma árvore (deleta filhos antes do pai),
                   avaliar expressões aritméticas (ver Parte 6).
        """
        if resultado is None:
            resultado = []
        if no is not None:
            Traversals.post_order(no.esquerdo, resultado) # 1. Visita esquerda
            Traversals.post_order(no.direito, resultado)  # 2. Visita direita
            resultado.append(no.valor)                    # 3. Processa raiz por último
        return resultado

    @staticmethod
    def level_order(raiz: Optional[No]) -> List[List[int]]:
        """
        LEVEL-ORDER (BFS — Busca em Largura): nível por nível.

        Usa uma FILA (deque) para processar nós na ordem em que foram descobertos.

        Processo visual para a árvore acima:
          Fila inicial: [10]
          Nível 0: processa 10 → enfileira 5, 15  → resultado: [[10]]
          Nível 1: processa 5  → enfileira 3, 7
                   processa 15 → enfileira 20      → resultado: [[10],[5,15]]
          Nível 2: processa 3, 7, 20               → resultado: [[10],[5,15],[3,7,20]]

        Uso comum: imprimir árvore por níveis, encontrar o nó mais próximo da raiz.
        Complexidade: O(n) tempo, O(n) espaço (fila pode ter até n/2 nós).
        """
        if raiz is None:
            return []

        resultado: List[List[int]] = []
        fila: deque = deque([raiz])                    # Fila começa com a raiz

        while fila:
            tamanho_nivel = len(fila)                  # Quantos nós há NESTE nível
            nivel_atual: List[int] = []

            for _ in range(tamanho_nivel):
                no = fila.popleft()                    # Remove da frente da fila
                nivel_atual.append(no.valor)

                # Enfileira os filhos para o PRÓXIMO nível
                if no.esquerdo:
                    fila.append(no.esquerdo)
                if no.direito:
                    fila.append(no.direito)

            resultado.append(nivel_atual)

        return resultado


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  PARTE 4 — VISUALIZAÇÃO NO TERMINAL
# ╚══════════════════════════════════════════════════════════════════════════════

class Visualizador:
    """
    Exibe a árvore de forma visual no terminal.

    Exemplo de saída:
            ____10____
           /          \\
         _5_          _15_
        /   \\              \\
       3     7             20
    """

    @staticmethod
    def imprimir(raiz: Optional[No], titulo: str = "Árvore") -> None:
        """
        Ponto de entrada da visualização.
        Usa BFS para calcular as posições e depois imprime linha a linha.
        """
        print(f"\n{'═' * 50}")
        print(f"  {titulo}")
        print('═' * 50)

        if raiz is None:
            print("  (árvore vazia)")
            print('═' * 50)
            return

        # Coleta todos os nós com seus níveis usando BFS
        niveis = Traversals.level_order(raiz)
        altura_total = len(niveis)

        for i, nivel in enumerate(niveis):
            # Calcula espaçamento proporcional à profundidade
            espacamento = 2 ** (altura_total - i)
            padding = ' ' * (espacamento // 2)
            espaco_entre = ' ' * espacamento

            linha = padding
            for j, val in enumerate(nivel):
                if val is not None:
                    linha += f"{val:^3}"
                else:
                    linha += '   '
                if j < len(nivel) - 1:
                    linha += espaco_entre

            print(linha)

            # Desenha as conexões entre níveis
            if i < altura_total - 1:
                conn = ' ' * (espacamento // 2 - 1)
                for j in range(len(nivel)):
                    conn += '/ \\'
                    if j < len(nivel) - 1:
                        conn += ' ' * (espacamento - 1)
                print(conn)

        print('═' * 50)

    @staticmethod
    def imprimir_simples(raiz: Optional[No], prefixo: str = "", eh_esquerdo: bool = True) -> None:
        """
        Visualização alternativa tipo 'tree' do terminal — mais compacta.

        Saída:
          10
          ├── 5
          │   ├── 3
          │   └── 7
          └── 15
              └── 20
        """
        if raiz is not None:
            print(prefixo + ("├── " if eh_esquerdo else "└── ") + str(raiz.valor))
            novo_prefixo = prefixo + ("│   " if eh_esquerdo else "    ")
            if raiz.esquerdo or raiz.direito:
                Visualizador.imprimir_simples(raiz.esquerdo, novo_prefixo, True)
                Visualizador.imprimir_simples(raiz.direito, novo_prefixo, False)


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  PARTE 5 — ÁRVORE AVL (AUTO-BALANCEADA)
# ╚══════════════════════════════════════════════════════════════════════════════

class ArvoreAVL:
    """
    Árvore AVL — inventada por Adelson-Velsky e Landis (1962).

    Resolve o problema da BST degenerada: ao inserir valores em ordem
    crescente na BST comum, ela vira uma lista ligada (O(n) para tudo).

    A AVL garante que o FATOR DE BALANCEAMENTO de cada nó seja -1, 0 ou 1.

    FATOR DE BALANCEAMENTO = altura(subárvore esquerda) - altura(subárvore direita)

    Quando o fator sai desse intervalo, rotações são aplicadas para rebalancear.

    TIPOS DE ROTAÇÃO:
      - Rotação Simples à Direita  (LL — desbalanceamento à esquerda-esquerda)
      - Rotação Simples à Esquerda (RR — desbalanceamento à direita-direita)
      - Rotação Dupla Esq-Dir      (LR — esquerda-direita)
      - Rotação Dupla Dir-Esq      (RL — direita-esquerda)
    """

    def __init__(self):
        self.raiz: Optional[No] = None

    # ── Funções auxiliares AVL ────────────────────────────────────────────────

    def _get_altura(self, no: Optional[No]) -> int:
        """Retorna a altura armazenada no nó, ou 0 se None."""
        return no.altura if no else 0

    def _atualizar_altura(self, no: No) -> None:
        """Recalcula e armazena a altura de um nó após modificações."""
        no.altura = 1 + max(self._get_altura(no.esquerdo),
                            self._get_altura(no.direito))

    def _fator_balanco(self, no: Optional[No]) -> int:
        """
        Calcula o fator de balanceamento: altura(esq) - altura(dir).
        AVL exige que este valor esteja em {-1, 0, 1}.
        """
        if no is None:
            return 0
        return self._get_altura(no.esquerdo) - self._get_altura(no.direito)

    # ── Rotações ──────────────────────────────────────────────────────────────

    def _rotacao_direita(self, z: No) -> No:
        """
        ROTAÇÃO SIMPLES À DIREITA — corrige desbalanceamento LL.

        Antes:          Depois:
            z               y
           / \\             / \\
          y   T4           x   z
         / \\             / \\ / \\
        x   T3          T1 T2 T3 T4

        O nó 'y' sobe, 'z' desce para a direita.
        O filho direito de 'y' (T3) vai para o filho esquerdo de 'z'.
        """
        y = z.esquerdo          # y é o filho esquerdo de z
        T3 = y.direito          # T3 é o filho direito de y (será movido)

        # Realiza a rotação
        y.direito = z           # z desce → vira filho direito de y
        z.esquerdo = T3         # T3 vai para o lugar que era de y em z

        # Atualiza alturas (z primeiro porque agora está abaixo de y)
        self._atualizar_altura(z)
        self._atualizar_altura(y)

        return y                # y é a nova raiz desta subárvore

    def _rotacao_esquerda(self, z: No) -> No:
        """
        ROTAÇÃO SIMPLES À ESQUERDA — corrige desbalanceamento RR.

        Antes:          Depois:
          z                 y
         / \\              / \\
        T1   y            z   x
            / \\          / \\ / \\
           T2  x        T1 T2 T3 T4

        O nó 'y' sobe, 'z' desce para a esquerda.
        """
        y = z.direito           # y é o filho direito de z
        T2 = y.esquerdo         # T2 será movido para z

        # Realiza a rotação
        y.esquerdo = z          # z desce → vira filho esquerdo de y
        z.direito = T2          # T2 vai para o lugar que era de y em z

        # Atualiza alturas
        self._atualizar_altura(z)
        self._atualizar_altura(y)

        return y                # y é a nova raiz desta subárvore

    # ── Inserção AVL ─────────────────────────────────────────────────────────

    def inserir(self, valor: int) -> None:
        """Insere um valor e rebalanceia automaticamente se necessário."""
        self.raiz = self._inserir_avl(self.raiz, valor)

    def _inserir_avl(self, no: Optional[No], valor: int) -> No:
        """
        Insere como BST comum, depois verifica e corrige o balanceamento
        ao RETORNAR da recursão (bottom-up).

        Os 4 casos de desbalanceamento após inserção:
          LL: inseriu à esquerda do filho esquerdo  → rotação direita
          RR: inseriu à direita do filho direito    → rotação esquerda
          LR: inseriu à direita do filho esquerdo  → rot. esq. + rot. dir.
          RL: inseriu à esquerda do filho direito  → rot. dir. + rot. esq.
        """
        # ── Passo 1: inserção BST normal ─────────────────────────────────────
        if no is None:
            return No(valor)

        if valor < no.valor:
            no.esquerdo = self._inserir_avl(no.esquerdo, valor)
        elif valor > no.valor:
            no.direito = self._inserir_avl(no.direito, valor)
        else:
            return no           # Duplicata: ignora

        # ── Passo 2: atualiza altura do nó atual ─────────────────────────────
        self._atualizar_altura(no)

        # ── Passo 3: verifica o fator de balanceamento ───────────────────────
        fb = self._fator_balanco(no)

        # CASO LL: desequilíbrio à esquerda, valor inserido à esquerda
        if fb > 1 and valor < no.esquerdo.valor:
            return self._rotacao_direita(no)

        # CASO RR: desequilíbrio à direita, valor inserido à direita
        if fb < -1 and valor > no.direito.valor:
            return self._rotacao_esquerda(no)

        # CASO LR: desequilíbrio à esquerda, valor inserido à direita
        if fb > 1 and valor > no.esquerdo.valor:
            no.esquerdo = self._rotacao_esquerda(no.esquerdo)  # Rotação dupla
            return self._rotacao_direita(no)

        # CASO RL: desequilíbrio à direita, valor inserido à esquerda
        if fb < -1 and valor < no.direito.valor:
            no.direito = self._rotacao_direita(no.direito)     # Rotação dupla
            return self._rotacao_esquerda(no)

        return no               # Nó balanceado: retorna sem alteração


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  PARTE 6 — ÁRVORE DE EXPRESSÃO ARITMÉTICA
# ╚══════════════════════════════════════════════════════════════════════════════

class NoExpressao:
    """
    Nó especial para expressões aritméticas.
    Pode armazenar um número (folha) ou um operador (+, -, *, /).
    """
    def __init__(self, valor: Any):
        self.valor = valor
        self.esquerdo: Optional[NoExpressao] = None
        self.direito: Optional[NoExpressao] = None


class ArvoreExpressao:
    """
    Representa expressões aritméticas como árvore binária.

    Para a expressão: (3 + 5) * (2 - 1)

    Árvore resultante:
              *
            /   \\
           +     -
          / \\   / \\
         3   5 2   1

    Regras:
      - Folhas (sem filhos) são sempre NÚMEROS
      - Nós internos são sempre OPERADORES (+, -, *, /)
      - Post-order traversal = notação pós-fixada (RPN)
      - Pre-order traversal  = notação pré-fixada (prefixada)
      - In-order  traversal  = notação infixada (a expressão normal)
    """

    def __init__(self):
        self.raiz: Optional[NoExpressao] = None

    def construir(self, operador: str,
                  esq_val: Any, dir_val: Any,
                  esq_op: Optional[str] = None,
                  dir_op: Optional[str] = None,
                  esq_esq: Any = None, esq_dir: Any = None,
                  dir_esq: Any = None, dir_dir: Any = None) -> None:
        """
        Constrói manualmente a árvore (3 + 5) * (2 - 1).
        Em produção, usaria-se um parser completo com tokenização.
        """
        self.raiz = NoExpressao(operador)

        # Constrói subárvore ESQUERDA
        if esq_op:
            self.raiz.esquerdo = NoExpressao(esq_op)
            self.raiz.esquerdo.esquerdo = NoExpressao(esq_val)
            self.raiz.esquerdo.direito = NoExpressao(dir_val)
        else:
            self.raiz.esquerdo = NoExpressao(esq_val)

        # Constrói subárvore DIREITA
        if dir_op:
            self.raiz.direito = NoExpressao(dir_op)
            self.raiz.direito.esquerdo = NoExpressao(dir_esq)
            self.raiz.direito.direito = NoExpressao(dir_dir)
        else:
            self.raiz.direito = NoExpressao(dir_val)

    def avaliar(self, no: Optional[NoExpressao] = None) -> float:
        """
        Avalia a expressão percorrendo a árvore em POST-ORDER.

        Estratégia:
          1. Avalia a subárvore esquerda (obtém resultado parcial)
          2. Avalia a subárvore direita  (obtém resultado parcial)
          3. Aplica o operador do nó atual nos dois resultados

        Isso é exatamente o que Post-order faz: filhos antes do pai.
        """
        if no is None:
            no = self.raiz

        # Caso base: nó folha (é um número)
        if no.esquerdo is None and no.direito is None:
            return float(no.valor)

        # Avalia recursivamente os dois lados
        val_esq = self.avaliar(no.esquerdo)
        val_dir = self.avaliar(no.direito)

        # Aplica o operador
        operadores = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else float('inf')
        }

        operacao = operadores.get(no.valor)
        if operacao is None:
            raise ValueError(f"Operador desconhecido: '{no.valor}'")

        return operacao(val_esq, val_dir)

    def para_string_inorder(self, no: Optional[NoExpressao] = None) -> str:
        """Converte a árvore de volta para expressão infixada com parênteses."""
        if no is None:
            no = self.raiz
        if no is None:
            return ""
        if no.esquerdo is None and no.direito is None:
            return str(no.valor)
        esq = self.para_string_inorder(no.esquerdo)
        dir_ = self.para_string_inorder(no.direito)
        return f"({esq} {no.valor} {dir_})"


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  PARTE 7 — FUNÇÕES UTILITÁRIAS
# ╚══════════════════════════════════════════════════════════════════════════════

def construir_bst_de_lista(valores: List[int]) -> ArvoreBinariaBusca:
    """
    Função conveniente: cria uma BST a partir de uma lista de inteiros.

    Exemplo: construir_bst_de_lista([10, 5, 15, 3, 7, 20])
    """
    arvore = ArvoreBinariaBusca()
    for v in valores:
        arvore.inserir(v)
    return arvore


def verificar_bst_valida(raiz: Optional[No],
                          minimo: float = float('-inf'),
                          maximo: float = float('inf')) -> bool:
    """
    Verifica se uma árvore binária é uma BST VÁLIDA.

    Percorre a árvore passando intervalos válidos para cada nó.
    Cada nó deve estar dentro do intervalo (minimo, maximo).

    Este é um algoritmo clássico de entrevistas técnicas!
    """
    if raiz is None:
        return True            # Árvore vazia é BST válida

    # O valor deste nó deve estar dentro do intervalo permitido
    if not (minimo < raiz.valor < maximo):
        return False

    # Subárvore esquerda: valores devem ser < raiz.valor
    # Subárvore direita:  valores devem ser > raiz.valor
    return (verificar_bst_valida(raiz.esquerdo, minimo, raiz.valor) and
            verificar_bst_valida(raiz.direito, raiz.valor, maximo))


def lca(raiz: Optional[No], p: int, q: int) -> Optional[int]:
    """
    LCA — Lowest Common Ancestor (Ancestral Comum Mais Próximo).

    Encontra o nó mais profundo que é ancestral de AMBOS p e q.

    Algoritmo para BST (muito eficiente):
      - Se p e q são ambos menores que raiz → LCA está na esquerda
      - Se p e q são ambos maiores que raiz → LCA está na direita
      - Caso contrário: a raiz atual É o LCA

    Exemplo: LCA(3, 7) = 5 na árvore abaixo:
              10
             /  \\
            5   15
           / \\
          3   7
    """
    if raiz is None:
        return None

    if p < raiz.valor and q < raiz.valor:
        return lca(raiz.esquerdo, p, q)   # Ambos à esquerda

    if p > raiz.valor and q > raiz.valor:
        return lca(raiz.direito, p, q)    # Ambos à direita

    return raiz.valor                      # Divisão ocorre aqui → é o LCA


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  PARTE 8 — TESTES AUTOMATIZADOS
# ╚══════════════════════════════════════════════════════════════════════════════

class TestesAutomatizados:
    """
    Bateria de testes para verificar a corretude de todas as implementações.
    Não usa pytest — apenas lógica Python pura para manter as dependências mínimas.
    """

    def __init__(self):
        self.total = 0
        self.passou = 0
        self.falhou = 0

    def afirmar(self, condicao: bool, mensagem: str) -> None:
        """
        Verifica uma condição e registra o resultado.
        Similar ao 'assert' mas com relatório detalhado.
        """
        self.total += 1
        if condicao:
            self.passou += 1
            print(f"  ✅ {mensagem}")
        else:
            self.falhou += 1
            print(f"  ❌ FALHOU: {mensagem}")

    def executar_todos(self) -> None:
        """Executa todos os grupos de testes."""
        print("\n" + "═" * 50)
        print("  TESTES AUTOMATIZADOS")
        print("═" * 50)

        self._testar_bst()
        self._testar_traversals()
        self._testar_avl()
        self._testar_expressao()
        self._testar_utilitarios()

        print("\n" + "─" * 50)
        print(f"  Resultado: {self.passou}/{self.total} testes passaram")
        if self.falhou == 0:
            print("  🎉 TODOS OS TESTES PASSARAM!")
        else:
            print(f"  ⚠️  {self.falhou} teste(s) falharam.")
        print("─" * 50)

    def _testar_bst(self) -> None:
        print("\n[BST — Árvore Binária de Busca]")
        bst = construir_bst_de_lista([10, 5, 15, 3, 7, 20])

        self.afirmar(bst.buscar(7),        "Busca: encontra 7 (existe)")
        self.afirmar(not bst.buscar(99),   "Busca: não encontra 99 (não existe)")
        self.afirmar(bst.contar_nos() == 6,"Contagem: 6 nós")
        self.afirmar(bst.altura() == 2,    "Altura: 2 (raiz=10, até 3/7/20)")
        self.afirmar(bst.esta_balanceada(),"Balanceamento: está balanceada")

        bst.remover(15)
        self.afirmar(not bst.buscar(15),   "Remoção: 15 removido com sucesso")
        self.afirmar(bst.buscar(20),       "Remoção: 20 ainda existe após remover 15")
        self.afirmar(bst.contar_nos() == 5,"Contagem após remoção: 5 nós")

    def _testar_traversals(self) -> None:
        print("\n[Traversals — Percursos]")
        bst = construir_bst_de_lista([10, 5, 15, 3, 7, 20])

        in_ord = Traversals.in_order(bst.raiz)
        self.afirmar(in_ord == [3, 5, 7, 10, 15, 20],
                     f"In-order: {in_ord} == [3,5,7,10,15,20]")

        pre_ord = Traversals.pre_order(bst.raiz)
        self.afirmar(pre_ord == [10, 5, 3, 7, 15, 20],
                     f"Pre-order: {pre_ord} == [10,5,3,7,15,20]")

        post_ord = Traversals.post_order(bst.raiz)
        self.afirmar(post_ord == [3, 7, 5, 20, 15, 10],
                     f"Post-order: {post_ord} == [3,7,5,20,15,10]")

        lvl = Traversals.level_order(bst.raiz)
        self.afirmar(lvl == [[10], [5, 15], [3, 7, 20]],
                     f"Level-order: {lvl}")

    def _testar_avl(self) -> None:
        print("\n[AVL — Árvore Auto-Balanceada]")
        avl = ArvoreAVL()

        # Inserção em ordem crescente — sem AVL viraria lista ligada
        for v in [1, 2, 3, 4, 5, 6, 7]:
            avl.inserir(v)

        # A AVL deve manter a árvore balanceada
        bst_check = ArvoreBinariaBusca()
        bst_check.raiz = avl.raiz
        self.afirmar(bst_check.esta_balanceada(),
                     "AVL: inserção 1-7 em ordem permanece balanceada")

        altura = bst_check.altura()
        self.afirmar(altura <= 3,
                     f"AVL: altura ({altura}) ≤ 3 para 7 nós (log₂7 ≈ 2.8)")

    def _testar_expressao(self) -> None:
        print("\n[Árvore de Expressão]")
        expr = ArvoreExpressao()
        # Constrói: (3 + 5) * (2 - 1)
        expr.raiz = NoExpressao('*')
        expr.raiz.esquerdo = NoExpressao('+')
        expr.raiz.esquerdo.esquerdo = NoExpressao(3)
        expr.raiz.esquerdo.direito = NoExpressao(5)
        expr.raiz.direito = NoExpressao('-')
        expr.raiz.direito.esquerdo = NoExpressao(2)
        expr.raiz.direito.direito = NoExpressao(1)

        resultado = expr.avaliar()
        self.afirmar(resultado == 8.0,
                     f"Avaliação (3+5)*(2-1) = {resultado} == 8.0")

        expressao_str = expr.para_string_inorder()
        self.afirmar("+" in expressao_str and "*" in expressao_str,
                     f"String inorder: '{expressao_str}'")

    def _testar_utilitarios(self) -> None:
        print("\n[Utilitários]")
        bst = construir_bst_de_lista([10, 5, 15, 3, 7, 20])

        self.afirmar(verificar_bst_valida(bst.raiz),
                     "Verificação BST: árvore válida reconhecida")

        # Cria árvore inválida manualmente para testar
        raiz_invalida = No(10)
        raiz_invalida.esquerdo = No(15)    # Errado! 15 > 10, deveria estar à direita
        self.afirmar(not verificar_bst_valida(raiz_invalida),
                     "Verificação BST: árvore inválida detectada")

        ancestral = lca(bst.raiz, 3, 7)
        self.afirmar(ancestral == 5, f"LCA(3,7) = {ancestral} == 5")

        ancestral2 = lca(bst.raiz, 3, 20)
        self.afirmar(ancestral2 == 10, f"LCA(3,20) = {ancestral2} == 10")


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  PARTE 9 — DEMONSTRAÇÃO PRINCIPAL
# ╚══════════════════════════════════════════════════════════════════════════════

def demonstracao_completa() -> None:
    """
    Executa uma demonstração passo a passo de todas as funcionalidades.
    Esta função serve como tutorial interativo do código.
    """

    # ── Demo 1: BST básica ────────────────────────────────────────────────────
    print("\n" + "═" * 50)
    print("  DEMO 1 — Árvore Binária de Busca (BST)")
    print("═" * 50)

    valores = [10, 5, 15, 3, 7, 20, 1, 4]
    print(f"\n📥 Inserindo valores: {valores}")
    bst = construir_bst_de_lista(valores)

    print(f"\n📊 Propriedades:")
    print(f"   Nós totais : {bst.contar_nos()}")
    print(f"   Altura     : {bst.altura()}")
    print(f"   Balanceada : {bst.esta_balanceada()}")

    print(f"\n🔍 Buscas:")
    for v in [7, 99, 1]:
        encontrado = bst.buscar(v)
        icone = "✅" if encontrado else "❌"
        print(f"   {icone} buscar({v}) → {'Encontrado' if encontrado else 'Não encontrado'}")

    # ── Demo 2: Traversals ────────────────────────────────────────────────────
    print("\n" + "═" * 50)
    print("  DEMO 2 — Traversals (Percursos)")
    print("═" * 50)

    bst2 = construir_bst_de_lista([10, 5, 15, 3, 7, 20])
    print(f"\n  In-order    (crescente): {Traversals.in_order(bst2.raiz)}")
    print(f"  Pre-order   (raiz 1º)  : {Traversals.pre_order(bst2.raiz)}")
    print(f"  Post-order  (raiz últ.): {Traversals.post_order(bst2.raiz)}")
    print(f"  Level-order (BFS)      : {Traversals.level_order(bst2.raiz)}")

    Visualizador.imprimir(bst2.raiz, "BST — Visualização")

    # ── Demo 3: Remoção ───────────────────────────────────────────────────────
    print("\n" + "═" * 50)
    print("  DEMO 3 — Remoção de Nós (3 casos)")
    print("═" * 50)

    bst3 = construir_bst_de_lista([10, 5, 15, 3, 7, 20])
    print(f"\n  Antes   : {Traversals.in_order(bst3.raiz)}")

    bst3.remover(3)     # Caso 1: folha (sem filhos)
    print(f"  Rem. 3  : {Traversals.in_order(bst3.raiz)}  ← caso 1: folha")

    bst3.remover(15)    # Caso 2: um filho (tem 20)
    print(f"  Rem. 15 : {Traversals.in_order(bst3.raiz)}  ← caso 2: um filho")

    bst3.remover(5)     # Caso 3: dois filhos (3 foi removido, mas 7 ainda existe)
    print(f"  Rem. 5  : {Traversals.in_order(bst3.raiz)}     ← caso 3: dois filhos")

    # ── Demo 4: AVL ───────────────────────────────────────────────────────────
    print("\n" + "═" * 50)
    print("  DEMO 4 — Árvore AVL vs BST (inserção em ordem)")
    print("═" * 50)

    valores_ord = [1, 2, 3, 4, 5, 6, 7]
    print(f"\n  Inserindo {valores_ord} (ordem crescente) em BST comum:")
    bst_degen = construir_bst_de_lista(valores_ord)
    print(f"  Altura BST : {bst_degen.altura()} (degenerada, como lista ligada!)")
    print(f"  Balanceada : {bst_degen.esta_balanceada()}")

    avl = ArvoreAVL()
    for v in valores_ord:
        avl.inserir(v)
    bst_check = ArvoreBinariaBusca()
    bst_check.raiz = avl.raiz
    print(f"\n  Inserindo {valores_ord} (mesma ordem) em AVL:")
    print(f"  Altura AVL : {bst_check.altura()} (balanceada automaticamente!)")
    print(f"  Balanceada : {bst_check.esta_balanceada()}")

    Visualizador.imprimir(avl.raiz, "AVL — Após inserção 1-7 em ordem crescente")

    # ── Demo 5: Expressão aritmética ──────────────────────────────────────────
    print("\n" + "═" * 50)
    print("  DEMO 5 — Árvore de Expressão: (3 + 5) * (2 - 1)")
    print("═" * 50)

    expr = ArvoreExpressao()
    expr.raiz = NoExpressao('*')
    expr.raiz.esquerdo = NoExpressao('+')
    expr.raiz.esquerdo.esquerdo = NoExpressao(3)
    expr.raiz.esquerdo.direito = NoExpressao(5)
    expr.raiz.direito = NoExpressao('-')
    expr.raiz.direito.esquerdo = NoExpressao(2)
    expr.raiz.direito.direito = NoExpressao(1)

    print(f"\n  Expressão  : {expr.para_string_inorder()}")
    print(f"  Resultado  : {expr.avaliar()}")
    Visualizador.imprimir(expr.raiz, "Árvore de Expressão")

    # ── Demo 6: LCA ──────────────────────────────────────────────────────────
    print("\n" + "═" * 50)
    print("  DEMO 6 — LCA (Ancestral Comum Mais Próximo)")
    print("═" * 50)

    bst_lca = construir_bst_de_lista([10, 5, 15, 3, 7, 20])
    pares = [(3, 7), (3, 20), (5, 20), (7, 15)]
    print()
    for p, q in pares:
        resultado = lca(bst_lca.raiz, p, q)
        print(f"  LCA({p:2d}, {q:2d}) = {resultado}")


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  PONTO DE ENTRADA — main()
# ╚══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """
    Função principal: executa demonstração completa e testes automatizados.

    Em Python, o bloco 'if __name__ == "__main__"' garante que
    este código só seja executado quando o arquivo for chamado diretamente,
    não quando for importado por outro módulo.
    """
    print("""
╔══════════════════════════════════════════════════════╗
║     ÁRVORES BINÁRIAS E MUITO MAIS — Python           ║
║     Guia Completo com Exemplos e Explicações         ║
╚══════════════════════════════════════════════════════╝
    """)

    # Executa toda a demonstração didática
    demonstracao_completa()

    # Executa os testes automatizados para validar correctude
    testes = TestesAutomatizados()
    testes.executar_todos()

    print("\n✅ Programa concluído com sucesso!\n")


# ── Ponto de entrada do script ────────────────────────────────────────────────
if __name__ == "__main__":
    main()
