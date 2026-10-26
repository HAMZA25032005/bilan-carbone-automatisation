"""Lance la chaîne complète : ingestion Excel -> dbt (seeds, modèles, tests) -> export Climatip.

Usage : python lancer.py [--fictif]
  --fictif  régénère d'abord les fichiers Excel de test dans data/entree/
"""
import os
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
os.environ.setdefault("BC_DUCKDB_PATH", str(RACINE / "bilan_carbone.duckdb"))
DBT = ["dbt", "--no-use-colors"]
ARGS_DBT = ["--project-dir", str(RACINE / "transformation"), "--profiles-dir", str(RACINE / "transformation")]


def etape(titre: str, commande: list[str]) -> None:
    print(f"\n=== {titre} ===", flush=True)
    if subprocess.run(commande, cwd=RACINE).returncode != 0:
        sys.exit(f"Échec à l'étape : {titre}")


def main() -> None:
    if "--fictif" in sys.argv:
        etape("Génération des données fictives", [sys.executable, "scripts/generer_donnees_fictives.py"])
    etape("Ingestion des fichiers Excel", [sys.executable, "scripts/ingerer_excel.py"])
    etape("Chargement des référentiels", DBT + ["seed"] + ARGS_DBT)
    etape("Transformation et tests", DBT + ["build", "--exclude", "resource_type:seed"] + ARGS_DBT)
    etape("Export Climatip", [sys.executable, "scripts/exporter_climatip.py"])


if __name__ == "__main__":
    main()
