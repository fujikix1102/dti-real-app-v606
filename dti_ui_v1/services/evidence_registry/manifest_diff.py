def compare_manifest(a,b):

    return {

        "asset_count":
            (
                a.get("asset_count"),
                b.get("asset_count")
            ),

        "schema_version":
            (
                a.get("schema_version"),
                b.get("schema_version")
            ),

        "checksum":
            (
                a.get("checksum"),
                b.get("checksum")
            )
    }
