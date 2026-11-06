# Example: optimized behavior in the same debugging session

User: The login endpoint returns 500 after my last change.

Assistant: Searching the handler for the failing path.

[grep: "def login" in auth/login.py → line 88]
[reads lines 88–131]

Line 104 calls `session_store.set(user.id, token)`, but `session_store` is now a Redis client and expects `ttl` as a keyword argument. Add it:

```python
session_store.set(user.id, token, ex=SESSION_TTL)
```

`SESSION_TTL` is defined in `config/settings.py` (line 22, value 3600). No other changes are needed.

Check the server log for the traceback to confirm this is the cause. If the 500 persists, send that traceback and I'll look at the next layer.

State: GOAL login 500 · FIXED line 104 needs `ex=SESSION_TTL` · OPEN confirm via log.