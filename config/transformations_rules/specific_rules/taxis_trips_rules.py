taxis_trips_rules = { 
    'essential_schema': [
        "VendorID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "PULocationID",
        "DOLocationID",
        "RatecodeID",
        "payment_type",
        
    ] , 
    'columns_types': [
        'int32', 
        'datetime64[us]',
        'datetime64[us]' , 
        'int32',
        'int32',
        'float64',
        'int64'
    ] 
}
