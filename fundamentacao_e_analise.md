# Fundamentação e análise complementar

## Relação entre teoria e prática
O projeto aplica conteúdos das quatro unidades didáticas fornecidas: evolução e aplicações da IA; representação de problemas por grafos e busca heurística; aprendizagem de máquina e agrupamento; e visualização, análise de texto/imagens e qualidade de dados. O recorte prático é roteamento urbano, portanto as áreas mais diretamente utilizadas são planejamento/busca e aprendizado não supervisionado.

## Decisões de projeto
- **Peso da aresta:** tempo estimado em minutos, porque a meta operacional é reduzir atrasos. A distância também é mantida para análise.
- **A* como método principal:** considera o custo acumulado e uma estimativa até o destino.
- **BFS/DFS como comparação:** ajudam a explicar por que a busca em grafo ponderado requer considerar pesos.
- **K-Means:** usa apenas coordenadas fictícias para propor três zonas.
- **Vizinho mais próximo:** cria uma ordem inicial de paradas, sem afirmar que é a melhor rota possível globalmente.

## Validade dos resultados
Os dados são sintéticos. Os valores gerados pelo script demonstram a execução dos algoritmos, mas não constituem evidência de redução real de tempo ou custo. Para uma avaliação válida, deve-se comparar o método atual e o protótipo usando pedidos, horários, distâncias e condições de tráfego equivalentes.

## Como interpretar os CSVs
- `search_comparison.csv`: caminhos encontrados por A*, BFS e DFS no exemplo depósito–Hospital.
- `cluster_assignments.csv`: zona atribuída a cada entrega pelo K-Means.
- `routes_summary.csv`: sequência heurística de visitas e métricas estimadas por zona.

## Métricas recomendadas para uma futura operação real
1. quilómetros percorridos por entrega;
2. tempo médio e percentil 90 de entrega;
3. percentagem de pedidos dentro do prazo;
4. custo de combustível por pedido;
5. taxa de entregas falhadas;
6. satisfação do cliente;
7. equilíbrio da carga de trabalho entre entregadores.

## Roteiro de teste-piloto
1. Registrar uma amostra de rotas planejadas manualmente por pelo menos alguns turnos.
2. Registrar o mesmo tipo de informação com a rota sugerida, mantendo comparáveis os períodos e volumes.
3. Separar dias por demanda e condições de trânsito.
4. Comparar médias e dispersão das métricas; não atribuir causalidade a diferenças pequenas sem amostra suficiente.
5. Revisar com entregadores as restrições não representadas no mapa e ajustar o modelo.
