import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from jev_client import ask

q = {"idiom": {"type": "noul", "instructions": "Is the phrase 'give up' in this sentence a phrasal verb whose meaning cannot be got word by word?"}}
for scheme in ("Bearer", None):
    status, body, dt = ask("She decided to give up smoking last year.", q, scheme)
    print(scheme, status, round(dt, 2), str(body)[:400])
    if status == 200:
        break
