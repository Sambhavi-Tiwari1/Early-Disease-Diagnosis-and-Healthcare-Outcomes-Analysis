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
            stage_data = patient_data[patient_data
