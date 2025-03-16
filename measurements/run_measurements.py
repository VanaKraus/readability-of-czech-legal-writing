#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser
import re

import pandas as pd
import requests


def log(str, newline: bool = False):
    sys.stdout.write(str + " ")
    sys.stdout.flush()
    if newline:
        print()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", nargs=1, type=str, help="/raw REST endpoint")
    parser.add_argument("-s", "--selected", nargs=1, type=str, help=".conllu directory")
    parser.add_argument("-c", "--csv", nargs=1, type=str, help="target CSV name")

    args = parser.parse_args(sys.argv[1:])

    df = None

    # reader = PlaintextCorpusReader(args.conllu[0], r".*\.conllu")

    df_selected_documents = pd.read_csv(args.selected[0])
    df_selected_documents["target_fpath_conllu"] = (
        df_selected_documents["target_fpath"]
        .str.replace("corpora_selected_txt", "corpora_selected_conllu")
        .str.replace(".txt", ".conllu")
    )

    for sd_row in df_selected_documents.iterrows():
        fpath_txt = sd_row[1]["target_fpath"]
        fpath_conllu = sd_row[1]["target_fpath_conllu"]

        log(fpath_conllu)

        # request
        # fpath = os.path.join(args.conllu[0], file)
        df_row = {"fpath": fpath_txt}

        request = requests.post(
            args.url[0] + "?profile=minimal_verbose",
            files={"file": open(fpath_conllu, "r")},
        )
        result = request.json()

        log("Rq")

        # rules
        conllu = result["modified_conllu"]

        measur_found = re.findall(
            r"(Rule[a-zA-Z]+):([0-9a-f]{8}):measur:([a-z\_]+)=([0-9\.]+)", conllu
        )
        df_measur = (
            pd.DataFrame(measur_found, columns=["rule", "id", "measur", "value"])
            .drop_duplicates()
            .reset_index(drop=True)
            .astype({"value": "float"})
        )

        rules_found = re.findall(r"(Rule[a-zA-Z]+):([0-9a-f]{8})", conllu)
        df_rules = (
            pd.DataFrame(rules_found, columns=["rule", "id"])
            .drop_duplicates()
            .reset_index(drop=True)
        )

        log("Ru")

        # rule counts
        df_counts = df_rules.groupby("rule").agg({"id": "nunique"})

        for count_row in df_counts.iterrows():
            df_row[count_row[0]] = count_row[1]["id"]

        log("RuC")

        # rule measurements
        df_measur_vals = (
            df_measur.groupby(["rule", "measur"])
            .agg({"value": ["mean", "std"]})
            .reset_index()
        )
        df_measur_vals["var_coeff"] = (
            df_measur_vals["value"]["std"] / df_measur_vals["value"]["mean"]
        )

        for measur_row in df_measur_vals.iterrows():
            meas_name = (
                f"{measur_row[1]['rule'].values[0]}.{measur_row[1]['measur'].values[0]}"
            )
            df_row[meas_name] = measur_row[1]["value"]["mean"]

            # represent missing variation coefficient by -1 to remain consistent with the metrics
            var_coeff = measur_row[1]["var_coeff"].values[0]
            df_row[f"{meas_name}.v"] = var_coeff or -1

        log("RuM")

        # metrics
        for item in result["metrics"]:
            k, v = list(item.items())[0]
            df_row[k] = v

        log("Me")

        # df handling
        if df is None:
            df = pd.DataFrame(columns=df_row.keys())

        df.loc[len(df)] = df_row

        for k in df_row.keys():
            if k not in df.columns:
                df[k] = [None] * (len(df) - 1) + [df_row[k]]
                log(f"added {k}")

        log("D", True)

    # reorder columns
    new_order = ["fpath"] + sorted(c for c in df.columns if c.startswith("Rule"))
    new_order += sorted(c for c in df.columns if c not in new_order)

    df = df[new_order]

    df_selected_documents = df_selected_documents.drop(columns=["target_fpath_conllu"])

    df_result = (
        df_selected_documents.rename(columns={"target_fpath": "fpath"})
        .set_index("fpath")
        .join(df.set_index("fpath"))
        .reset_index()
    )

    df_result.to_csv(args.csv[0], index=False)
