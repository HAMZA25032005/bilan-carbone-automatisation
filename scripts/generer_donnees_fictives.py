"""Génère des fichiers Excel de saisie FICTIFS dans data/entree/.

Les fichiers imitent les défauts réels attendus (en-têtes variables, lignes
vides, territoire inconnu, quantité manquante) pour tester l'ingestion et les
contrôles qualité. Aucune donnée TDF.
"""
from pathlib import Path

from openpyxl import Workbook

RACINE = Path(__file__).resolve().parents[1]
SORTIE = RACINE / "data" / "entree"

FICHIERS = {
    "saisie_VEVE-DEPL_fictif.xlsx": (
        ["Domaine", "Territoire", "Libellé", "Quantité", "Unité", "Data owner", "Commentaire"],
        [
            ["VEVE-DEPL", "T_NORD", "Trajets train", 12000, "km", "owner.a@exemple.fr", None],
            ["VEVE-DEPL", "T_SUD", "Trajets avion", 45000, "km", "owner.a@exemple.fr", None],
            [None, None, None, None, None, None, None],
            ["VEVE-DEPL", "T_IDF", "Trajets voiture", 8000, "km", "owner.b@exemple.fr", "estimation"],
            ["VEVE-DEPL", "T_OUEST", "Trajets voiture", 3000, "km", "owner.b@exemple.fr", "territoire inconnu"],
        ],
    ),
    "saisie_ENER-ELEC_fictif.xlsx": (
        # variantes d'en-têtes volontaires
        ["Code domaine", "Code territoire", "Description", "Valeur", "Unite", "Saisi par", "Commentaires"],
        [
            ["ENER-ELEC", "T_NORD", "Conso sites", 350000, "kWh", "owner.c@exemple.fr", None],
            ["ENER-ELEC", "T_SUD", "Conso sites", 280000, "kWh", "owner.c@exemple.fr", None],
            ["ENER-ELEC", "T_IDF", "Conso sites", None, "kWh", "owner.c@exemple.fr", "valeur manquante"],
        ],
    ),
}


def main() -> None:
    SORTIE.mkdir(parents=True, exist_ok=True)
    for nom, (entetes, lignes) in FICHIERS.items():
        wb = Workbook()
        ws = wb.active
        ws.title = "Saisie"
        ws.append(entetes)
        for ligne in lignes:
            ws.append(ligne)
        wb.save(SORTIE / nom)
        print(f"créé : {SORTIE / nom}")


if __name__ == "__main__":
    main()
