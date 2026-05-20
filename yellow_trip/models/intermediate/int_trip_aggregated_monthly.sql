-- assuming taunny bener yeeeee

with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

aggregated as (
  select 
    month(dropoff_datetime) as month,
    CONCAT('$', FORMAT('{:,.2f}', sum(total_amount))) as total_amount_in_usd
  from ref
  group by
    month(dropoff_datetime)
  order by
    month(dropoff_datetime) asc
)

select * from aggregated
