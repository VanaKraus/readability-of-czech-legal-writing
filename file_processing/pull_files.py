#!/usr/bin/env python3

import os
import shutil

import pandas as pd

if __name__ == "__main__":
    selected_documents = pd.read_csv("dataset_preparation/selected_documents.csv")

    rows_to_remove: list[int] = []

    for i, row in selected_documents.iterrows():
        fname = row["FileName"] + ".txt"

        # gosh
        if fname == "Tucker vs Southwestern.txt":
            fname = "Tucker vs Southwestern .txt"

        if fname == "partred_Jak chránit vody a správně s nimi nakládat.txt":
            rows_to_remove += [i]
            continue

        match (row["FolderPath"]):
            case "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11372/LRT-3052/SupAdmCo.zip":
                flocation = "SupAdmCo"
            case "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11372/LRT-3052/SupCoCo.zip":
                flocation = "SupCo"
            case "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11372/LRT-3052/ConCo.zip":
                flocation = "ConCo"
            case "https://lindat.cz/repository/xmlui/bitstream/handle/11234/1-5225/LIFRLawRELEASE2.0.zip":
                flocation = os.path.join("LIFRLawRELEASE2.0", "lifr_texts", "txt")

            case _:
                flocation = os.path.join("KUK_1.0", row["FolderPath"])

        fpath = os.path.join("corpora", flocation, fname)
        target_fpath = os.path.join("corpora_selected_txt", flocation, fname)

        selected_documents.loc[i, "target_fpath"] = target_fpath

        os.makedirs(os.path.dirname(target_fpath), exist_ok=True)

        print(f"{fpath} -> {target_fpath}")

        shutil.copyfile(fpath, target_fpath)

    selected_documents = selected_documents.drop(
        selected_documents.index[rows_to_remove]
    )

    selected_documents.to_csv("file_processing/selected_documents.csv", index=False)
