from pathlib import Path


def discover_parquets(paths: dict[str, Path]) -> dict[str, list[Path]]:
    discovered = {}

    for name, directory in paths.items():
        discovered[name] = list(directory.rglob("*.parquet"))

    return discovered