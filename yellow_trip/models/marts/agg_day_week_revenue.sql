with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

aggregated as (
  select
    dayofweek(dropoff_datetime) as day_of_week,
    count(*) as total_trips,
    min(trip_distance) as min_distance,
    max(trip_distance) as max_distance,
    avg(trip_distance) as avg_distance,
    sum(trip_distance) as total_distance,
    avg(fare_amount) as avg_fare,
    sum(fare_amount) as total_fare,
    avg(tip_amount) as avg_tip,
    sum(tip_amount) as total_tip,
    avg(total_amount) as avg_total,
    sum(total_amount) as total_amount,
  from ref
  group by
    dayofweek(dropoff_datetime)
  order by
    dayofweek(dropoff_datetime) asc
)

select * from aggregated
