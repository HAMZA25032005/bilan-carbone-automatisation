# bilan-carbone-automatisation

Chaîne automatisée du Bilan Carbone TDF (partie E) : **fichiers Excel de saisie → contrôles → démultiplication par Ligne de Produit → export Climatip**, en SQL portable (dbt), exécutable en local sur DuckDB et migrable vers Snowflake en changeant uniquement `transformation/profiles.yml`.

> ⚠️ Toutes les données du dépôt sont **fictives**.

## Installation (une fois)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/Mac : source .venv/bin/activate)
pip install -r requirements.txt
```

## Lancer la chaîne

```bash
python lancer.py --fictif   # régénère des Excel de test puis lance tout
python lancer.py            # traite les Excel présents dans data/entree/
```

Sorties dans `data/sortie/` : `climatip_*.csv` (import Climatip) et `anomalies_*.xlsx` (à renvoyer aux data owners).

## Architecture

| Étape | Où | Rôle |
|---|---|---|
| Ingestion | `scripts/ingerer_excel.py` + `config/mapping_excel.yml` | Lit les Excel, tolère les variantes d'en-têtes, trace fichier / hash / ligne / run. Un fichier renvoyé corrigé remplace l'ancienne version (historique conservé). |
| Référentiels | `transformation/seeds/` | LP, territoires, clés de répartition, règles de démultiplication versionnées par campagne. |
| Typage | `models/staging/stg_saisie.sql` | Conversion des types, dernière version de chaque fichier. |
| Contrôles | `models/intermediate/int_saisie_controlee.sql` | Motif d'anomalie par saisie (territoire inconnu, quantité manquante…). |
| Démultiplication | `models/marts/fct_repartition.sql` | 1 saisie → 1 ligne par LP via la clé désignée par la règle du domaine. |
| Anomalies | `models/marts/anomalies_saisie.sql` | Quoi corriger, qui, quel fichier, quelle ligne. |
| Export | `models/export/exp_climatip.sql` + `config/export_climatip.yml` | Couche isolée : seul endroit à adapter au format Climatip. |
| Tests | `transformation/tests/` + `schema.yml` | Clés = 100 %, conservation des quantités, unicité, intégrité LP. |

## Reste à faire

- Règles de démultiplication réelles (Pilote Bilan Carbone) → `ref_regle_demultiplication`.
- Référentiels réels : LP, clés territoire × LP, transcodage BU ↔ LP.
- Les 6 colonnes de calcul de la matrice de fusion → `fct_repartition`.
- Format d'import Climatip confirmé → `config/export_climatip.yml`.
- Test de non-régression contre la matrice de fusion 2025.
