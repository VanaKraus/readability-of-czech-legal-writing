# Dataset Preparation

1. run `dataset_preparation/analysis.Rmd`

# File Processing

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

# Measurements

1. `python3 measurements/run_measurements.py -s file_processing/selected_documents.csv -u http://localhost:8000/raw -c measurements/measurements.csv`