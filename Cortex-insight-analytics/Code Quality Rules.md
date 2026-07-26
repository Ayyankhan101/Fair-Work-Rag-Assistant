# Code Quality Rules

## Principles
- **Minimal code** — no unnecessary complexity
- **Smaller version preferred** — if 10 lines work, don't write 50
- **No boilerplate** — skip obvious comments, obvious functions
- **DRY** — never repeat logic
- **Readability > cleverness** — simple beats fancy

## Examples

### Bad (verbose)
```python
def get_total(items):
    """Calculate the total of all items."""
    total = 0
    for item in items:
        total = total + item.price
    return total
```

### Good (concise)
```python
def get_total(items):
    return sum(i.price for i in items)
```

### Bad (unnecessary class)
```python
class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def process(self):
        return [x * 2 for x in self.data]
```

### Good (simple function)
```python
def process(data):
    return [x * 2 for x in data]
```

## When to Use Classes
- Only when you need state across methods
- Only when you need multiple instances
- Otherwise, use functions

## Related
- [[Architecture Decision]] — System design
- [[Key Files]] — File reference
