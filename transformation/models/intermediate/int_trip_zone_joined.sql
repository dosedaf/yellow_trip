select
      vendor_id,
      pickup_datetime,
      dropoff_datetime,
      passenger_count, --driver input btw
      trip_distance,
      pickup_location_id,
      dropoff_location_id,
      fare_amount,
      tip_amount,
      total_amount,
      payment_type,
      pu_zone.zone as pickup_zone,
      do_zone.zone as dropoff_zone,
      pu_zone.borough as pickup_borough,
      do_zone.borough as dropoff_borough,
      pu_zone.service_zone as pickup_service_zone,
      do_zone.service_zone as dropoff_service_zone,
from {{ ref('stg_trip__yellow_trips') }} trips

left join {{ ref('stg_zone__lookup') }} pu_zone
    on trips.pickup_location_id = pu_zone.location_id

left join {{ ref('stg_zone__lookup') }} do_zone
    on trips.dropoff_location_id = do_zone.location_id
