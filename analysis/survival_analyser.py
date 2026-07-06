"""
Survival Analysis for Early Disease Diagnosis
"""
import numpy as np
import pandas as pd
from scipy import stats
from lifelines import KaplanMeierFitter, CoxPHFitter
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class SurvivalAnalyzer:
    """
    Analyze survival outcomes for early vs late diagnosis
    """
    
    def __init__(self):
        self.kmf = KaplanMeierFitter()
        self.cox_model = CoxPHFitter()
        
    def analyze(self, patient_data: pd.DataFrame, survival_data: pd.DataFrame) -> Dict:
        """Complete survival analysis"""
        
        # Calculate survival metrics
        survival_metrics = self._calculate_survival_metrics(survival_data)
        
        # Analyze stage-specific survival
        stage_analysis = self._analyze_stage_survival(patient_data)
        
        # Calculate survival improvement
        improvement = self._calculate_improvement(survival_metrics)
        
        # Perform Cox regression (if data available)
        hazard_analysis = self._perform_cox_analysis(patient_data)
        
        return {
            'survival_metrics': survival_metrics,
            'stage_analysis': stage_analysis,
            'improvement': improvement,
            'hazard_analysis': hazard_analysis,
            'summary': self._generate_summary(
                survival_metrics, stage_analysis, improvement
            )
        }
    
    def _calculate_survival_metrics(self, survival_data: pd.DataFrame) -> Dict:
        """Calculate survival metrics by disease and stage"""
        metrics = {}
        
        for disease in survival_data['disease'].unique():
            disease_data = survival_data[survival_data['disease'] == disease]
            
            metrics[disease] = {}
            for _, row in disease_data.iterrows():
                stage = row['stage']
                metrics[disease][stage] = {
                    'year_1_survival': row['year_1_survival'] * 100,
                    'year_3_survival': row['year_3_survival'] * 100,
                    'year_5_survival': row['year_5_survival'] * 100,
                    'survival_rates': [r * 100 for r in row['survival_rates']]
                }
        
        # Calculate averages
        avg_early = np.mean([
            metrics[d]['Early']['year_5_survival'] 
            for d in metrics if 'Early' in metrics[d]
        ])
        avg_late = np.mean([
            metrics[d]['Late']['year_5_survival'] 
            for d in metrics if 'Late' in metrics[d]
        ])
        
        metrics['average'] = {
            'early_stage_survival': round(avg_early, 1),
            'late_stage_survival': round(avg_late, 1),
            'improvement': round(avg_early - avg_late, 1)
        }
        
        return metrics
    
    def _analyze_stage_survival(self, patient_data: pd.DataFrame) -> Dict:
        """Analyze stage-specific survival from patient data"""
        analysis = {}
        
        for stage in patient_data['stage'].unique():
            stage_data = patient_data[patient_data['stage'] == stage]
            
            # Survival statistics
            survival_months = stage_data['survival_months']
            survival_rate = stage_data['survival_rate'].mean() * 100
            
            analysis[stage] = {
                'count': len(stage_data),
                'mean_survival_months': round(survival_months.mean(), 1),
                'median_survival_months': round(survival_months.median(), 1),
                'std_survival_months': round(survival_months.std(), 1),
                'survival_rate': round(survival_rate, 1),
                'survival_range': [round(survival_months.min(), 1), 
                                   round(survival_months.max(), 1)]
            }
        
        # Statistical test between stages
        early_survival = patient_data[patient_data['stage'] == 'Early']['survival_months']
        late_survival = patient_data[patient_data['stage'] == 'Late']['survival_months']
        
        if len(early_survival) > 0 and len(late_survival) > 0:
            t_stat, p_value = stats.ttest_ind(early_survival, late_survival)
            analysis['statistical_significance'] = {
                't_statistic': round(t_stat, 3),
                'p_value': round(p_value, 4),
                'significant': p_value < 0.05
            }
        
        return analysis
    
    def _calculate_improvement(self, survival_metrics: Dict) -> Dict:
        """Calculate improvement from early diagnosis"""
        improvement = {
            'by_disease': {},
            'average_improvement': survival_metrics['average']['improvement'],
            'percentage_improvement': 0
        }
        
        for disease, metrics in survival_metrics.items():
            if disease != 'average' and 'Early' in metrics and 'Late' in metrics:
                early = metrics['Early']['year_5_survival']
                late = metrics['Late']['year_5_survival']
                
                improvement['by_disease'][disease] = {
                    'early_survival': early,
                    'late_survival': late,
                    'absolute_improvement': round(early - late, 1),
                    'relative_improvement': round(((early - late) / late) * 100, 1)
                }
        
        # Overall percentage improvement
        avg_improvement = improvement['average_improvement']
        avg_late = survival_metrics['average']['late_stage_survival']
        improvement['percentage_improvement'] = round(
            (avg_improvement / avg_late) * 100, 1
        )
        
        return improvement
    
    def _perform_cox_analysis(self, patient_data: pd.DataFrame) -> Dict:
        """Perform Cox proportional hazards analysis"""
        try:
            # Prepare data for Cox analysis
            cox_data = patient_data.copy()
            cox_data['survival_time'] = cox_data['survival_months']
            cox_data['event_occurred'] = ~cox_data['alive']
            
            # Stage encoding
            stage_map = {'Early': 1, 'Intermediate': 2, 'Late': 3}
            cox_data['stage_encoded'] = cox_data['stage'].map(stage_map)
            
            # Fit Cox model
            self.cox_model.fit(
                cox_data,
                duration_col='survival_time',
                event_col='event_occurred',
                formula='stage_encoded + age_at_diagnosis + comorbidities'
            )
            
            hazard_ratios = self.cox_model.hazard_ratios_.to_dict()
            confidence_intervals = self.cox_model.confidence_intervals_.to_dict()
            
            return {
                'hazard_ratios': hazard_ratios,
                'confidence_intervals': confidence_intervals,
                'summary': self.cox_model.summary.to_dict(),
                'log_likelihood': self.cox_model.log_likelihood_
            }
            
        except Exception as e:
            logger.warning(f"Cox analysis failed: {e}")
            return {
                'hazard_ratios': {},
                'confidence_intervals': {},
                'summary': {},
                'log_likelihood': None,
                'error': str(e)
            }
    
    def _generate_summary(self, survival_metrics: Dict, 
                         stage_analysis: Dict,
                         improvement: Dict) -> Dict:
        """Generate survival analysis summary"""
        
        summary = {
            'overall_5year_survival': {
                'early': survival_metrics['average']['early_stage_survival'],
                'late': survival_metrics['average']['late_stage_survival'],
                'improvement': improvement['average_improvement'],
                'relative_improvement': improvement['percentage_improvement']
            },
            'best_disease_for_early_detection': max(
                improvement['by_disease'].items(),
                key=lambda x: x[1]['relative_improvement']
            )[0] if improvement['by_disease'] else 'N/A',
            'statistical_significance': stage_analysis.get(
                'statistical_significance', {}
            ).get('significant', False),
            'survival_benefit': 'Substantial' if improvement['average_improvement'] > 25 else
                               'Moderate' if improvement['average_improvement'] > 15 else 'Limited'
        }
        
        return summary
