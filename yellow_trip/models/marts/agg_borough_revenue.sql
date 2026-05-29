with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

aggregated as (
  select
    pickup_borough,
    dropoff_borough,
    count(*) as total,
    sum(total_amount) as total_amount
  from ref
  group by pickup_borough, dropoff_borough
)

select * from aggregated
