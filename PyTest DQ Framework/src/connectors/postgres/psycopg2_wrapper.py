print("Loading psycopg2_wrapper.py")
"""
Wrapper module to handle psycopg2 imports regardless of whether
the regular psycopg2 or psycopg2-binary is installed.
"""
try:
    import psycopg2
    from psycopg2 import extensions, extras, sql, pool
except ImportError:
    # If direct import fails, psycopg2-binary should be available
    # The binary version provides the same interface
    import psycopg2.extensions
    import psycopg2.extras
    import psycopg2.sql
    import psycopg2.pool
    from psycopg2 import extensions, extras, sql, pool

# Re-export everything so imports work the same way
__all__ = ['psycopg2', 'extensions', 'extras', 'sql', 'pool']