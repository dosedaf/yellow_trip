with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

aggregated as (
  select
    dropoff_zone,
    count(*) as total_dropoff,
    sum(total_amount) as total_amount
  from ref
  group by dropoff_zone
)

select * from aggregated
