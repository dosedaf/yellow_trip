with ref as (
  select * from {{ ref('int_trip_zone_joined') }}
),

aggregated as (
  select
    payment_type,
    count(*) as total_payment,
    sum(total_amount) as total_amount
  from ref
  group by payment_type
)

select * from aggregated
