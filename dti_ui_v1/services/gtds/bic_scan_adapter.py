from math import log
from pathlib import Path

from .profile_adapter import load_profile


def weighted_mean(rows):

    ys=[]
    ws=[]

    for r in rows:

        try:
            y=float(r["y"])
            w=float(r["w"])
        except Exception:
            continue

        ys.append(y)
        ws.append(w)

    if not ys:
        return 0.0

    return sum(
        y*w for y,w in zip(ys,ws)
    ) / sum(ws)



def weighted_chi2(rows,mu):

    value=0.0

    for r in rows:

        try:
            y=float(r["y"])
            w=float(r["w"])
        except Exception:
            continue

        value += w*(y-mu)**2

    return value



def run_route_a_bic(profile_path):

    profile=load_profile(
        profile_path
    )

    rows=profile.get(
        "rows",
        []
    )

    n=len(rows)

    if n < 6:

        return {
            "status":"INSUFFICIENT_POINTS",
            "points":n
        }


    mu0=weighted_mean(rows)

    chi0=weighted_chi2(
        rows,
        mu0
    )

    bic0=chi0+log(n)


    scans=[]


    for k in range(
        2,
        n-3
    ):

        left=rows[:k+1]
        right=rows[k+1:]


        mu1=weighted_mean(left)
        mu2=weighted_mean(right)


        chi1=(
            weighted_chi2(left,mu1)
            +
            weighted_chi2(right,mu2)
        )


        bic1=chi1+3*log(n)

        scans.append(
            {
                "index":k,
                "delta_bic":bic1-bic0,
                "mu_left":mu1,
                "mu_right":mu2
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
            n,

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
