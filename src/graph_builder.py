"""Knowledge graph construction utilities."""


def build_graph(nodes_path: str, edges_path: str) -> tuple[str, str]:
    """Return input file paths for downstream KG processing pipelines."""
    return nodes_path, edges_path
