"""
Patient outcome data generator for early diagnosis analysis
"""
import numpy as np
import pandas as pd
import logging
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PatientDataGenerator:
    """
    Generate synthetic patient outcome data
    """
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        
        self.diseases = [
            "Breast Cancer", "Lung Cancer", "Colorectal Cancer", 
            "Prostate Cancer", "Diabetes", "Heart Disease"
        ]
        
        self.stages = ["Early", "Intermediate", "Late"]
        self.treatments = ["Surgery", "Chemotherapy", "Radiation", "Immunotherapy", "Combined"]
    
    def generate_patient_outcomes(self, n_patients: int = 1000) -> pd.DataFrame:
        """Generate patient outcome data"""
        data = []
        
        for i in range(n_patients):
            disease = random.choice(self.diseases)
            
            # Diagnosis stage with bias towards late stage
            stage_weights = [0.3, 0.35, 0.35]
            if disease in ["Breast Cancer", "Prostate Cancer"]:
                stage_weights = [0.4, 0.35, 0.25]  # More early detection
            
            stage = random.choices(self.stages, weights=stage_weights)[0]
            
            age_at_diagnosis = random.randint(35, 80)
            gender = random.choice(["Male", "Female"])
            
            # Treatment
            treatment = random.choice(self.treatments)
            
            # Survival time based on stage
            if stage == "Early":
                survival_months = random.randint(60, 180)
                survival_rate = np.random.uniform(0.85, 0.98)
            elif stage == "Intermediate":
                survival_months = random.randint(24, 84)
                survival_rate = np.random.uniform(0.55, 0.80)
            else:  # Late
                survival_months = random.randint(6, 48)
                survival_rate = np.random.uniform(0.20, 0.50)
            
            # Quality of life scores
            qol_scores = []
            base_qol = 80 if stage == "Early" else 60 if stage == "Intermediate" else 40
            for month in range(0, min(36, survival_months), 3):
                qol = base_qol + np.random.normal(0, 10)
                qol = max(0, min(100, qol))
                qol_scores.append(round(qol, 1))
            
            # Treatment costs
            if stage == "Early":
                treatment_cost = random.randint(15000, 40000)
                yearly_ongoing_cost = random.randint(3000, 10000)
            elif stage == "Intermediate":
                treatment_cost = random.randint(30000, 70000)
                yearly_ongoing_cost = random.randint(8000, 18000)
            else:
                treatment_cost = random.randint(50000, 120000)
                yearly_ongoing_cost = random.randint(15000, 30000)
            
            # Healthcare utilization
            hospitalizations = random.randint(1, 5) if stage == "Late" else random.randint(0, 2)
            doctor_visits = random.randint(4, 12) if stage == "Late" else random.randint(2, 6)
            
            patient = {
                "patient_id": f"P{str(i+1).zfill(4)}",
                "disease": disease,
                "stage": stage,
                "age_at_diagnosis": age_at_diagnosis,
                "gender": gender,
                "treatment": treatment,
                "survival_months": survival_months,
                "survival_rate": round(survival_rate, 3),
                "quality_of_life_scores": qol_scores,
                "avg_qol_score": round(np.mean(qol_scores), 1) if qol_scores else 0,
                "treatment_cost": treatment_cost,
                "yearly_ongoing_cost": yearly_ongoing_cost,
                "total_cost_5yr": round(treatment_cost + (yearly_ongoing_cost * 5), 0),
                "hospitalizations": hospitalizations,
                "doctor_visits": doctor_visits,
                "diagnosis_delay_months": random.randint(0, 24) if stage == "Late" else random.randint(0, 6),
                "alive": survival_months > 60,
                "comorbidities": random.randint(0, 3),
                "screening_participation": random.choice([True, False]) if stage in ["Early", "Intermediate"] else False,
                "symptoms_at_diagnosis": random.choice([True, False])
            }
            
            data.append(patient)
        
        df = pd.DataFrame(data)
        logger.info(f"Generated {len(df)} patient outcome records")
        return df
    
    def generate_quality_of_life_data(self) -> pd.DataFrame:
        """Generate quality of life data by disease and stage"""
        data = []
        
        for disease in self.diseases:
            for stage in self.stages:
                # Baseline QOL scores
                if stage == "Early":
                    baseline_qol = np.random.uniform(75, 90)
                    qol_improvement = np.random.uniform(5, 15)
                elif stage == "Intermediate":
                    baseline_qol = np.random.uniform(55, 75)
                    qol_improvement = np.random.uniform(10, 25)
                else:
                    baseline_qol = np.random.uniform(30, 55)
                    qol_improvement = np.random.uniform(15, 35)
                
                # QOL over time
                qol_timeline = []
                for month in range(0, 25, 3):
                    if month < 6:
                        qol = baseline_qol - np.random.uniform(5, 15)
                    elif month < 12:
                        qol = baseline_qol + qol_improvement * 0.5
                    else:
                        qol = baseline_qol + qol_improvement
                    
                    qol = max(0, min(100, qol))
                    qol_timeline.append(round(qol, 1))
                
                # Domain-specific QOL
                domains = {
                    "physical": np.random.uniform(40, 90),
                    "emotional": np.random.uniform(40, 90),
                    "social": np.random.uniform(40, 90),
                    "functional": np.random.uniform(40, 90)
                }
                
                data.append({
                    "disease": disease,
                    "stage": stage,
                    "baseline_qol": round(baseline_qol, 1),
                    "qol_improvement": round(qol_improvement, 1),
                    "qol_timeline": qol_timeline,
                    "domain_scores": domains,
                    "avg_domain_score": round(np.mean(list(domains.values())), 1)
                })
        
        df = pd.DataFrame(data)
        logger.info(f"Generated {len(df)} quality of life records")
        return df
