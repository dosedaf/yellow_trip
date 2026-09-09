with ref as (
  select * from {{ ref('int_trip_zone_joined')}}
)

select * from ref
