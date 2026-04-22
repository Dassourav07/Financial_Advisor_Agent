try:
    from langfuse import Langfuse

    class Tracer:
        def __init__(self):
            self.client = Langfuse()

        def trace(self, name: str, data: dict):
            self.client.trace(name=name, metadata=data)

except ImportError:
    class Tracer:
        def trace(self, name: str, data: dict):
            pass