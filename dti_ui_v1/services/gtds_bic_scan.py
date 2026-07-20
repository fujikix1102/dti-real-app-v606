from pathlib import Path
import math
import csv


def load_profile(path):

    rows=[]

    with open(path,newline="") as f:

        reader=csv.DictReader(
            f,
            delimiter="\t"
        )

        for r in reader:

            rows.append(
                {
                    "z":float(r["z_i"]),
                    "y":float(r["y_i"]),
                    "w":float(r["w_i"])
                }
            )

    return rows



def weighted_mean(rows):

    sw=sum(
        r["w"]
        for r in rows
    )

    if sw==0:
        return 0.0

    return sum(
        r["w"]*r["y"]
        for r in rows
    )/sw



def chi2(rows,mu):

    return sum(
        r["w"]*(r["y"]-mu)**2
        for r in rows
    )



def run_gtds_scan(path):

    data=load_profile(path)

    n=len(data)

    mu0=weighted_mean(data)

    chi20=chi2(
        data,
        mu0
    )

    bic0=chi20 + math.log(n)


    results=[]


    for k in range(5,n-5):

        left=data[:k+1]
        right=data[k+1:]


        mu1=weighted_mean(left)
        mu2=weighted_mean(right)


        chi21=(
            chi2(left,mu1)
            +
            chi2(right,mu2)
        )


        bic1=chi21 + 3*math.log(n)


        results.append(
            {
                "k":k,
                "zc":data[k]["z"],
                "mu1":mu1,
                "mu2":mu2,
                "delta_bic":
                    bic1-bic0
            }
        )


    best=min(
        results,
        key=lambda x:x["delta_bic"]
    )


    label="CONTINUOUS_SUPPORTED"


    if best["delta_bic"] < -10:

        label="CHANGE_POINT_PATTERN"


    return {

        "points":n,

        "bic0":bic0,

        "best":best,

        "delta_bic_min":
            best["delta_bic"],

        "classification":
            label,

        "claim_boundary":
            [
                "diagnostic_only",
                "no_posterior",
                "no_detection_claim"
            ]

    }
