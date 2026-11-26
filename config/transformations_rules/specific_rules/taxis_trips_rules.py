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
    ], 
    'new_columns': { 
        'VendorName': { 
            'column_data' : {
                '1': 'Creative Mobile Technologies, LLC' , 
                '2' : 'Curb Mobility, LLC' , 
                '6': 'Myle Technologies Inc' , 
                '7': 'Helix'
            } , 
            'column': 'VendorID'
        } , 
        'PaymentTypeName': { 
            'column_data' : {
                '0' :'Flex Fare trip',
                '1' : 'Credit card',
                '2' : 'Cash',
                '3' : 'No charge',
                '4' : 'Dispute',
                '5' : 'Unknown',
                '6' : 'Voided trip'
            }  , 
            'column': 'payment_type'
        }, 
        'RatecodeName': { 
            'column_data': {
                '1' : 'Standard rate',
                '2' : 'JFK',
                '3' : 'Newark',
                '4' : 'Nassau or Westchester',
                '5' : 'Negotiated fare',
                '6' : 'Group ride',
                '99' : 'Null/unknown'
            } , 
            'column': 'RatecodeID'
        }
    }
}
