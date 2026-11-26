import pandas as pd
generic_rules = { 
    'yellow_taxis_trips': { 
        'fill_null_columns': {
            'VendorID': pd.NA,
            'tpep_pickup_datetime': pd.NaT,
            'tpep_dropoff_datetime': pd.NaT,
            'passenger_count': pd.NA,
            'trip_distance': pd.NA,
            'RatecodeID': pd.NA,
            'store_and_fwd_flag': 'Não-indicado',
            'PULocationID': pd.NA,
            'DOLocationID': pd.NA,
            'payment_type': pd.NA,
            'fare_amount': pd.NA,
            'extra': pd.NA,
            'mta_tax': pd.NA,
            'tip_amount': pd.NA,
            'tolls_amount': pd.NA,
            'improvement_surcharge': pd.NA,
            'total_amount': pd.NA,
            'congestion_surcharge': pd.NA,
            'Airport_fee': pd.NA,
            'cbd_congestion_fee': pd.NA ,
            'VendorName': 'Não-definido' , 
            'PaymentTypeName': 'Não-definido' , 
            'RatecodeName': 'Não-definido'
        }, 
        'columns_to_rename': {
            'VendorID': 'id_prestadora',
            'tpep_pickup_datetime': 'data_hora_inicio',
            'tpep_dropoff_datetime': 'data_hora_termino',
            'passenger_count': 'qtd_passageiros',
            'trip_distance': 'distância_viagem',
            'RatecodeID': 'id_tarifa',
            'store_and_fwd_flag': 'indicador_registro_armazenado_encaminhado',
            'PULocationID': 'id_local_embarque',
            'DOLocationID': 'id_local_desembarque',
            'payment_type': 'id_tipo_pagamento',
            'fare_amount': 'valor_tarifa',
            'extra': 'valor_taxas_extras',
            'mta_tax': 'valor_taxa_MTA',
            'tip_amount': 'valor_gorjeta',
            'tolls_amount': 'valor_pedágios',
            'improvement_surcharge': 'valor_taxa_melhoria',
            'total_amount': 'valor_total_viagem',
            'congestion_surcharge': 'valor_taxa_congestionamento',
            'Airport_fee': 'valor_taxa_aeroporto',
            'cbd_congestion_fee': 'valor_taxa_congestionamento_região_central' , 
            'VendorName': 'nome_prestadora' ,
            'PaymentTypeName': 'tipo_pagamento' , 
            'RatecodeName' :'tipo_tarifa'
        } , 
        
        'drop_duplicates': {'subset': False}
    }
}