with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

aggregated as (
  select 
    pickup_zone,
    count(pickup_zone) as total_pickup
  from int_trip_zone_joined 
  group by pickup_zone
)

select * from aggregated
