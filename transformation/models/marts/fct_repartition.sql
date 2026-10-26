-- Démultiplication : 1 saisie valide -> 1 ligne par Ligne de Produit,
-- selon la clé de répartition désignée par la règle du domaine.
-- TODO : ajouter les 6 colonnes de calcul de la matrice de fusion
--        (formules à récupérer auprès de la Pilote Bilan Carbone).
select
    s.id_saisie || '-' || c.code_lp           as id_repartition,
    s.id_saisie,
    s.campagne,
    s.domaine,
    s.code_territoire,
    c.code_lp,
    s.libelle,
    s.unite,
    s.quantite                                 as quantite_saisie,
    c.coefficient,
    cast(s.quantite * c.coefficient as decimal(18, 4)) as quantite_repartie,
    s.type_cle,
    s.version_regle,
    s.data_owner,
    s.fichier_source,
    s.numero_ligne,
    s.run_id,
    s.charge_le
from {{ ref('int_saisie_controlee') }} s
join {{ ref('ref_cle_repartition') }} c
    on  c.campagne        = s.campagne
    and c.type_cle        = s.type_cle
    and c.code_territoire = s.code_territoire
where s.motif_anomalie is null
