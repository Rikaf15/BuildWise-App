import pandas as pd

# Data material berdasarkan SNI
MATERIAL_DATA = {
    'beton': {
        'density': 2400,  # kg/m³
        'compressive_strength': 25,  # MPa
        'cost_per_m3': 800000,  # Rupiah
        'foundation_types': ['Pondasi Telapak', 'Pondasi Menerus', 'Pondasi Tiang Pancang']
    },
    'baja': {
        'density': 7850,  # kg/m³
        'yield_strength': 240,  # MPa
        'cost_per_kg': 15000,  # Rupiah
        'foundation_types': ['Pondasi Baja', 'Pondasi Komposit', 'Pondasi Tiang Baja']
    },
    'campuran': {
        'density': 2200,  # kg/m³
        'compressive_strength': 20,  # MPa
        'cost_per_m3': 650000,  # Rupiah
        'foundation_types': ['Pondasi Campuran', 'Pondasi Batu Kali', 'Pondasi Rollag']
    }
}

SNI_LOAD_FACTORS = {
    'dead_load': 1.2,
    'live_load': 1.6,
    'wind_load': 1.0,
    'earthquake_load': 1.0
}
