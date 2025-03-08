#/usr/bin/bash

set -ueo pipefail

function send_request() {
    path="$1"
    corpus="$2"
    t_dir="$3"

    if [ "$t_dir" = "" ] ; then
        t_dir="$corpus"
    fi

    bname="$( basename "$path" .txt)"
    target="$( dirname "$path" | sed "s/_txt/_conllu/g" )/$bname.conllu"
    mkdir -p "$( dirname "$target")"

    if [ -f "$target" ] ; then
        echo "skipping $1: already parsed"
        return
    fi

    echo "parse $1 -> $target"

    file_processing/stdin_conllu.py <"$path" >"$target"
}

export -f send_request

corpus="$1"
t_dir=""

if [ "$#" -gt 1 ] ; then
    t_dir="$2"
fi

find "corpora_selected_txt/$corpus" -name '*.txt' -exec bash -c 'send_request "$0" "$1" "$2"' {} "$corpus" "$t_dir" \;

# this was needed to convert the encoding. some conversions may have failed.
# find "_local/$corpus" -name '*.txt' -exec iconv -f WINDOWS-1250 -t UTF-8 {} -o {} \; 