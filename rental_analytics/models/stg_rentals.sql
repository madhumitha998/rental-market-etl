WITH raw_rentals AS (
    SELECT * FROM {{ source('raw_data', 'troy_rentals') }}
)

SELECT
    id,
    formattedaddress AS address,
    city,
    state,
    zipcode,
    -- Using double quotes for longitude/latitude as they are often lowercase in JSON
    latitude,
    longitude,
    
    -- Property specs for Power BI filters
    propertytype,
    bedrooms,
    bathrooms,
    squarefootage,
    
    price,
    status,
    
    -- Your proven JSON parsing logic
    PARSE_JSON(REPLACE(NULLIF(hoa, ''), '''', '"')):"fee"::NUMBER AS hoa_fee,
    PARSE_JSON(REPLACE(NULLIF(listingagent, ''), '''', '"')):"name"::STRING AS agent_name,
    PARSE_JSON(REPLACE(NULLIF(listingagent, ''), '''', '"')):"email"::STRING AS agent_email,
    PARSE_JSON(REPLACE(NULLIF(listingoffice, ''), '''', '"')):"name"::STRING AS office_name,

    CAST(listeddate AS DATE) AS date_listed

FROM raw_rentals