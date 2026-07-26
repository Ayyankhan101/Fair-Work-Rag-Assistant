# Dashboard

## All Notes
```dataview
TABLE file.mtime as "Last Modified"
FROM ""
SORT file.mtime DESC
```

## Components
```dataview
TABLE file.mtime as "Modified"
FROM "RAG Chain" OR "CAG Context Cache" OR "Query Router" OR "Filtered Retriever" OR "Vector Store"
SORT file.name
```

## Evaluation
```dataview
TABLE file.mtime as "Modified"
FROM "Evaluation Questions" OR "Evaluation Results" OR "Hard Eval Suite"
SORT file.name
```

## Progress
```dataview
TABLE file.mtime as "Modified"
FROM "Improvement Progress" OR "Next Steps"
SORT file.name DESC
```

## Recently Modified
```dataview
TABLE file.mtime as "When"
FROM ""
SORT file.mtime DESC
LIMIT 10
```

## Related
- [[Project Overview]] — Hub note
