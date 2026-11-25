# Manual Retrieval Checks

Each query retrieves up to 20 passages. Expected evidence must be
checked against the original PDF before judging the search results.

| # | Query | Expected document/page and evidence | First relevant rank | Notes |
|---|---|---|---|---|
| 1 | What is the prerequisite for CSCI 161? | Undergraduate Catalog 2026–2027, PDF p. 199: CSCI 160 with a C or higher. | 12 | Chunk 467. Found in top 20, missed top 5. Higher results often describe courses requiring CSCI 161 instead. |
| 2 | What is the prerequisite for CSCI 242? | Undergraduate Catalog 2026–2027, PDF p. 199: CSCI 161 with a C or higher. | 3 | Chunk 468. Found in top 5 and top 20; higher results lack the direct answer. |
| 3 | What is the prerequisite for CSCI 243? | Undergraduate Catalog 2026–2027, PDF p. 199: CSCI 242 with a C or higher. | 2 | Chunk 468. Found in top 5 and top 20; rank 1 lacks the direct answer. |
| 4 | How do I drop a class? | Undergraduate Catalog 2026–2027, PDF p. 22: drop via Campus Connection, subject to deadlines; the last course follows university withdrawal procedures. | 3 | Chunk 73. Found in top 5 and top 20. Higher results discuss waitlists or attendance rather than the full instructions. |
| 5 | If I stop attending a class, is it automatically dropped? | Student Handbook 2026–2027, PDF pp. 27–28: nonattendance does not guarantee cancellation; students must properly process a drop. | 1 | Chunk 881 contains the warning but labels cross-page text as p. 27 only. Content found; citation attribution needs repair. |
| 6 | How many credits do I need to be eligible for Federal Direct Loans? | Financial Aid Guide 2026–2027, PDF p. 2: at least six credits. | 18 | Chunk 985. Found in top 20, missed top 5. Rank 1 says half-time without specifying the credit minimum. |
| 7 | If I take fewer than 12 credits, what should I do about my financial aid? | Financial Aid Guide 2026–2027, PDF p. 2: notify the Financial Aid Office so aid can be adjusted appropriately. | 20 | Chunk 985. Found in top 20, missed top 5. Rank 1 discusses adjustments but lacks the specific instruction. |
| 8 | What academic performance standards must I meet to remain eligible for financial aid? | Financial Aid Guide 2026–2027, PDF p. 7: at least 2.0 cumulative GPA and completion of two-thirds of attempted credits. | 1 | Chunk 993 contains both expected facts. Catalog p. 265 at rank 2 adds a maximum timeframe; complete policy coverage was not established. |
| 9 | Can I accept financial aid before completing FAFSA verification? | Financial Aid Guide 2026–2027, PDF p. 3: selected verification must be completed before accepting aid. | 2 | Chunk 987 explicitly matches the expected evidence. Rank 1 also supports the answer indirectly by saying aid is not offered until verification is complete. |
| 10 | CSCI 160 | Undergraduate Catalog 2026–2027, PDF p. 199: course-description heading identifies Computer Science I, 4 hours. | 5 | Chunk 467. Expected course-description entry found in top 5 and top 20. Earlier results include references and program listings. |

## Results summary

On this small, manually selected set:
- Expected evidence appeared in the top 20 for 10/10 queries.
- Expected evidence appeared in the top 5 for 7/10 queries.
- Queries 1, 6, and 7 required ranks 12, 18, and 20 respectively.

These counts use the expected passages recorded in the table.
Other passages may also provide useful or indirect support.
This is not a representative benchmark or a measurement of answer accuracy.

Issues identified:
- Results can confuse a course's prerequisites with courses requiring it.
- Related financial aid passages can outrank the specific requested fact.
- Query 5 retrieved useful cross-page text labeled only as page 27,
  although the verified source spans PDF pages 27–28.
- Query 8's expected facts do not cover every academic-progress requirement.

Next priorities: investigate page attribution, improve ranking, and
evaluate on a broader set. Reranking cannot recover evidence absent
from its candidate set.