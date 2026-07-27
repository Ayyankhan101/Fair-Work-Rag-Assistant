# Rerank API (v2) | Cohere

> Source: https://docs.cohere.com/reference/rerank
> Cached: 2026-07-27T17:20:12.860Z

---

[Endpoints](/reference/chat)[v2/rerank](/reference/rerank)# Rerank API (v2)

Copy pagePOSThttps://api.cohere.com/v2/rerankPOST/v2/rerankPython1import cohere23co = cohere.ClientV2()45docs = [6    "Carson City is the capital city of the American state of Nevada.",7    "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",8    "Capitalization or capitalisation in English grammar is the use of a capital letter at the start of a word. English usage varies from capitalization in other languages.",9    "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",10    "Capital punishment has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states.",11]1213response = co.rerank(14    model="rerank-v4.0-pro",15    query="What is the capital of the United States?",16    documents=docs,17    top_n=3,18)19print(response)Try it200Successful1{2  "results": [3    {4      "index": 3,5      "relevance_score": 0.9990716    },7    {8      "index": 4,9      "relevance_score": 0.786786710    },11    {12      "index": 0,13      "relevance_score": 0.3271306814    }15  ],16  "id": "07734bd2-2473-4f07-94e1-0d9f0e6843cf",17  "meta": {18    "api_version": {19      "version": "2",20      "is_experimental": false21    },22    "billed_units": {23      "search_units": 124    }25  }26}This endpoint takes in a query and a list of texts and produces an ordered array with each text assigned a relevance score.### Authentication

AuthorizationBearerBearer authentication of the form `Bearer <token>`, where token is your auth token.

### Headers

X-Client-NamestringOptionalThe name of the project that is making the request.
### Request

modelstringRequiredThe identifier of the model to use, eg `rerank-v3.5`.

querystringRequiredThe search querydocumentslist of stringsRequiredA list of texts that will be compared to the `query`.
For optimal performance we recommend against sending more than 1,000 documents in a single request.

**Note**: long documents will automatically be truncated to the value of `max_tokens_per_doc`.

**Note**: structured data should be formatted as YAML strings for best performance.top_nintegerOptional`>=1`Limits the number of returned rerank results to the specified value. If not passed, all the rerank results will be returned.max_tokens_per_docintegerOptionalDefaults to `4096`. Long documents will be automatically truncated to the specified number of tokens.

priorityintegerOptional`0-999`Defaults to `0`Controls how early the request is handled. Lower numbers indicate higher priority (default: 0, the highest). When the system is under load, higher-priority requests are processed first and are the least likely to be dropped.

### Response

OKresultslist of objectsAn ordered list of ranked documentsidstringmetaobject### Errors

400Bad Request Error401Unauthorized Error403Forbidden Error404Not Found Error422Unprocessable Entity Error429Too Many Requests Error498Invalid Token Error499Client Closed Request Error500Internal Server Error501Not Implemented Error503Service Unavailable Error504Gateway Timeout Error