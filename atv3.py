from collections import deque
from typing import Dict, List, Optional, Tuple


class EdmondsBlossom:
    """Implementacao exata do algoritmo de emparelhamento maximo de Jack Edmonds (1965),

    utilizando busca em arvore alternante, deteccao de Menor Ancestral Comum (LCA)
    e contracao/desdobramento de ciclos impares (blossoms).
    """

    def __init__(self, n: int, edges: List[Tuple[int, int]]):
        self.n = n
        self.adj: List[List[int]] = [[] for _ in range(n)]
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

        # match[i] armazena o vertice emparelhado com i (-1 se exposto)
        self.match: List[int] = [-1] * n

    def _find_augmenting_path(self, root: int) -> bool:
        parent = [-1] * self.n
        base = list(range(self.n))  # Identificador do pseudovertice de cada no
        tree_label = [
            0
        ] * self.n  # 0: nao visitado, 1: externo (outer), 2: interno (inner)

        q = deque([root])
        tree_label[root] = 1

        def get_lca(u: int, v: int) -> int:
            """Determina a base do blossom encontrando o menor ancestral comum."""
            visited = [False] * self.n
            curr = u
            while True:
                curr = base[curr]
                visited[curr] = True
                if curr == root:
                    break
                curr = parent[self.match[curr]]

            curr = v
            while True:
                curr = base[curr]
                if visited[curr]:
                    return curr
                curr = parent[self.match[curr]]

        def contract(u: int, v: int, b: int):
            """Contrai o blossom com base b e reconfigura os ponteiros da arvore."""
            blossom = [False] * self.n

            def mark_branch(curr: int, child: int):
                while base[curr] != b:
                    blossom[base[curr]] = True
                    blossom[base[self.match[curr]]] = True
                    parent[curr] = child
                    child = self.match[curr]
                    curr = parent[self.match[curr]]

            mark_branch(u, v)
            mark_branch(v, u)

            # Atualiza os nos pertencentes ao blossom
            for i in range(self.n):
                if blossom[base[i]]:
                    base[i] = b
                    if tree_label[i] == 2:
                        tree_label[i] = 1
                        q.append(i)

        while q:
            u = q.popleft()

            for v in self.adj[u]:
                # Ignora arestas internas ao mesmo blossom ou arestas do emparelhamento
                if base[u] == base[v] or self.match[u] == v:
                    continue

                # CASO 3 (Secao 4.7): Dois vertices externos -> Blossom detectado!
                if tree_label[base[v]] == 1:
                    b = get_lca(u, v)
                    contract(u, v, b)

                # CASO 4 e 5: Vertice ainda nao visitado na arvore alternante
                elif tree_label[v] == 0:
                    # CASO 4 (Secao 4.7): Vertice exposto -> Caminho aumentante encontrado!
                    if self.match[v] == -1:
                        parent[v] = u
                        # Aplica o aumento M = M + A invertendo as arestas do caminho
                        curr = v
                        while curr != -1:
                            pv = parent[curr]
                            next_curr = self.match[pv]
                            self.match[curr] = pv
                            self.match[pv] = curr
                            curr = next_curr
                        return True

                    # CASO 5 (Secao 4.7): Vertice ja emparelhado -> Estende a arvore
                    else:
                        parent[v] = u
                        tree_label[v] = 2
                        mv = self.match[v]
                        tree_label[mv] = 1
                        q.append(mv)

        return False

    def solve(self) -> List[Tuple[int, int]]:
        """Busca caminhos aumentantes iterativamente a partir dos vertices expostos."""
        while True:
            augmented = False
            for v in range(self.n):
                if self.match[v] == -1:
                    if self._find_augmenting_path(v):
                        augmented = True
                        break
            if not augmented:
                break

        pairs = []
        for u in range(self.n):
            if self.match[u] > u:
                pairs.append((u, self.match[u]))
        return pairs


# --- SIMULACAO DO PROGRAMA DE TRANSPLANTE CRUZADO ---
if __name__ == "__main__":
    familias = {
        0: "Par 0 (Família Silva)",
        1: "Par 1 (Família Santos)",
        2: "Par 2 (Família Oliveira)",
        3: "Par 3 (Família Souza)",
        4: "Par 4 (Família Lima)",
        5: "Par 5 (Família Pereira)",
    }

    # Grafo com o ciclo impar de compatibilidade C_5 e a extensao para o Par 5
    arestas_compatibilidade = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 0),  # Ciclo impar (blossom potencial)
        (4, 5),  # Conexao externa para o Par 5
    ]

    print("=== REDE HOSPITALAR DE COMPATIBILIDADE CRUZADA ===")
    for u, v in arestas_compatibilidade:
        print(f"  {familias[u]} <---> {familias[v]}")

    alocador = EdmondsBlossom(n=6, edges=arestas_compatibilidade)

    # Forcando um emparelhamento inicial subotimo para demonstrar a atuacao do blossom:
    # Emparelha (1, 2) e (3, 4), deixando os pares 0 e 5 expostos.
    alocador.match[1] = 2
    alocador.match[2] = 1
    alocador.match[3] = 4
    alocador.match[4] = 3

    print("\n--- ESTADO INICIAL SUBÓTIMO (Alocação Prévia Local) ---")
    print(f"  {familias[1]} <=====> {familias[2]}")
    print(f"  {familias[3]} <=====> {familias[4]}")
    print(f"  Pares aguardando transplante: {familias[0]} e {familias[5]}")

    # Executa o algoritmo de Edmonds
    resultado_final = alocador.solve()

    print(
        "\n--- RESULTADO FINAL OTIMIZADO (Via Algoritmo de Blossom de Edmonds) ---"
    )
    for u, v in resultado_final:
        print(f"  Cirurgia Pareada: {familias[u]}  <=====>  {familias[v]}")

    total_pacientes = len(resultado_final) * 2
    print(
        f"\nTotal de trocas viabilizadas: {len(resultado_final)} pares simultâneos."
    )
    print(
        f"Total de pacientes receptores beneficiados: {total_pacientes} de 6 (100% de sucesso)."
    )