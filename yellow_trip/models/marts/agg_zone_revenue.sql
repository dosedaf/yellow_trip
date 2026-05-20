with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

pu as (
  select pickup_zone from ref
),


aggregated as (
  select
    pickup,
    count(pickup_zone) as total_pickup
  from ref
  group by pickup_zone, dropoff_zone
)

select * from aggregated
