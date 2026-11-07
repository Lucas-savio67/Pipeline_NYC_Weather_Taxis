generic_rules = { 
    'yellow_taxis_trips': { 
        'fill_null_columns': {'passenger_count': 0} , 
        'columns_to_rename': { 
            'passenger_count': 'qtd_passageiros' , 
            'payment_type': 'tipo_pagamento'
        } , 
        'drop_duplicates': {'subset': False}
    }
}