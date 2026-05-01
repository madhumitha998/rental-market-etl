WITH staging AS (
    SELECT * FROM {{ ref('stg_rentals') }}
)

SELECT
    id,
    address,
    city,
    zipcode,
    latitude,
    longitude,
    bedrooms,
    bathrooms,
    squarefootage,
    
    -- The "Cost Story" Calculations
    price AS base_rent,
    COALESCE(hoa_fee, 0) AS monthly_hoa,
    (price + COALESCE(hoa_fee, 0)) AS total_monthly_cost,
    
    -- Price per Square Foot (Value Metric)
    CASE 
        WHEN squarefootage > 0 THEN ROUND((price + COALESCE(hoa_fee, 0)) / squarefootage, 2)
        ELSE NULL 
    END AS cost_per_sqft,

    agent_name,
    office_name,
    status

FROM staging
WHERE price > 0 
  -- This keeps only the 'Active' listings for your "Live" dashboard
  AND LOWER(status) = 'active'