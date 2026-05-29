with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

aggregated as (
  select
    pickup_zone,
    dropoff_zone,
    count(*) as total,
    sum(total_amount) as total_amount
  from ref
  group by pickup_zone, dropoff_zone
)

select * from aggregated
