-- Liste à renvoyer aux data owners : quoi corriger, dans quel fichier, à quelle ligne.
select
    data_owner,
    fichier_source,
    numero_ligne,
    domaine,
    code_territoire,
    quantite_brute,
    motif_anomalie,
    charge_le
from {{ ref('int_saisie_controlee') }}
where motif_anomalie is not null
