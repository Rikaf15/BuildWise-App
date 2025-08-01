import math
from data.material_data import MATERIAL_DATA, SNI_LOAD_FACTORS

class BuildingCalculator:
    def __init__(self, length, width, floors, structure_type):
        self.length = length
        self.width = width
        self.floors = floors
        self.structure_type = structure_type
        self.material = MATERIAL_DATA[structure_type]
    
    def calculate_area(self):
        return self.length * self.width
    
    def calculate_volume(self):
        # Asumsi tinggi per lantai 3.5m
        return self.calculate_area() * self.floors * 3.5
    
    def calculate_dead_load(self):
        # Beban mati struktur
        volume = self.calculate_volume()
        structural_load = volume * self.material['density'] * 0.15  # 15% dari volume untuk struktur
        return structural_load
    
    def calculate_live_load(self):
        # Beban hidup berdasarkan SNI (250 kg/m² untuk hunian)
        area = self.calculate_area()
        live_load_per_floor = area * 250  # kg/m²
        return live_load_per_floor * self.floors
    
    def calculate_total_load(self):
        dead_load = self.calculate_dead_load()
        live_load = self.calculate_live_load()
        
        # Faktor beban SNI
        factored_dead = dead_load * SNI_LOAD_FACTORS['dead_load']
        factored_live = live_load * SNI_LOAD_FACTORS['live_load']
        
        return factored_dead + factored_live
    
    def get_load_category(self):
        total_load = self.calculate_total_load()
        area = self.calculate_area()
        load_per_area = total_load / area
        
        if load_per_area < 1000:
            return "Ringan"
        elif load_per_area < 2000:
            return "Sedang"
        else:
            return "Berat"
    
    def get_foundation_recommendation(self):
        load_category = self.get_load_category()
        foundations = self.material['foundation_types']
        
        if load_category == "Ringan":
            return foundations[0]
        elif load_category == "Sedang":
            return foundations[1]
        else:
            return foundations[2]
    
    def check_overdesign(self):
        area = self.calculate_area()
        if area > 500 and self.floors == 1:
            return "Potensi overdesign: Bangunan terlalu luas untuk 1 lantai"
        elif self.floors > 3 and self.structure_type == "campuran":
            return "Potensi overdesign: Material campuran tidak cocok untuk >3 lantai"
        else:
            return "Desain sesuai standar"
    
    def estimate_cost(self):
        volume = self.calculate_volume()
        if 'cost_per_m3' in self.material:
            return volume * self.material['cost_per_m3']
        else:
            # Untuk baja (per kg)
            weight = volume * self.material['density']
            return weight * self.material['cost_per_kg']
