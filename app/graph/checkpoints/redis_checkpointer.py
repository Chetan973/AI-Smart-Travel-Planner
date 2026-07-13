from langgraph.checkpoint.memory import MemorySaver


class GraphCheckpointer:
    """
    Development Checkpointer.

    Replace with Redis implementation later
    without changing graph code.
    """

    @staticmethod
    def get_checkpointer():

        return MemorySaver()