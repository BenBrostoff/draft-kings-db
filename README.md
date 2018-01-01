## Setup

```bash
pip install draft_kings_db
```

## Example

Example:

```python
from draft_kings_db import client

c = client.DraftKingsHistory()
c.initialize_nba()
for perf in c.lookup_nba_performances('Kevin Durant'):
    print('{} {}'.format(
        perf.matchup,
        perf.draft_kings_points,
    ))
```