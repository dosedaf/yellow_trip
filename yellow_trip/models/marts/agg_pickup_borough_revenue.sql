with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

aggregated as (
  select
    pickup_borough,
    count(*) as total_pickup,
    sum(total_amount) as total_amount
  from ref
  group by pickup_borough
)

select * from aggregated
