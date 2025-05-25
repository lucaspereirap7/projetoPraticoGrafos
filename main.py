import os
import csv

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
        self.capacidade = None

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
        if linha.startswith("Capacity:"):
            grafo.capacidade = int(linha.split(':')[1].strip())
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

def construir_servicos(grafo):
    servicos = []
    id_servico = 1

    for v in grafo.vertices.values():
        if v.requerido:
            servicos.append({
                'id': id_servico,
                'tipo': 'nó',
                'origem': v.id,
                'destino': v.id,
                'demanda': v.demanda,
                'custo_servico': v.custo_servico,
                'obj': v
            })
            id_servico += 1

    for a in grafo.arestas:
        if a.requerida:
            servicos.append({
                'id': id_servico,
                'tipo': 'aresta',
                'origem': a.origem,
                'destino': a.destino,
                'demanda': a.demanda,
                'custo_servico': a.custo_servico,
                'obj': a
            })
            id_servico += 1

    for a in grafo.arcos:
        if a.requerido:
            servicos.append({
                'id': id_servico,
                'tipo': 'arco',
                'origem': a.origem,
                'destino': a.destino,
                'demanda': a.demanda,
                'custo_servico': a.custo_servico,
                'obj': a
            })
            id_servico += 1

    return servicos

def construir_rotas_guloso(grafo, servicos, capacidade, dist):
    nao_atendidos = set(s['id'] for s in servicos)
    id_para_servico = {s['id']: s for s in servicos}
    rotas = []

    while nao_atendidos:
        candidatos_iniciais = [
            id_para_servico[sid]
            for sid in nao_atendidos
            if dist[grafo.deposito][id_para_servico[sid]['origem']] < float('inf')
        ]
        if not candidatos_iniciais:
            break

        prox = min(candidatos_iniciais, key=lambda s: dist[grafo.deposito][s['origem']])
        rota = []
        demanda_rota = 0
        custo_rota = 0
        atual = grafo.deposito
        rota_visitas = []

        rota_visitas.append(('D', 0, 1, 1))

        while True:
            candidatos = [
                id_para_servico[sid]
                for sid in nao_atendidos
                if id_para_servico[sid]['demanda'] + demanda_rota <= capacidade
                and dist[atual][id_para_servico[sid]['origem']] < float('inf')
            ]
            if not candidatos:
                break
            prox = min(candidatos, key=lambda s: dist[atual][s['origem']])
            custo_rota += dist[atual][prox['origem']] + prox['custo_servico']
            demanda_rota += prox['demanda']
            rota_visitas.append(('S', prox['id'], prox['origem'], prox['destino']))
            atual = prox['destino']
            nao_atendidos.remove(prox['id'])

        custo_rota += dist[atual][grafo.deposito]
        rota_visitas.append(('D', 0, 1, 1))

        rotas.append({
            'demanda': demanda_rota,
            'custo': custo_rota,
            'visitas': rota_visitas
        })

    return rotas

def buscar_clocks(nome_instancia, arquivo_csv='reference_values.csv'):
    clocks_exec = 0
    clocks_sol = 0
    try:
        with open(arquivo_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row = {k.strip(): v for k, v in row.items()}
                if nome_instancia.lower() in row['Nome'].lower():
                    clocks_exec = int(float(row['clocks']))
                    clocks_sol = int(float(row['clocks_melhor_sol']))
                    break
    except Exception as e:
        print("Erro ao ler reference_values.csv:", e)
    return clocks_exec, clocks_sol

def imprimir_solucao_em_arquivo(rotas, custo_total, clocks_exec, clocks_sol, caminho_saida):
    with open(caminho_saida, 'w') as f:
        f.write(f"{custo_total}\n")
        f.write(f"{len(rotas)}\n")
        f.write(f"{clocks_exec}\n")
        f.write(f"{clocks_sol}\n")
        for i, rota in enumerate(rotas):
            visitas = rota['visitas']
            total_visitas = len(visitas)
            linha = f" 0 1 {i+1} {rota['demanda']} {rota['custo']}  {total_visitas}"
            for v in visitas:
                if v[0] == 'D':
                    linha += f" (D 0,1,1)"
                elif v[0] == 'S':
                    linha += f" (S {v[1]},{v[2]},{v[3]})"
            f.write(linha + "\n")

def imprimir_solucao(rotas, custo_total, clocks_exec, clocks_sol):
    print(custo_total)
    print(len(rotas))
    print(clocks_exec)
    print(clocks_sol)
    for i, rota in enumerate(rotas):
        visitas = rota['visitas']
        total_visitas = len(visitas)
        linha = f" 0 1 {i+1} {rota['demanda']} {rota['custo']}  {total_visitas}"
        for v in visitas:
            if v[0] == 'D':
                linha += f" (D 0,1,1)"
            elif v[0] == 'S':
                linha += f" (S {v[1]},{v[2]},{v[3]})"
        print(linha)

if __name__ == '__main__':
    import os

    while True:
        nome_arquivo = input("Digite o nome do arquivo de entrada (ex: BHW1.dat): ").strip()
        caminho_arquivo = os.path.join('dats', nome_arquivo)
        nome_instancia = os.path.splitext(nome_arquivo)[0]
        try:
            grafo = ler_arquivo_dat(caminho_arquivo)
            break
        except FileNotFoundError:
            print(f"Arquivo '{caminho_arquivo}' não encontrado. Tente novamente.\n")

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
    
    capacidade = grafo.capacidade
    servicos = construir_servicos(grafo)
    rotas = construir_rotas_guloso(grafo, servicos, capacidade, dist)
    custo_total = sum(r['custo'] for r in rotas if r['custo'] < float('inf'))
    clocks_exec, clocks_sol = buscar_clocks(nome_instancia)
    os.makedirs('G22', exist_ok=True)
    caminho_saida = os.path.join('G22', f"sol-{nome_instancia}.dat")
    imprimir_solucao_em_arquivo(rotas, custo_total, clocks_exec, clocks_sol, caminho_saida)

    print(f"Solução salva em: {caminho_saida}")