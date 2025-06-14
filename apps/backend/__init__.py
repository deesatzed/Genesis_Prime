# Enable legacy absolute-style imports of backend submodules
import importlib
import pkgutil
import sys

# Dynamically load all direct child modules of this package and expose them
# under their bare names in sys.modules so that statements like
# ``import agent`` or ``from personality_presets import X`` continue to work
# even when the backend package is executed with ``python -m``.
for _finder, _mod_name, _is_pkg in pkgutil.iter_modules(__path__):
    _full_name = f"{__name__}.{_mod_name}"
    try:
        _module = importlib.import_module(_full_name)
        # Register the module under the short name as well
        sys.modules.setdefault(_mod_name, _module)
    except Exception:
        # Silently ignore modules that raise on import during the scan;
        # they'll be imported normally when first needed.
        pass

# Temporary monkey-patch to emulate asyncpg-style `fetch` on psycopg AsyncConnection
try:
    import psycopg
    from psycopg import AsyncConnection

    async def _ac_fetch(self, query: str, *args, **kwargs):  # type: ignore[override]
        """Execute query and return all rows (async). Added for legacy code compatibility."""
        async with self.cursor(row_factory=psycopg.rows.dict_row) as cur:
            await cur.execute(query, *args, **kwargs)
            return await cur.fetchall()

    if not hasattr(AsyncConnection, "fetch"):
        AsyncConnection.fetch = _ac_fetch  # type: ignore[attr-defined]

    async def _ac_fetchrow(self, query: str, *args, **kwargs):  # type: ignore[override]
        res = await _ac_fetch(self, query, *args, **kwargs)
        return res[0] if res else None

    if not hasattr(AsyncConnection, "fetchrow"):
        AsyncConnection.fetchrow = _ac_fetchrow  # type: ignore[attr-defined]
except ImportError:
    pass