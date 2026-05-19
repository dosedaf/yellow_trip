{{ config(materialized='table') }}

with source as (
    select * from {{ source('taxi_raw', 'yellow_tripdata') }}
),

renamed as (
    select
        VendorID                as vendor_id,
        tpep_pickup_datetime    as pickup_datetime,
        tpep_dropoff_datetime   as dropoff_datetime,
        passenger_count,
        trip_distance,
        PULocationID            as pickup_location_id,
        DOLocationID            as dropoff_location_id,
        fare_amount,
        tip_amount,
        total_amount,
        payment_type
    from source
)

select * from renamed
