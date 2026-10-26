-- Contrôle qualité de chaque saisie : une saisie est valide si aucun motif d'anomalie.
with saisie as (
    select * from {{ ref('stg_saisie') }}
),
regle as (
    select * from {{ ref('ref_regle_demultiplication') }}
    where campagne = {{ var('campagne') }}
)
select
    s.*,
    r.type_cle,
    r.version_regle,
    case
        when s.domaine is null                     then 'DOMAINE_MANQUANT'
        when r.domaine is null                     then 'DOMAINE_SANS_REGLE'
        when t.code_territoire is null             then 'TERRITOIRE_INCONNU'
        when s.quantite_brute is null              then 'QUANTITE_MANQUANTE'
        when s.quantite is null                    then 'QUANTITE_NON_NUMERIQUE'
        when s.quantite < 0                        then 'QUANTITE_NEGATIVE'
    end as motif_anomalie
from saisie s
left join regle r
    on r.domaine = s.domaine
left join {{ ref('ref_territoire') }} t
    on t.code_territoire = s.code_territoire
