-- Typage des saisies brutes. Aucune règle métier ici.
-- raw_saisie garde toutes les versions d'un fichier ; on ne retient que le
-- dernier chargement de chaque fichier source (version corrigée par le data owner).
with derniere_version as (
    select fichier_source, max(charge_le) as charge_le
    from {{ source('raw', 'raw_saisie') }}
    group by fichier_source
)
select
    md5(r.hash_fichier || '-' || cast(r.numero_ligne as varchar)) as id_saisie,
    r.run_id,
    r.fichier_source,
    r.hash_fichier,
    r.onglet,
    r.numero_ligne,
    r.charge_le,
    r.campagne,
    upper(trim(domaine))                       as domaine,
    upper(trim(territoire))                    as code_territoire,
    libelle,
    try_cast(replace(quantite, ',', '.') as decimal(18, 4)) as quantite,
    quantite                                   as quantite_brute,
    unite,
    lower(trim(data_owner))                    as data_owner,
    commentaire
from {{ source('raw', 'raw_saisie') }} r
join derniere_version d
    on  d.fichier_source = r.fichier_source
    and d.charge_le      = r.charge_le
where r.campagne = {{ var('campagne') }}
