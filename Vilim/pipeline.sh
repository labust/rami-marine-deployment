#!/bin/bash

# Provjera ulaznih parametara
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <image_path> <txt_data_path> <output_csv>"
  echo "Primjer: ./run_pipeline.sh testnaSlika.jpg input.txt final_output.csv"
  exit 1
fi

# Definiraj ulazne varijable
IMAGE_PATH=$1
TXT_DATA_PATH=$2
OUTPUT_CSV=$3

# Provjera postojanja Python skripte
PIPELINE_SCRIPT="src/pipeline/merge_pipeline.py"

if [ ! -f "$PIPELINE_SCRIPT" ]; then
  echo "Greška: Python skripta $PIPELINE_SCRIPT nije pronađena!"
  exit 1
fi

# Pokretanje pipeline-a
echo "Pokrećem pipeline s parametrima:"
echo "  Slika: $IMAGE_PATH"
echo "  TXT podaci: $TXT_DATA_PATH"
echo "  CSV izlaz: $OUTPUT_CSV"

# Poziv Python pipeline skripte
python3 "$PIPELINE_SCRIPT" "$IMAGE_PATH" "$TXT_DATA_PATH" "$OUTPUT_CSV"

# Provjera je li CSV generiran
if [ -f "$OUTPUT_CSV" ]; then
  echo "Pipeline završen. CSV generiran na lokaciji: $OUTPUT_CSV"
else
  echo "Greška: CSV nije generiran. Provjeri pipeline."
  exit 1
fi
