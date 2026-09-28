# Algoritmo de Blossom de Jack Edmonds (1965) - Emparelhamento Máximo

Projeto prático para a disciplina de **Tópicos de Otimização** (UFRPE).

Este repositório contém a implementação do algoritmo polinomial de emparelhamento de cardinalidade máxima proposto por Jack Edmonds no clássico artigo:

> **EDMONDS, Jack.** *Paths, trees, and flowers.* Canadian Journal of Mathematics, v. 17, p. 449-467, 1965.

---

## 📌 Contextualização: Doação Cruzada de Rins (Kidney Paired Donation)

O algoritmo foi contextualizado para resolver a alocação ótima em um programa de **Doação Cruzada de Rins** em regime de trocas bilaterais (2 a 2):

* **Vértices ($V$)**: Pares incompatíveis doador-receptor $(\text{Doador } D_v, \text{Receptor } R_v)$.
* **Arestas ($E$)**: Compatibilidade imunológica mútua cruzada entre duas famílias.
* **Desafio**: A rede de compatibilidade médica contém circuitos de comprimento ímpar (ex.: pentágono $C_5$). Métodos ingênuos de busca falham ou caem em custo combinatório exponencial; o algoritmo de Edmonds resolve o problema contraindo os *blossoms* em tempo polinomial $O(n^4)$.

---

## 🚀 Como Executar

O projeto utiliza apenas a biblioteca padrão do Python 3 (sem dependências externas):

```bash
python atv3.py