# Local Reranking Checks

Model: BAAI/bge-reranker-v2-m3, running locally on CPU.
Hardware: Apple M1 MacBook Air, 8 GB memory.
Input limit: 1,024 BGE tokens per question–passage pair.
Selection: rerank the same 20 hybrid candidates and return five.

## Results

| Query | Expected evidence | Before rank | After rank | Rerank time |
|---|---|---|---|---|
| What is the prerequisite for CSCI 161? | Catalog p. 199: CSCI 160 with a C or higher. | 12 | 3 | 22.06 s |
| How many credits do I need to be eligible for Federal Direct Loans? | Financial Aid Guide p. 2: at least six credits. | 18 | 1 | 17.35 s |

None of the returned five inputs was truncated in either check.
Truncation status across all 20 candidates was not recorded.

## Other checks

- Empty candidates returned an empty list without loading the model.
- A prerequisite passage outranked an unrelated parking passage.
- Initial download, loading, and scoring took 281 seconds.
- Repeating the two-short-passage example with the loaded model took 6.6 seconds.

## Limitations

These two selected queries do not establish a general improvement.
Timings are individual measurements, not a latency benchmark.
The CSCI 161 answer passage still did not rank first.
Scores are relevance indicators, not calibrated correctness probabilities.
Truncation can omit useful evidence.
The reranker cannot recover passages absent from its candidate list.
Local CPU latency and deployment resource requirements need further evaluation.

Reranking is not yet connected to the API endpoint or answer generation.