"""
Cost-Benefit Analysis for Early Disease Diagnosis
"""
import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class CostBenefitAnalyzer:
    """
    Analyze healthcare costs and benefits of early diagnosis
    """
    
    def __init__(self):
        self.discount_rate = 0.03  # 3% discount rate
        self.productivity_cost_per_day = 200  # USD
        
    def analyze(self, patient_data: pd.DataFrame) -> Dict:
        """Complete cost-benefit analysis"""
        
        # Calculate costs
        cost_analysis = self._calculate_costs(patient_data)
        
        # Calculate benefits
        benefit_analysis = self._calculate_benefits(patient_data)
        
        # Calculate ROI
        roi_analysis = self._calculate_roi(cost_analysis, benefit_analysis)
        
        return {
            'cost_analysis': cost_analysis,
            'benefit_analysis': benefit_analysis,
            'roi_analysis': roi_analysis,
            'summary': self._generate_summary(
                cost_analysis, benefit_analysis, roi_analysis
            )
        }
    
    def _calculate_costs(self, patient_data: pd.DataFrame) -> Dict:
        """Calculate healthcare costs by stage"""
        costs = {}
        
        for stage in patient_data['stage'].unique():
            stage_data = patient_data[patient_data['stage'] == stage]
            
            # Treatment costs
            avg_treatment_cost = stage_data['treatment_cost'].mean()
            avg_ongoing_cost = stage_data['yearly_ongoing_cost'].mean()
            
            # Total 5-year cost (discounted)
            total_cost_5yr = avg_treatment_cost
            for year in range(1, 6):
                discounted_cost = avg_ongoing_cost / ((1 + self.discount_rate) ** year)
                total_cost_5yr += discounted_cost
            
            # Hospitalization costs
            avg_hospitalizations = stage_data['hospitalizations'].mean()
            hospitalization_cost = avg_hospitalizations * 5000  # $5000 per hospitalization
            
            # Total cost per patient
            total_per_patient = total_cost_5yr + hospitalization_cost
            
            costs[stage] = {
                'avg_treatment_cost': round(avg_treatment_cost, 0),
                'avg_ongoing_cost': round(avg_ongoing_cost, 0),
                'total_cost_5yr': round(total_cost_5yr, 0),
                'hospitalization_cost': round(hospitalization_cost, 0),
                'total_per_patient': round(total_per_patient, 0),
                'patient_count': len(stage_data)
            }
        
        # Calculate savings
        early_cost = costs.get('Early', {}).get('total_per_patient', 0)
        late_cost = costs.get('Late', {}).get('total_per_patient', 0)
        
        costs['savings'] = {
            'per_patient': round(late_cost - early_cost, 0),
            'per_100k_patients': round((late_cost - early_cost) * 100000, 0),
            'percentage_savings': round(((late_cost - early_cost) / late_cost) * 100, 1)
        }
        
        return costs
    
    def _calculate_benefits(self, patient_data: pd.DataFrame) -> Dict:
        """Calculate benefits of early diagnosis"""
        benefits = {}
        
        # Quality of Life (QALY) benefits
        qol_by_stage = patient_data.groupby('stage')['avg_qol_score'].mean()
        survival_by_stage = patient_data.groupby('stage')['survival_months'].mean()
        
        # Calculate QALYs
        qaly_early = (qol_by_stage.get('Early', 0) / 100) * (survival_by_stage.get('Early', 0) / 12)
        qaly_late = (qol_by_stage.get('Late', 0) / 100) * (survival_by_stage.get('Late', 0) / 12)
        
        benefits['qaly_gain'] = {
            'early_qaly': round(qaly_early, 2),
            'late_qaly': round(qaly_late, 2),
            'qaly_gain': round(qaly_early - qaly_late, 2),
            'per_100k_patients': round((qaly_early - qaly_late) * 100000, 0)
        }
        
        # Productivity gains
        productivity_loss_early = (survival_by_stage.get('Early', 0) / 12) * self.productivity_cost_per_day * 30
        productivity_loss_late = (survival_by_stage.get('Late', 0) / 12) * self.productivity_cost_per_day * 30
        
        benefits['productivity'] = {
            'early_loss': round(productivity_loss_early, 0),
            'late_loss': round(productivity_loss_late, 0),
            'gain': round(productivity_loss_late - productivity_loss_early, 0),
            'per_100k_patients': round((productivity_loss_late - productivity_loss_early) * 100000, 0)
        }
        
        # Quality of life improvement
        qol_improvement = {
            'early_avg': round(qol_by_stage.get('Early', 0), 1),
            'late_avg': round(qol_by_stage.get('Late', 0), 1),
            'improvement': round(qol_by_stage.get('Early', 0) - qol_by_stage.get('Late', 0), 1)
        }
        
        benefits['quality_of_life'] = qol_improvement
        
        return benefits
    
    def _calculate_roi(self, cost_analysis: Dict, benefit_analysis: Dict) -> Dict:
        """Calculate Return on Investment"""
        
        # Cost per patient for screening program
        screening_cost_per_patient = 500  # Average cost of screening
        screening_effectiveness = 0.70   # 70% of cases detected early
        
        # Savings from early detection
        savings_per_patient = cost_analysis['savings']['per_patient']
        
        # ROI calculation
        net_benefit_per_screened = (savings_per_patient * screening_effectiveness) - screening_cost_per_patient
        roi = (net_benefit_per_screened / screening_cost_per_patient) * 100
        
        return {
            'screening_cost_per_patient': screening_cost_per_patient,
            'screening_effectiveness': screening_effectiveness,
            'savings_per_patient': savings_per_patient,
            'net_benefit_per_screened': round(net_benefit_per_screened, 0),
            'roi_percentage': round(roi, 1),
            'break_even_effectiveness': round((screening_cost_per_patient / savings_per_patient) * 100, 1),
            'payback_period_years': round(screening_cost_per_patient / (savings_per_patient / 5), 1)
        }
    
    def _generate_summary(self, cost_analysis: Dict, 
                         benefit_analysis: Dict,
                         roi_analysis: Dict) -> Dict:
        """Generate cost-benefit summary"""
        
        summary = {
            'total_savings_per_patient': cost_analysis['savings']['per_patient'],
            'qaly_gain_per_patient': benefit_analysis['qaly_gain']['qaly_gain'],
            'roi_percentage': roi_analysis['roi_percentage'],
            'is_cost_effective': roi_analysis['roi_percentage'] > 100,
            'recommendation': 'Strongly Recommended' if roi_analysis['roi_percentage'] > 200 else
                             'Recommended' if roi_analysis['roi_percentage'] > 100 else
                             'Consider with Caution' if roi_analysis['roi_percentage'] > 50 else
                             'Not Recommended'
        }
        
        return summary
