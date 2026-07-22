def detect_weight_mode(rows):

    weights=[]

    for r in rows:

        w=r.get("w")

        if w is None:
            continue

        if str(w).upper()=="NA":
            continue

        try:
            float(w)
            weights.append(True)
        except Exception:
            pass


    if len(weights)==len(rows) and len(rows)>0:

        return "WEIGHTED"


    return "UNWEIGHTED"



def safe_weight(r):

    try:

        return float(r.get("w"))

    except Exception:

        return 1.0
