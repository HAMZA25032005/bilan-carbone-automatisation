-- La démultiplication ne crée ni ne perd de quantité : pour chaque saisie valide,
-- la somme répartie égale la quantité saisie.
select s.id_saisie, s.quantite, sum(r.quantite_repartie) as total_reparti
from {{ ref('int_saisie_controlee') }} s
left join {{ ref('fct_repartition') }} r on r.id_saisie = s.id_saisie
where s.motif_anomalie is null
group by s.id_saisie, s.quantite
having sum(r.quantite_repartie) is null
    or abs(sum(r.quantite_repartie) - s.quantite) > 0.01
