with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

q as (
    select 
        trip_distance,
        NTILE(4) over (order by trip_distance) as quartile
    FROM ref
)

SELECT
    quartile,
    min(trip_distance) AS range_start,
    max(trip_distance) AS range_end
FROM q AS bucketed_data
GROUP BY quartile
ORDER BY quartile

