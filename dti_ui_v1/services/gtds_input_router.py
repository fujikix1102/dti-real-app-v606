from pathlib import Path


def resolve_gtds_input(asset):

    if asset is None:

        return None


    path=Path(
        asset
    )


    if not path.exists():

        return None


    return path
