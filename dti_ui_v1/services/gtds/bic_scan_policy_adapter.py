from math import log

from .profile_adapter import load_profile
from .bic_weight_policy import detect_weight_mode,safe_weight



def mean_value(rows):

    return sum(
        float(r["y"])
        for r in rows
    ) / len(rows)



def weighted_mean(rows):

    numerator=0
    denominator=0

    for r in rows:

        w=safe_weight(r)

        numerator += float(r["y"])*w

        denominator += w


    return numerator/denominator



def calc_mean(rows,mode):

    if mode=="WEIGHTED":

        return weighted_mean(rows)

    return mean_value(rows)



def calc_chi(rows,mu,mode):

    total=0

    for r in rows:

        w=safe_weight(r) if mode=="WEIGHTED" else 1.0

        total += w*(float(r["y"])-mu)**2


    return total



def run_route_a_policy_bic(path):

    profile=load_profile(path)

    rows=profile.get(
        "rows",
        []
    )


    mode=detect_weight_mode(rows)


    if len(rows)<6:

        return {
            "status":"INSUFFICIENT_POINTS",
            "points":len(rows)
        }


    mu0=calc_mean(rows,mode)

    chi0=calc_chi(
        rows,
        mu0,
        mode
    )

    bic0=chi0+log(len(rows))


    scans=[]


    for k in range(
        2,
        len(rows)-3
    ):

        left=rows[:k+1]

        right=rows[k+1:]


        mu1=calc_mean(left,mode)

        mu2=calc_mean(right,mode)


        chi1=(
            calc_chi(left,mu1,mode)
            +
            calc_chi(right,mu2,mode)
        )


        bic1=chi1+3*log(len(rows))


        scans.append(
            {
                "index":k,
                "delta_bic":bic1-bic0
            }
        )


    best=min(
        scans,
        key=lambda x:x["delta_bic"]
    )


    return {

        "status":
            "GTDS_DIAGNOSTIC_COMPLETE",

        "points":
            len(rows),

        "bic_mode":
            mode,

        "bic0":
            bic0,

        "best_scan":
            best,

        "scan_count":
            len(scans),

        "claim_boundary":
            [
                "diagnostic_only",
                "no_posterior",
                "no_detection_claim"
            ]
    }
