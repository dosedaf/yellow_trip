with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

aggregated as (
  select
    dropoff_borough,
    count(*) as total_dropoff,
    sum(total_amount) as total_amount
  from ref
  group by dropoff_borough
)

select * from aggregated
