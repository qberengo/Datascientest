#!/bin/sh
# Lance les 6 tests de l'API les uns après les autres.
# L'adresse de l'API vient de la variable API_HOST (par défaut 0.0.0.0).
cd "$(dirname "$0")"
for t in status_test/api_status.py \
         authentification_test/api_authentification.py \
         biketomorrow_LR/api_biketomorrow_LR.py \
         biketomorrow_KNR/api_biketomorrow_KNR.py \
         biketomorrow_LOGR/api_biketomorrow_LOGR.py \
         metrics_LR/api_metrics_LR.py; do
  python "$t"
done
