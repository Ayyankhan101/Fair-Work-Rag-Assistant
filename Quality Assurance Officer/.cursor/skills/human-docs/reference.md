# AI writing tells — reference

Condensed from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). These are **signals**, not proof. Fix the underlying vagueness, not just the words.

## Content patterns

### Significance inflation

LLM text pads topics with importance language unrelated to the facts.

Words to watch: stands/serves as, testament, reminder, crucial, pivotal, vital, significant (as filler), key role/moment, underscores, highlights its importance, reflects broader, symbolizing, enduring, lasting, contributing to, setting the stage for, marking/shaping, represents a shift, turning point, evolving landscape, focal point, indelible mark, deeply rooted.

**Fix:** State the fact. Delete the paragraph about what it "represents."

### Superficial analysis

Trailing participles and vague impact statements.

Words to watch: highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, cultivating, fostering, encompassing, enhancing, valuable insights, align with, resonate with.

Pattern: main clause + `, highlighting/ensuring/reflecting …`

**Fix:** End the sentence at the fact. Put requirements in a table.

### Promotional tone

Words to watch: boasts, vibrant, rich, profound, groundbreaking, renowned, nestled, in the heart of, diverse array, commitment to, natural beauty, showcasing, exemplifies.

**Fix:** Neutral verbs: has, contains, returns, fails if.

### Vague attribution

Words to watch: industry reports, observers note, experts argue, some critics, several sources (when few cited).

**Fix:** Name the file, commit, ticket, or person. If unknown, write "unknown" or "TBD" with owner.

### Outline conclusions

Sections titled "Challenges and future prospects" that speculate without data.

**Fix:** "Open issues" with numbered items and owners.

## Language patterns

### AI vocabulary (high signal when clustered)

Additionally (sentence start), align with, boasts, bolstered, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract), meticulous, pivotal, robust, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant.

Era note (Wikipedia): older ChatGPT overused *delve* and *tapestry*; newer models overuse *showcase*, *fostering*, *align with*.

### Negative parallelisms

- Not only X, but also Y
- It's not X, it's Y
- No X, no Y, just Z
- X rather than Y (when rhetorical, not technical contrast)

**Fix:** State X. State Y in the next sentence if both needed.

### Rule of three

Three adjectives, three parallel phrases, or three bullet groups where one item or a table works.

**Fix:** Use the count that matches reality (129 awards, not "three pillars").

### Elegant variation

Renaming the same thing every sentence to avoid repetition (e.g. "the pipeline", "the workflow", "the process", "the mechanism").

**Fix:** Repeat the proper noun or file name.

### Copula avoidance

Circumlocution instead of "is/are": " serves as", " stands as", " marks a", " represents a".

**Fix:** Use "is" or "are".

## Formatting patterns

| Tell | Fix for tech docs |
|------|-------------------|
| Title Case Headings | Sentence case |
| Bold every keyword | Bold only literals or UI |
| `**Label:** description` bullet lists | Table with Label column |
| Em dash overuse | Commas or separate sentences |
| Emoji section markers | Plain headings |
| `---` before every heading | One blank line only |
| Skipped heading levels (h1 → h3) | Sequential ## / ### |
| Curly quotes when repo uses straight | Match project style |

## Communication patterns (avoid in docs)

- "Great question"
- "I'd be happy to help"
- "Let's dive in / unpack / explore"
- "Here's how we'll tackle this"
- Offering options the reader did not ask for
- Restating the user's entire request before answering

## Technical doc additions

Patterns common in AI-generated README/plans but rare in human maintainer docs:

- "Architecture overview" followed by adjectives, not interfaces
- Tier names like "super easy" mixed with "server melters" without definitions (define once in a table)
- Mermaid diagrams with no corresponding code paths
- Success criteria with no measurement command
- Phrases: "end-to-end", "holistic", "best-in-class", "world-class", "cutting-edge", "seamlessly", "powerful", "transformative"

## Review priority

When time is short, fix in this order:

1. Remove significance/promotional paragraphs
2. Replace buzzword clusters with numbers and paths
3. Convert inline-bold lists to tables
4. Shorten sentences and headings
5. Scan for AI vocabulary list (three or more hits in one section = rewrite section)
