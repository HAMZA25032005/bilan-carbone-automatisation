-- Chaque clé de répartition (campagne, type, territoire) doit sommer à 100 %.
select campagne, type_cle, code_territoire, sum(coefficient) as total
from {{ ref('ref_cle_repartition') }}
group by campagne, type_cle, code_territoire
having abs(sum(coefficient) - 1) > 0.0001
