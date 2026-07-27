# An Overview of Cohere&#x27;s Rerank Model | Cohere

> Source: https://docs.cohere.com/docs/reranking
> Cached: 2026-07-27T17:19:32.579Z

---

[Embeddings (Vectors, Search, Retrieval)](/docs/embeddings)[Reranking](/docs/rerank-overview)# An Overview of Cohere&#x27;s Rerank Model

Copy page## How Rerank Works

The [Rerank API endpoint](/reference/rerank-1), powered by the [Rerank models](/v2/docs/rerank), is a simple and very powerful tool for semantic search. Given a `query` and a list of `documents`, Rerank indexes the documents from most to least semantically relevant to the query.

## Get Started

### Example with Texts

In the example below, we use the [Rerank API endpoint](/reference/rerank-1) to index the list of `documents` from most to least relevant to the query `"What is the capital of the United States?"`.

**Request**

In this example, the documents are being passed in as a list of strings:

PYTHONcURL1import cohere23co = cohere.ClientV2()45query = "What is the capital of the United States?"6docs = [7    "Carson City is the capital city of the American state of Nevada. At the 2010 United States Census, Carson City had a population of 55,274.",8    "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean that are a political division controlled by the United States. Its capital is Saipan.",9    "Charlotte Amalie is the capital and largest city of the United States Virgin Islands. It has about 20,000 people. The city is on the island of Saint Thomas.",10    "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district. The President of the USA and many major national government offices are in the territory. This makes it the political center of the United States of America.",11    "Capital punishment has existed in the United States since before the United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states. The federal government (including the United States military) also uses capital punishment.",12]1314results = co.rerank(15    model="rerank-v4.0-pro", query=query, documents=docs, top_n=516)
We’ll get back a `V2RerankResponse` object that will look like this:

1V2RerankResponse(2    id="2104ccd0-74b5-4951-9bb1-cc543b26720f",3    results=[4        V2RerankResponseResultsItem(5            index=3, relevance_score=0.9432646        ),7        V2RerankResponseResultsItem(8            index=2, relevance_score=0.622092079        ),10        V2RerankResponseResultsItem(11            index=1, relevance_score=0.605425812        ),13        V2RerankResponseResultsItem(14            index=0, relevance_score=0.5904013515        ),16        V2RerankResponseResultsItem(17            index=4, relevance_score=0.466456718        ),19    ],20    meta=ApiMeta(21        api_version=ApiMetaApiVersion(22            version="2", is_deprecated=None, is_experimental=None23        ),24        billed_units=ApiMetaBilledUnits(25            images=None,26            input_tokens=None,27            output_tokens=None,28            search_units=1.0,29            classifications=None,30        ),31        tokens=None,32        cached_tokens=None,33        warnings=None,34    ),35)
Note that the `index` works as it does in Python, with `index=0` being the first document. Also, the `V2RerankResponse` object will be more compact, the example above was reformatted to make reading easier.

### Example with Structured Data:

If your documents contain structured data, for best performance we recommend formatting them as YAML strings.

**Request**

PYTHONcURL1import yaml2import cohere34co = cohere.ClientV2()56query = "What is the capital of the United States?"7docs = [8    {9        "Title": "Facts about Carson City",10        "Content": "Carson City is the capital city of the American state of Nevada. At the 2010 United States Census, Carson City had a population of 55,274.",11    },12    {13        "Title": "The Commonwealth of Northern Mariana Islands",14        "Content": "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean that are a political division controlled by the United States. Its capital is Saipan.",15    },16    {17        "Title": "The Capital of United States Virgin Islands",18        "Content": "Charlotte Amalie is the capital and largest city of the United States Virgin Islands. It has about 20,000 people. The city is on the island of Saint Thomas.",19    },20    {21        "Title": "Washington D.C.",22        "Content": "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district. The President of the USA and many major national government offices are in the territory. This makes it the political center of the United States of America.",23    },24    {25        "Title": "Capital Punishment in the US",26        "Content": "Capital punishment has existed in the United States since before the United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states. The federal government (including the United States military) also uses capital punishment.",27    },28]2930yaml_docs = [yaml.dump(doc, sort_keys=False) for doc in docs]3132results = co.rerank(33    model="rerank-v4.0-pro",34    query=query,35    documents=yaml_docs,36    top_n=5,37)
In the `documents` parameter, we are passing in a list YAML strings, representing the structured data.

As before, we get back a `V2RerankResponse` object that will look like this:

1V2RerankResponse(2    id="df4d8720-8265-4868-a8f5-0bcee7a35bd0",3    results=[4        V2RerankResponseResultsItem(5            index=3, relevance_score=0.94978136        ),7        V2RerankResponseResultsItem(8            index=2, relevance_score=0.690642549        ),10        V2RerankResponseResultsItem(11            index=0, relevance_score=0.5790195512        ),13        V2RerankResponseResultsItem(14            index=1, relevance_score=0.548286515        ),16        V2RerankResponseResultsItem(17            index=4, relevance_score=0.4937502718        ),19    ],20    meta=ApiMeta(21        api_version=ApiMetaApiVersion(22            version="2", is_deprecated=None, is_experimental=None23        ),24        billed_units=ApiMetaBilledUnits(25            images=None,26            input_tokens=None,27            output_tokens=None,28            search_units=1.0,29            classifications=None,30        ),31        tokens=None,32        cached_tokens=None,33        warnings=None,34    ),35)
## Multilingual Reranking

Cohere’s Rerank models have been trained for performance across 100+ languages.

When choosing the model, please note the following language support:

- **Rerank 4.0** (both ‘fast’ and ‘pro’): A single multilingual model (`rerank-v4.0-pro` and `rerank-v4.0-fast`)

- **Rerank 3.5**: A single multilingual model (`rerank-v3.5`)

- **Rerank 3.0**: Separate English-only and multilingual models (`rerank-english-v3.0` and `rerank-multilingual-v3.0`)

The following table provides the list of languages supported by the Rerank models. Please note that performance may vary across languages.

ISO CodeLanguage NameafAfrikaansamAmharicarArabicasAssameseazAzerbaijanibeBelarusianbgBulgarianbnBengaliboTibetanbsBosniancaCatalancebCebuanocoCorsicancsCzechcyWelshdaDanishdeGermanelGreekenEnglisheoEsperantoesSpanishetEstonianeuBasquefaPersianfiFinnishfrFrenchfyFrisiangaIrishgdScots_gaelicglGalicianguGujaratihaHausahawHawaiianheHebrewhiHindihmnHmonghrCroatianhtHaitian_creolehuHungarianhyArmenianidIndonesianigIgboisIcelandicitItalianjaJapanesejvJavanesekaGeorgiankkKazakhkmKhmerknKannadakoKoreankuKurdishkyKyrgyzLaLatinLbLuxembourgishLoLaothianLtLithuanianLvLatvianmgMalagasymiMaorimkMacedonianmlMalayalammnMongolianmrMarathimsMalaymtMaltesemyBurmeseneNepalinlDutchnoNorwegiannyNyanjaorOriyapaPunjabiplPolishptPortugueseroRomanianruRussianrwKinyarwandasiSinhaleseskSlovakslSloveniansmSamoansnShonasoSomalisqAlbaniansrSerbianstSesothosuSundanesesvSwedishswSwahilitaTamilteTelugutgTajikthThaitkTurkmentlTagalogtrTurkishttTatarugUighurukUkrainianurUrduuzUzbekviVietnamesewoWolofxhXhosayiYiddishyoYorubazhChinesezuZulu