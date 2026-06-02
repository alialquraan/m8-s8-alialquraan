# Routing Report — Module 8 Tuesday Stretch

> 300–500 words. Replace the placeholder text in each section with your analysis.

## 1. Per-Query-Type Classifier Accuracy

The query classifier in this system is implemented using a rule-based heuristic approach. The goal is to categorize incoming queries into three types: factoid, semantic, and mixed. The classification logic relies on simple but effective signals. Queries containing digits or quoted phrases are treated as factoid, since they typically refer to specific entities, dates, or exact expressions. Queries with strong named-entity patterns or short length are also more likely to be classified as factoid. Semantic queries are identified using keyword indicators such as “explain,” “compare,” “describe,” “why,” and “how,” as well as longer query length which often correlates with conceptual questions. All remaining queries are classified as mixed.

To evaluate classifier quality, a small held-out subset of queries from the evaluation set was manually inspected. The classifier performed well on clear factoid and semantic cases, but showed occasional confusion on borderline queries where both keyword signals and entity-like structure were present. Overall, the classifier is lightweight but sufficiently accurate for routing purposes in this system.

## 2. Routed Retriever Metrics

The performance of the routed retriever is compared against three baselines: BM25, dense retrieval, and hybrid retrieval (α = 0.5). The metrics include Recall@5, Recall@10, and Mean Reciprocal Rank (MRR).

Comparison table:

| Retriever | recall@5 | recall@10 | MRR |
|---|---|---|---|
| BM25 (baseline) | 0.567 | 0.650 | 0.549 |
| Dense (baseline) | 0.900 | 0.933 |0.670 |
| Hybrid α=0.5 (baseline) | 0.850 | 0.983 | 0.707 |
| Routed | 0.800 | 0.867 | 0.672 |

The results show that dense retrieval significantly outperforms BM25, confirming that semantic embedding-based retrieval is more effective for most queries in this dataset. The hybrid model achieves the best overall performance, especially in Recall@10 and MRR, because it combines lexical matching with semantic similarity.

The routed retriever performs better than BM25 but does not surpass the hybrid baseline. This is expected, since routing introduces an additional classification step that can introduce errors. However, its performance remains competitive with dense retrieval, indicating that the routing logic is generally effective.

## 3. When Does Routing Win, When Does It Lose, Why

The routing system performs best when the classifier correctly identifies clear factoid or semantic queries. For example, factoid-style queries involving specific entities or numeric information benefit from BM25 due to exact token matching. Similarly, semantic queries such as “explain the difference between X and Y” are better handled by dense retrieval.

However, routing underperforms in ambiguous or mixed queries where classification is uncertain. In such cases, the model may incorrectly route a query that would have benefited from hybrid retrieval into either BM25 or dense retrieval alone. This leads to a drop in recall compared to the hybrid baseline, which does not rely on classification and instead combines both signals.

Specific failure cases typically occur when a query contains both semantic intent and entity-like structure. In these cases, the classifier may prioritize heuristics such as length or keywords incorrectly, leading to suboptimal routing decisions.

Overall, routing demonstrates the trade-off between interpretability and robustness. While it introduces modular decision-making and can outperform single retrievers in some cases, it is still limited by classification errors. Future improvements could include embedding-based classification or probabilistic routing to reduce misclassification and better approximate hybrid performance.
