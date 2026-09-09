with source as (
  select * from {{ source('zone', 'taxi_zone_lookup') }}
),

renamed as (
  select
    LocationID as location_id,
    Borough as borough,
    Zone as zone,
    service_zone
  from source
)

select * from renamed

