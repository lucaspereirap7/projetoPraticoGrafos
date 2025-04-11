class Vertice:
    def __init__(self, id, requerido=False, demanda=0, custo_servico=0):
        self.id = id
        self.requerido = requerido
        self.demanda = demanda
        self.custo_servico = custo_servico
        self.arestas = []
        self.arcos = []

class Aresta:
    def __init__(self, origem, destino, custo_transito, demanda=0, custo_servico=0, requerida=False):
        self.origem = origem
        self.destino = destino
        self.custo_transito = custo_transito
        self.demanda = demanda
        self.custo_servico = custo_servico
        self.requerida = requerida

class Arco:
    def __init__(self, origem, destino, custo_transito, demanda=0, custo_servico=0, requerido=False):
        self.origem = origem
        self.destino = destino
        self.custo_transito = custo_transito
        self.demanda = demanda
        self.custo_servico = custo_servico
        self.requerido = requerido

class Grafo:
    def __init__(self):
        self.vertices = {}
        self.arestas = []
        self.arcos = []
        self.deposito = None

    def adicionar_vertice(self, id, requerido=False, demanda=0, custo_servico=0):
        if id not in self.vertices:
            self.vertices[id] = Vertice(id, requerido, demanda, custo_servico)
        else:
            v = self.vertices[id]
            v.requerido |= requerido
            v.demanda = max(v.demanda, demanda)
            v.custo_servico = max(v.custo_servico, custo_servico)

    def adicionar_aresta(self, origem, destino, custo_transito, demanda=0, custo_servico=0, requerida=False):
        aresta = Aresta(origem, destino, custo_transito, demanda, custo_servico, requerida)
        self.arestas.append(aresta)
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        self.vertices[origem].arestas.append(aresta)
        self.vertices[destino].arestas.append(aresta)

    def adicionar_arco(self, origem, destino, custo_transito, demanda=0, custo_servico=0, requerido=False):
        arco = Arco(origem, destino, custo_transito, demanda, custo_servico, requerido)
        self.arcos.append(arco)
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        self.vertices[origem].arcos.append(arco)

def ler_arquivo_dat(caminho):
    grafo = Grafo()
    vertices_validos = set()

    with open(caminho, 'r') as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip() != '']

    for linha in linhas:
        if linha.startswith("#Nodes:"):
            num_nodes = int(linha.split(':')[1].strip())
            for i in range(1, num_nodes + 1):
                vertices_validos.add(i)
                grafo.adicionar_vertice(i)
            break

    i = 0
    while i < len(linhas):
        linha = linhas[i]

        if linha.startswith("Depot Node"):
            grafo.deposito = int(linha.split(':')[1].strip())

        elif linha.startswith("ReN."):
            i += 1
            while i < len(linhas) and not linhas[i].startswith("ReE."):
                partes = linhas[i].split()
                node = int(partes[0][1:])
                demanda = int(partes[1])
                s_cost = int(partes[2])
                grafo.adicionar_vertice(node, True, demanda, s_cost)
                i += 1
            continue

        elif linha.startswith("ReE."):
            i += 1
            while i < len(linhas) and not linhas[i].startswith("EDGE"):
                partes = linhas[i].split()
                origem = int(partes[1])
                destino = int(partes[2])
                t_cost = int(partes[3])
                demanda = int(partes[4])
                s_cost = int(partes[5])
                grafo.adicionar_aresta(origem, destino, t_cost, demanda, s_cost, True)
                i += 1
            continue

        elif linha.startswith("EDGE"):
            i += 1
            while i < len(linhas) and not linhas[i].startswith("ReA."):
                partes = linhas[i].split()
                origem = int(partes[1])
                destino = int(partes[2])
                t_cost = int(partes[3])
                grafo.adicionar_aresta(origem, destino, t_cost, 0, 0, False)
                i += 1
            continue

        elif linha.startswith("ReA."):
            i += 1
            while i < len(linhas) and not linhas[i].startswith("ARC"):
                partes = linhas[i].split()
                origem = int(partes[1])
                destino = int(partes[2])
                t_cost = int(partes[3])
                demanda = int(partes[4])
                s_cost = int(partes[5])
                grafo.adicionar_arco(origem, destino, t_cost, demanda, s_cost, True)
                i += 1
            continue

        elif linha.startswith("ARC"):
            i += 1
            while i < len(linhas) and not (linhas[i].startswith("END") or i == len(linhas) - 1):
                partes = linhas[i].split()
                origem = int(partes[1])
                destino = int(partes[2])
                t_cost = int(partes[3])
                grafo.adicionar_arco(origem, destino, t_cost, 0, 0, False)
                i += 1
            continue

        i += 1

    return grafo

if __name__ == '__main__':
    caminho_arquivo = 'dats/BHW2.dat'
    grafo = ler_arquivo_dat(caminho_arquivo)

    vertices_requeridos = [v for v in grafo.vertices.values() if v.requerido]
    arestas_requeridas = [a for a in grafo.arestas if a.requerida]
    arcos_requeridos = [a for a in grafo.arcos if a.requerido]

    n_vertices = len(grafo.vertices)
    n_arestas = len(grafo.arestas)
    n_arcos = len(grafo.arcos)
    densidade = (n_arestas + n_arcos) / (n_vertices * (n_vertices - 1)) if n_vertices > 1 else 0

    dist = {v: {u: float('inf') for u in grafo.vertices} for v in grafo.vertices}
    next_node = {v: {u: None for u in grafo.vertices} for v in grafo.vertices}
    for v in grafo.vertices:
        dist[v][v] = 0
    for arco in grafo.arcos:
        dist[arco.origem][arco.destino] = arco.custo_transito
        next_node[arco.origem][arco.destino] = arco.destino

    for k in grafo.vertices:
        for i in grafo.vertices:
            for j in grafo.vertices:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    componentes = 0
    visitados = set()
    for v in grafo.vertices:
        if v not in visitados:
            fila = [v]
            while fila:
                atual = fila.pop()
                if atual not in visitados:
                    visitados.add(atual)
                    for u in grafo.vertices:
                        if dist[atual][u] < float('inf') and u not in visitados:
                            fila.append(u)
            componentes += 1

    grau_total = {v: 0 for v in grafo.vertices}
    for arco in grafo.arcos:
        grau_total[arco.origem] += 1
        grau_total[arco.destino] += 1

    grau_min = min(grau_total.values())
    grau_max = max(grau_total.values())

    inter = {v: 0 for v in grafo.vertices}
    soma_caminhos = 0
    diametro = 0
    for i in grafo.vertices:
        for j in grafo.vertices:
            if i != j and dist[i][j] < float('inf'):
                soma_caminhos += dist[i][j]
                diametro = max(diametro, dist[i][j])
                k = i
                while next_node[k][j] is not None and next_node[k][j] != j:
                    inter[next_node[k][j]] += 1
                    k = next_node[k][j]

    total_caminhos = n_vertices * (n_vertices - 1)
    caminho_medio = soma_caminhos / total_caminhos if total_caminhos else 0

    print("Estatísticas do grafo:")
    print(f"Qtd Vértices: {n_vertices}")
    print(f"Qtd Arestas: {n_arestas}")
    print(f"Qtd Arcos: {n_arcos}")
    print(f"Qtd Vértices Requeridos: {len(vertices_requeridos)}")
    print(f"Qtd Arestas Requeridas: {len(arestas_requeridas)}")
    print(f"Qtd Arcos Requeridos: {len(arcos_requeridos)}")
    print(f"Densidade: {densidade}")
    print(f"Componentes conectados: {componentes}")
    print(f"Grau Mínimo: {grau_min}")
    print(f"Grau Máximo: {grau_max}")
    print(f"Intermediação: {inter}")
    print(f"Caminho Médio: {round(caminho_medio, 3)}")
    print(f"Diâmetro: {diametro}")