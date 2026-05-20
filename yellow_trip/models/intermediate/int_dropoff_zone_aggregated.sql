with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

aggregated as (
  select
    dropoff_zone,
    count(dropoff_zone) as total_pickup
  from int_trip_zone_joined
  group by dropoff_zone
)

select * from aggregated

