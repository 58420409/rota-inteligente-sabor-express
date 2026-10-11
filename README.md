# Rota Inteligente: Otimização de Entregas com Algoritmos de IA

**Projeto acadêmico — Artificial Intelligence Fundamentals**  
**Empresa fictícia:** Sabor Express

## 1. Resumo executivo

Este projeto demonstra uma solução introdutória para apoiar o planejamento de entregas urbanas. A cidade é representada como um grafo ponderado: cada vértice é um local e cada aresta é uma ligação viária com distância e tempo estimado. O algoritmo A* encontra caminhos entre pontos; BFS e DFS são incluídos para comparação conceitual; e K-Means agrupa os pedidos por proximidade geográfica para sugerir zonas de atendimento.

O projeto é um **protótipo didático**, não um sistema de navegação real. Os locais, coordenadas, distâncias e tempos são **dados sintéticos criados exclusivamente para demonstração**. Os resultados gerados pelo programa não representam medições reais da Sabor Express.

## 2. Problema e objetivos

A Sabor Express define rotas manualmente e enfrenta atrasos, trajetos pouco eficientes, maior consumo de combustível e insatisfação de clientes, sobretudo no almoço e no jantar.

### Objetivo geral
Construir um protótipo reproduzível que combine busca em grafos e agrupamento não supervisionado para apoiar a organização de entregas.

### Objetivos específicos
- representar pontos de entrega e ruas por meio de um grafo ponderado;
- implementar A* para encontrar um caminho de menor custo estimado;
- apresentar BFS e DFS como métodos de busca de referência;
- aplicar K-Means às coordenadas dos pedidos para formar zonas;
- criar uma sequência de visitas por zona usando uma heurística simples de vizinho mais próximo;
- medir distância e tempo estimados e discutir limites, riscos e melhorias.

## 3. Fundamentação teórica

### 3.1 Inteligência Artificial e planejamento
A Inteligência Artificial reúne técnicas para resolver problemas que exigem percepção, busca, aprendizado ou tomada de decisão. No cenário proposto, o planejamento de rotas é tratado como um problema de busca em um espaço de estados: o estado atual é o ponto onde o entregador se encontra, as ações correspondem às ruas disponíveis e o custo é a distância ou o tempo estimado.

### 3.2 Grafos
Um grafo é formado por vértices e arestas. Neste projeto:
- **vértices:** depósito e pontos de entrega;
- **arestas:** conexões viárias permitidas;
- **pesos:** tempo estimado de deslocamento em minutos;
- **coordenadas:** posições simplificadas em um plano, usadas para visualizar e calcular a heurística.

O grafo é não direcionado neste exemplo, ou seja, cada rua pode ser percorrida nos dois sentidos. Em uma aplicação real, ruas de mão única, conversões proibidas e restrições de acesso exigiriam arestas direcionadas e dados cartográficos confiáveis.

### 3.3 Busca em largura (BFS) e busca em profundidade (DFS)
A **BFS** explora os vértices por camadas e encontra um caminho com o menor número de arestas em grafos não ponderados. Não garante o menor tempo quando as arestas possuem pesos diferentes. A **DFS** explora um ramo até onde consegue e depois retorna; é útil para explorar conectividade, mas não garante o caminho de menor custo. As duas são incluídas como referências didáticas, não como a estratégia principal de roteamento.

### 3.4 A* (A-estrela)
O A* avalia um nó usando `f(n) = g(n) + h(n)`, em que `g(n)` é o custo acumulado desde a origem e `h(n)` é uma estimativa do custo restante até o destino. Com custos não negativos e uma heurística admissível, o algoritmo pode encontrar uma rota de custo mínimo. Neste protótipo, a heurística usa a distância em linha reta multiplicada por um fator conservador de tempo por quilômetro. Os dados sintéticos foram escolhidos para manter essa estimativa compatível com os custos das arestas.

### 3.5 K-Means e aprendizado não supervisionado
K-Means é um algoritmo de aprendizado não supervisionado que divide observações em `k` grupos, procurando reduzir a soma das distâncias quadráticas entre cada observação e o centro do grupo. Aqui, cada pedido é representado por coordenadas (x, y). O agrupamento sugere zonas geográficas, mas **não resolve sozinho** o problema completo de roteamento: não considera, por si só, ruas, trânsito, capacidade do entregador, horários prometidos ou prioridade do pedido.

### 3.6 Heurística de vizinho mais próximo
Depois de criar zonas, o protótipo escolhe repetidamente o ponto ainda não visitado mais próximo do ponto atual, considerando os tempos mínimos calculados pelo grafo. É uma heurística simples e rápida, mas não garante a sequência globalmente ótima para múltiplas paradas. O retorno ao depósito é incluído para facilitar a comparação.

## 4. Abordagem adotada

1. Ler `data/nodes.csv`, `data/edges.csv` e `data/deliveries.csv`.
2. Construir um grafo ponderado a partir das ruas disponíveis.
3. Calcular caminhos entre os locais com A*; calcular BFS e DFS para comparação conceitual.
4. Agrupar as entregas em três zonas usando K-Means.
5. Ordenar as paradas dentro de cada zona pela heurística de vizinho mais próximo.
6. Gerar tabelas CSV e imagens em `outputs/`.
7. Interpretar os resultados com cautela, pois a rede e os dados são fictícios.

## 5. Estrutura do repositório

```text
rota_inteligente_sabor_express/
├── README.md
├── requirements.txt
├── data/
│   ├── nodes.csv
│   ├── edges.csv
│   └── deliveries.csv
├── src/
│   └── main.py
├── docs/
│   ├── fundamentacao_e_analise.md
│   └── roteiro_video_pitch.md
└── outputs/
    ├── routes_summary.csv       # gerado na execução
    ├── cluster_assignments.csv  # gerado na execução
    ├── graph.png                # gerado na execução
    └── clusters.png             # gerado na execução
```

## 6. Como executar

### Requisitos
- Python 3.10 ou superior;
- pip;
- bibliotecas listadas em `requirements.txt`.

### Windows — passo a passo
1. Extraia o ZIP em uma pasta.
2. Abra essa pasta no VS Code.
3. Abra **Terminal > Novo Terminal**.
4. (Opcional, recomendado) crie um ambiente virtual:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   Se o comando `py` não funcionar, tente `python`.
5. Instale as bibliotecas:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Execute:
   ```powershell
   python src/main.py
   ```
7. Confira as imagens e os CSVs criados na pasta `outputs`.

Se o PowerShell bloquear a ativação do ambiente virtual, você pode executar `python -m pip install -r requirements.txt` e `python src/main.py` sem ativá-lo, usando a instalação de Python já disponível.

### GitHub
1. Entre em https://github.com e crie um repositório público chamado `rota-inteligente-sabor-express`.
2. Descompacte o projeto e abra a pasta no VS Code.
3. No repositório do GitHub, use **Add file > Upload files** e envie os arquivos e pastas do projeto (ou use Git, se já souber utilizá-lo).
4. Após executar o programa, envie também os arquivos gerados em `outputs/`, se a plataforma permitir. Não inclua a pasta `.venv`.
5. Confirme que o README aparece na página inicial do repositório.
6. Copie a URL pública do repositório para entregar à faculdade.

## 7. Diagrama do modelo

O programa gera `outputs/graph.png` a partir dos nós e das arestas presentes nos CSVs. O desenho mostra a rede sintética e os pesos de tempo. Também gera `outputs/clusters.png`, com as zonas sugeridas pelo K-Means.

Representação lógica simplificada:

```text
Depósito (D)
  ├── Centro (C)
  ├── Norte (N)
  └── Sul (S)

Cada conexão possui um tempo estimado. O A* procura o caminho de menor custo entre origem e destino.
K-Means agrupa as coordenadas dos pedidos em zonas, e a heurística ordena as paradas de cada zona.
```

## 8. Métricas de avaliação

O programa registra:
- **tempo estimado da rota:** soma dos pesos das arestas percorridas;
- **distância estimada:** soma das distâncias das arestas percorridas;
- **quantidade de paradas:** número de entregas da zona;
- **tempo médio por parada:** tempo estimado dividido pelo número de paradas, como indicador simples;
- **comparação entre métodos de busca:** BFS e DFS retornam caminhos para referência, enquanto A* otimiza o custo ponderado do tempo.

Não se apresenta uma redução percentual real sem uma linha de base real. Para calcular melhoria operacional, a empresa precisaria medir rotas manuais e rotas sugeridas em períodos comparáveis.

## 9. Resultados e análise

Ao executar o programa, os valores concretos serão gravados em `outputs/routes_summary.csv` e `outputs/cluster_assignments.csv`. Como a base é sintética, os resultados demonstram o funcionamento do algoritmo e não comprovam economia real de combustível ou melhoria real no prazo de entrega.

A expectativa metodológica é que A* selecione caminhos de menor tempo estimado no grafo fornecido, enquanto K-Means organize entregas próximas em grupos. A sequência de vizinho mais próximo reduz a complexidade de construir uma ordem inicial de visitas, mas pode produzir uma solução inferior à ótima global.

### Comparação qualitativa
| Método | Uso no projeto | Vantagem | Limitação |
|---|---|---|---|
| BFS | Busca de referência | Simples; minimiza número de arestas em grafos não ponderados | Ignora pesos de tempo |
| DFS | Busca de referência | Explora conectividade com pouca estrutura adicional | Não garante menor caminho |
| A* | Caminhos entre pontos | Usa custo acumulado e heurística para orientar a busca | Depende da qualidade da heurística e dos dados |
| K-Means | Zonas de entregas | Agrupa pontos geograficamente próximos | Exige definir `k`; não considera ruas nem restrições operacionais |
| Vizinho mais próximo | Ordem das paradas | Fácil de implementar e rápido | Não garante a rota globalmente ótima |

## 10. Relação com casos reais

A UPS desenvolveu o ORION (On-Road Integrated Optimization and Navigation), sistema de otimização de rotas baseado em dados e técnicas de pesquisa operacional. A INFORMS descreve o projeto como uma solução que organiza rotas de coleta e entrega e relata benefícios operacionais e ambientais. Em comunicação da UPS de 2015, a empresa estimava reduzir 100 milhões de milhas percorridas por ano quando a implementação estivesse completa. Esses números pertencem à operação da UPS e **não devem ser transferidos como previsão para a Sabor Express**.

A Kardinal descreve aplicações de otimização para entregas de produtos frescos, incluindo janelas de tempo, capacidade, previsão de chegada e ajustes de rota diante de mudanças. Isso evidencia que sistemas reais precisam modelar mais restrições do que distância geográfica.

## 11. Limitações e melhorias futuras

- substituir coordenadas e ruas fictícias por mapa real e dados geográficos;
- usar dados históricos e tráfego em tempo real;
- modelar ruas de mão única, conversões, obras e restrições de circulação;
- incluir capacidade dos entregadores, horários prometidos e prioridades;
- testar diferentes valores de `k` e comparar K-Means com DBSCAN;
- comparar a heurística de vizinho mais próximo com algoritmos de otimização de rotas (por exemplo, busca local ou programação matemática);
- avaliar desempenho com entregas reais e um período de teste controlado;
- preservar privacidade dos clientes, coletando apenas os dados necessários e controlando o acesso.

## 12. Ética, privacidade e responsabilidade

O protótipo utiliza dados inventados e não contém informações pessoais. Em uma implantação real, endereços e hábitos de entrega devem ser protegidos, com acesso restrito, retenção limitada e observância da legislação aplicável, incluindo a LGPD. As recomendações automáticas devem apoiar — e não substituir cegamente — a avaliação humana, principalmente quando houver imprevistos, riscos de segurança ou necessidades especiais dos clientes e entregadores.

## 13. Conclusão

O projeto mostra como conceitos fundamentais de IA podem ser combinados em um problema logístico: grafos representam a rede viária, A* busca caminhos de menor custo estimado, BFS e DFS servem como referências de busca, e K-Means propõe zonas de atendimento. A heurística de vizinho mais próximo organiza uma sequência inicial de entregas em cada zona.

A principal contribuição é um protótipo simples, executável e documentado que pode ser ampliado gradualmente. Para afirmar ganhos reais, a Sabor Express deverá substituir os dados sintéticos por dados operacionais, comparar os resultados com o planejamento manual e acompanhar distância, tempo, pontualidade, custo e satisfação dos clientes.

## 14. Preparação do vídeo pitch

O arquivo `docs/roteiro_video_pitch.md` contém um roteiro sugerido para um vídeo de até quatro minutos. Grave a tela mostrando o problema, os algoritmos, a execução do programa e os resultados gerados. O roteiro descreve os resultados demonstrativos do projeto e deixa claro que os dados são sintéticos.

## 15. Referências

HOLLAND, Chuck; LEVIS, Jack; NUGGHELLI, Ranganath S.; SANTILLI, Robert; WINTERS, Jeff. **UPS Optimizes Delivery Routes**. *Interfaces*, v. 47, n. 1, p. 8–23, 2017. Disponível em: https://pubsonline.informs.org/doi/10.1287/inte.2016.0875. Acesso em: 10 out. 2026.

INFORMS. **UPS 2016 Edelman Award: ORION Project**. Disponível em: https://www.informs.org/Recognizing-Excellence/Award-Recipients/UPS-2016-Edelman. Acesso em: 10 out. 2026.

KARDINAL. **Fresh product delivery — route optimization**. Disponível em: https://kardinal.ai/delivery-fresh-produce/. Acesso em: 10 out. 2026.

KARDINAL. **Route optimization: addressing the challenges of fresh produce transport**. Disponível em: https://kardinal.ai/route-optimization-addressing-the-challenges-of-fresh-produce-transport/. Acesso em: 10 out. 2026.

MATERIAL DIDÁTICO DA DISCIPLINA. **Artificial Intelligence Fundamentals — Unidades I, II, III e IV**. Conteúdo disponibilizado pela instituição de ensino. (Completar com instituição, ano e dados editoriais, se exigidos pela faculdade.)
