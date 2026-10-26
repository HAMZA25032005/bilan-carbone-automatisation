-- Couche d'export Climatip, isolée et paramétrable.
-- Le format exact (colonnes, libellés, CSV ou Excel) est à confirmer :
-- seule cette vue (et scripts/exporter_climatip.py) devra changer.
select
    campagne,
    domaine,
    code_territoire,
    code_lp,
    libelle,
    unite,
    sum(quantite_repartie) as quantite,
    max(version_regle)     as version_regle
from {{ ref('fct_repartition') }}
group by campagne, domaine, code_territoire, code_lp, libelle, unite
