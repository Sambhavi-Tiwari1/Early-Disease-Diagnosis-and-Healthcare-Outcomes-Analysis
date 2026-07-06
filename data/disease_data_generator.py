"""
Disease data generator for early diagnosis analysis
"""
import numpy as np
import pandas as pd
import logging
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DiseaseDataGenerator:
    """
    Generate synthetic disease incidence and outcome data
    """
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        
        self.diseases = [
            "Breast Cancer", "Lung Cancer", "Colorectal Cancer", 
            "Prostate Cancer", "Diabetes", "Heart Disease",
            "Cervical Cancer", "Ovarian Cancer"
        ]
        
        self.stages = ["Early", "Intermediate", "Late"]
        self.genders = ["Male", "Female"]
        self.age_groups = ["30-40", "41-50", "51-60", "61-70", "71-80"]
    
    def generate_disease_incidence(self) -> pd.DataFrame:
        """Generate disease incidence data"""
        data = []
        
        for disease in self.diseases:
            for age_group in self.age_groups:
                for gender in self.genders:
                    # Incidence rates per 100,000
                    base_rate = {
                        "Breast Cancer": 120,
                        "Lung Cancer": 80,
                        "Colorectal Cancer": 70,
                        "Prostate Cancer": 60,
                        "Diabetes": 200,
                        "Heart Disease": 150,
                        "Cervical Cancer": 40,
                        "Ovarian Cancer": 30
                    }.get(disease, 100)
                    
                    # Adjust by age and gender
                    age_factor = self._get_age_factor(age_group, disease)
                    gender_factor = self._get_gender_factor(gender, disease)
                    
                    incidence_rate = base_rate * age_factor * gender_factor * np.random.uniform(0.9, 1.1)
                    
                    data.append({
                        "disease": disease,
                        "age_group": age_group,
                        "gender": gender,
                        "incidence_rate_per_100k": round(incidence_rate, 1),
                        "prevalence_rate_per_100k": round(incidence_rate * np.random.uniform(2, 5), 1),
                        "mortality_rate_per_100k": round(incidence_rate * np.random.uniform(0.2, 0.6), 1)
                    })
        
        df = pd.DataFrame(data)
        logger.info(f"Generated {len(df)} disease incidence records")
        return df
    
    def _get_age_factor(self, age_group: str, disease: str) -> float:
        """Get age adjustment factor"""
        age_factors = {
            "30-40": 0.4,
            "41-50": 0.7,
            "51-60": 1.0,
            "61-70": 1.3,
            "71-80": 1.5
        }
        
        # Special adjustments for certain diseases
        if disease in ["Breast Cancer", "Cervical Cancer"] and age_group in ["30-40", "41-50"]:
            return age_factors[age_group] * 1.2
        
        return age_factors.get(age_group, 1.0)
    
    def _get_gender_factor(self, gender: str, disease: str) -> float:
        """Get gender adjustment factor"""
        if disease in ["Breast Cancer", "Cervical Cancer", "Ovarian Cancer"]:
            return 1.0 if gender == "Female" else 0.01
        elif disease == "Prostate Cancer":
            return 1.0 if gender == "Male" else 0.01
        else:
            return np.random.uniform(0.9, 1.1)
    
    def generate_survival_data(self) -> pd.DataFrame:
        """Generate survival rate data by stage"""
        data = []
        
        for disease in self.diseases:
            for stage in self.stages:
                # Base survival rates
                if stage == "Early":
                    base_rate = np.random.uniform(0.85, 0.98)
                elif stage == "Intermediate":
                    base_rate = np.random.uniform(0.60, 0.80)
                else:  # Late
                    base_rate = np.random.uniform(0.30, 0.50)
                
                # Disease-specific adjustments
                if disease in ["Breast Cancer", "Prostate Cancer"]:
                    base_rate += 0.05
                elif disease in ["Lung Cancer", "Pancreatic Cancer"]:
                    base_rate -= 0.10
                
                # Generate survival rates for each year
                survival_rates = []
                current_rate = base_rate
                for year in range(1, 6):
                    current_rate *= np.random.uniform(0.85, 0.95)
                    survival_rates.append(round(current_rate, 3))
                
                data.append({
                    "disease": disease,
                    "stage": stage,
                    "stage_numeric": self.stages.index(stage) + 1,
                    "year_1_survival": survival_rates[0],
                    "year_3_survival": survival_rates[2],
                    "year_5_survival": survival_rates[4],
                    "survival_rates": survival_rates
                })
        
        df = pd.DataFrame(data)
        logger.info(f"Generated {len(df)} survival records")
        return df
    
    def generate_disease_progression_data(self) -> pd.DataFrame:
        """Generate disease progression data"""
        data = []
        
        for disease in self.diseases:
            for stage in self.stages:
                # Progression rates
                if stage == "Early":
                    progression_rate = np.random.uniform(0.05, 0.15)
                    remission_rate = np.random.uniform(0.60, 0.80)
                elif stage == "Intermediate":
                    progression_rate = np.random.uniform(0.15, 0.30)
                    remission_rate = np.random.uniform(0.30, 0.50)
                else:
                    progression_rate = np.random.uniform(0.30, 0.50)
                    remission_rate = np.random.uniform(0.10, 0.30)
                
                data.append({
                    "disease": disease,
                    "stage": stage,
                    "progression_rate": round(progression_rate, 3),
                    "remission_rate": round(remission_rate, 3),
                    "avg_time_to_progression_months": round(np.random.uniform(6, 36), 1),
                    "avg_time_to_remission_months": round(np.random.uniform(3, 18), 1)
                })
        
        df = pd.DataFrame(data)
        logger.info(f"Generated {len(df)} disease progression records")
        return df
