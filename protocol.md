# Requirements

The main data analysis scripts are in Rmarkdown and Python 3.13. Bash scripts are used for file manipulation.

Corpora should be unpacked in a `corpora` directory prior to running the workflow.

# Workflow

## Dataset Preparation

1. run `dataset_preparation/analysis.Rmd`

## File Processing

1. `python3 file_processing/pull_files.py`
2. `find "corpora_selected_txt/ConCo" -name '*.txt' -exec iconv -f WINDOWS-1250 -t UTF-8 {} -o {} \;`
3. `find "corpora_selected_txt/SupCo" -name '*.txt' -exec iconv -f WINDOWS-1250 -t UTF-8 {} -o {} \;`
4. `bash file_processing/parse-txt.sh LIFRLawRELEASE2.0`
5. `bash file_processing/parse-txt.sh KUK_1.0`
6. `bash file_processing/parse-txt.sh ConCo`
7. `bash file_processing/parse-txt.sh SupAdmCo`
8. `bash file_processing/parse-txt.sh SupCo`

*ConCo* and *SupCo* seem to use different encoding.

Documents parsed on 2025-03-08 using `czech-pdt-ud-2.15-241121`.

## Measurements

I ran the linguistic module of the PONK App locally on port 8000.

1. `python3 measurements/run_measurements.py -s file_processing/selected_documents.csv -u http://localhost:8000/raw -c measurements/measurements.csv`

## Importance measures

1. run `importance_measures/importances.Rmd`
2. `importance_measures/format_tables.Rmd` for pre-formatted TSVs

## EFA

1. run `efa/efa.Rmd`

## Classifier

1. run `classifier/classifier.Rmd`

`classifier_legacy` and `classifier_legacy2` not used.

# Files

- `measurements/measurements.csv`: initial data as measured by the software
- `importance_measures/featcomp.csv`: variables' significances and effect sizes
- `efa/data_w_factors.csv`: data with filled NAs and factor scores
- `feat_name_mapping.csv`: a translation table for more concise variable names