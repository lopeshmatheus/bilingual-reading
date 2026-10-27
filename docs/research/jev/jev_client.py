import json, os, ssl, time, urllib.request, urllib.error

URL = "https://api.typesafe.ai/v1/systemone"
# The cloud sandbox re-signs TLS with its own CA; elsewhere the system store is used.
_SANDBOX_CA = "/root/.ccr/ca-bundle.crt"
CTX = ssl.create_default_context(cafile=_SANDBOX_CA if os.path.exists(_SANDBOX_CA) else None)


def ask(state, questions, auth_scheme="Bearer"):
    key = os.environ["TYPESAFE_API_KEY"]
    body = json.dumps({"model": "jev-latest", "state": state, "questions": questions}).encode()
    headers = {"Content-Type": "application/json"}
    headers["Authorization"] = f"{auth_scheme} {key}" if auth_scheme else key
    req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
            return r.status, json.loads(r.read()), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500], time.time() - t0
