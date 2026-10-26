"""Exporte la vue exp_climatip (et les anomalies) vers data/sortie/."""
import os
from datetime import datetime
from pathlib import Path

import duckdb
import yaml

RACINE = Path(__file__).resolve().parents[1]
DB = os.environ.get("BC_DUCKDB_PATH", str(RACINE / "bilan_carbone.duckdb"))
SORTIE = RACINE / "data" / "sortie"


def main() -> None:
    conf = yaml.safe_load((RACINE / "config" / "export_climatip.yml").read_text(encoding="utf-8"))
    SORTIE.mkdir(parents=True, exist_ok=True)
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")

    con = duckdb.connect(DB, read_only=True)
    export = con.execute("select * from main.exp_climatip order by 1, 2, 3, 4").df()
    anomalies = con.execute("select * from main.anomalies_saisie order by 1, 2, 3").df()
    con.close()

    export = export[list(conf["colonnes"])].rename(columns=conf["colonnes"])
    if conf["format"] == "xlsx":
        chemin = SORTIE / f"climatip_{horodatage}.xlsx"
        export.to_excel(chemin, index=False)
    else:
        chemin = SORTIE / f"climatip_{horodatage}.csv"
        export.to_csv(chemin, index=False, sep=conf["separateur"], encoding=conf["encodage"])
    print(f"export Climatip : {chemin} ({len(export)} lignes)")

    chemin_anom = SORTIE / f"anomalies_{horodatage}.xlsx"
    anomalies.to_excel(chemin_anom, index=False)
    print(f"anomalies : {chemin_anom} ({len(anomalies)} lignes)")


if __name__ == "__main__":
    main()
