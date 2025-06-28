# Trabalho Prático - Etapa 1, 2, 3 - Grafos e Suas Aplicações

Este projeto é a implementação da Etapa 1, 2 e 3 do trabalho prático da disciplina **Grafos e Suas Aplicações**, utilizando a linguagem **Python**. O objetivo principal é fazer o pré-processamento de arquivos `.dat` com descrições de grafos e extrair estatísticas importantes.

Grupo composto por: **Lucas de Oliveira Pereira** matrícula 202210578 e **Vinicius Passos Oliveira** matrícula 202210579.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```

trabalhoPraticoGrafos/
│
├── dats/                  # Arquivos de entrada (.dat)
│   ├── BHW1.dat
│   ├── BHW2.dat
│   └── ...
│
├── main.py                # Arquivo principal, com toda logica do projeto
├── teste.ipynb            # Notebook de teste
└── README.md              # Este arquivo
├── G22-Fase 2/                  # Resultado dos arquivos de entrada (.dat)
│   ├── sol-BHW1.dat
│   ├── sol-BHW2.dat
│   └── ...
── G22 - Fase 3/                  # Resultado dos arquivos de entrada (.dat) com o algoritmo construtivo aprimorado
│   ├── sol-BHW1.dat
│   ├── sol-BHW2.dat
│   └── ...

## Requisitos

- Python instalado (usei a versão 3.12.1, mas deve funcionar em outras recentes)

## Como Executar

1. **Clone o projeto ou baixe os arquivos**
2. Abra um terminal e vá até a pasta do projeto.
3. Execute o `python main.py`.
4. Se quiser rodar codigos no arquivo de teste, deve instalar o pandas e o jupyer. Pode ser com o comando `pip install notebook pandas`

## Exemplo de Saída

Estatísticas do grafo:
1. Qtd Vértices: 12
2. Qtd Arestas: 0
3. Qtd Arcos: 25
4. Qtd Vértices Requeridos: 4
5. Qtd Arestas Requeridas: 0

...e as outras estatisticas solicitadas
