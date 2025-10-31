
class ClaimState(dict):
    """A lightweight wrapper to allow both dict and attribute-style access."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'ClaimState' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        self[name] = value

    def get(self, key, default=None):
        """Support dict-style .get()"""
        return self[key] if key in self else default

    def to_dict(self):
        """Convert back to a regular dictionary."""
        return dict(self)
