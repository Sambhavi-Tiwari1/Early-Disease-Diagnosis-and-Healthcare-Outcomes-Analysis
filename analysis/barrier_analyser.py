"""
Barrier Analysis for Early Disease Diagnosis
"""
import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Tuple
from collections import Counter

logger = logging.getLogger(__name__)

class BarrierAnalyzer:
    """
    Analyze barriers to early disease diagnosis
    """
    
    def __init__(self):
        self.barrier_categories = {
            'Patient-Related': {
                'lack_of_awareness': {'impact': 0.85, 'prevalence': 0.65},
                'fear_anxiety': {'impact': 0.65, 'prevalence': 0.55},
                'denial': {'impact': 0.55, 'prevalence': 0.40},
                'lack_of_symptoms': {'impact': 0.60, 'prevalence': 0.40}
            },
            'Healthcare System': {
                'cost_of_screening': {'impact': 0.75, 'prevalence': 0.45},
                'access_to_healthcare': {'impact': 0.70, 'prevalence': 0.35},
                'provider_shortage': {'impact': 0.45, 'prevalence': 0.25},
                'long_wait_times': {'impact': 0.55, 'prevalence': 0.30}
            },
            'Socioeconomic': {
                'income_level': {'impact': 0.65, 'prevalence': 0.40},
                'education_level': {'impact': 0.70, 'prevalence': 0.45},
                'geographic_location': {'impact': 0.50, 'prevalence': 0.30},
                'insurance_coverage': {'impact': 0.60, 'prevalence': 0.35}
            },
            'Cultural': {
                'cultural_beliefs': {'impact': 0.50, 'prevalence': 0.30},
                'religious_factors': {'impact': 0.40, 'prevalence': 0.20},
                'language_barriers': {'impact': 0.45, 'prevalence': 0.25}
            }
        }
    
    def analyze(self) -> Dict:
        """Complete barrier analysis"""
        
        # Calculate barrier scores
        barrier_scores = self._calculate_barrier_scores()
        
        # Identify key barriers
        key_barriers = self._identify_key_barriers(barrier_scores)
        
        # Segment analysis
        segment_analysis = self._analyze_barrier_segments(barrier_scores)
        
        # Recommendations
        recommendations = self._generate_recommendations(barrier_scores)
        
        return {
            'barrier_scores': barrier_scores,
            'key_barriers': key_barriers,
            'segment_analysis': segment_analysis,
            'recommendations': recommendations,
            'summary': self._generate_summary(barrier_scores, key_barriers)
        }
    
    def _calculate_barrier_scores(self) -> Dict:
        """Calculate barrier impact scores"""
        scores = {}
        
        for category, barriers in self.barrier_categories.items():
            category_scores = {}
            total_impact = 0
            total_prevalence = 0
            
            for barrier_name, metrics in barriers.items():
                impact_score = metrics['impact'] * 100
                prevalence_score = metrics['prevalence'] * 100
                combined_score = (impact_score * 0.6 + prevalence_score * 0.4)
                
                category_scores[barrier_name] = {
                    'impact_score': round(impact_score, 1),
                    'prevalence_score': round(prevalence_score, 1),
                    'combined_score': round(combined_score, 1),
                    'priority': self._get_priority(combined_score)
                }
                
                total_impact += impact_score
                total_prevalence += prevalence_score
            
            scores[category] = {
                'barriers': category_scores,
                'avg_impact': round(total_impact / len(barriers), 1),
                'avg_prevalence': round(total_prevalence / len(barriers), 1),
                'category_priority': self._get_priority(
                    (total_impact / len(barriers) * 0.6 + 
                     total_prevalence / len(barriers) * 0.4)
                )
            }
        
        return scores
    
    def _get_priority(self, score: float) -> str:
        """Get priority level based on score"""
        if score > 70:
            return "Very High"
        elif score > 55:
            return "High"
        elif score > 40:
            return "Medium"
        else:
            return "Low"
    
    def _identify_key_barriers(self, barrier_scores: Dict) -> List:
        """Identify top barriers"""
        all_barriers = []
        
        for category, data in barrier_scores.items():
            for barrier_name, scores in data['barriers'].items():
                all_barriers.append({
                    'category': category,
                    'barrier': barrier_name,
                    'combined_score': scores['combined_score'],
                    'impact_score': scores['impact_score'],
                    'prevalence_score': scores['prevalence_score'],
                    'priority': scores['priority']
                })
        
        # Sort by combined score
        all_barriers.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return all_barriers[:10]  # Top 10 barriers
    
    def _analyze_barrier_segments(self, barrier_scores: Dict) -> Dict:
        """Analyze barriers by segment"""
        
        segments = {
            'High_Impact_High_Prevalence': [],
            'High_Impact_Low_Prevalence': [],
            'Low_Impact_High_Prevalence': [],
            'Low_Impact_Low_Prevalence': []
        }
        
        for category, data in barrier_scores.items():
            for barrier_name, scores in data['barriers'].items():
                impact = scores['impact_score']
                prevalence = scores['prevalence_score']
                
                if impact > 50 and prevalence > 50:
                    segments['High_Impact_High_Prevalence'].append({
                        'category': category,
                        'barrier': barrier_name,
                        'impact': impact,
                        'prevalence': prevalence
                    })
                elif impact > 50 and prevalence <= 50:
                    segments['High_Impact_Low_Prevalence'].append({
                        'category': category,
                        'barrier': barrier_name,
                        'impact': impact,
                        'prevalence': prevalence
                    })
                elif impact <= 50 and prevalence > 50:
                    segments['Low_Impact_High_Prevalence'].append({
                        'category': category,
                        'barrier': barrier_name,
                        'impact': impact,
                        'prevalence': prevalence
                    })
                else:
                    segments['Low_Impact_Low_Prevalence'].append({
                        'category': category,
                        'barrier': barrier_name,
                        'impact': impact,
                        'prevalence': prevalence
                    })
        
        return segments
    
    def _generate_recommendations(self, barrier_scores: Dict) -> Dict:
        """Generate recommendations to address barriers"""
        
        recommendations = {
            'awareness_campaigns': {
                'priority': 'Very High',
                'target_barriers': ['lack_of_awareness', 'fear_anxiety', 'denial'],
                'recommendations': [
                    'Launch mass media campaigns on importance of early diagnosis',
                    'Develop targeted education programs for high-risk populations',
                    'Share patient success stories to reduce fear and stigma',
                    'Partner with community organizations for outreach'
                ]
            },
            'access_improvement': {
                'priority': 'High',
                'target_barriers': ['access_to_healthcare', 'cost_of_screening', 'long_wait_times'],
                'recommendations': [
                    'Expand mobile screening units to underserved areas',
                    'Subsidize screening costs for low-income populations',
                    'Reduce wait times through streamlined processes',
                    'Implement telemedicine for initial consultations'
                ]
            },
            'healthcare_system': {
                'priority': 'High',
                'target_barriers': ['provider_shortage', 'insurance_coverage', 'education_level'],
                'recommendations': [
                    'Train more healthcare providers in underserved areas',
                    'Advocate for expanded insurance coverage of screenings',
                    'Develop patient education materials at various literacy levels',
                    'Implement reminder systems for routine screenings'
                ]
            },
            'cultural_sensitivity': {
                'priority': 'Medium',
                'target_barriers': ['cultural_beliefs', 'religious_factors', 'language_barriers'],
                'recommendations': [
                    'Develop culturally appropriate educational materials',
                    'Engage community leaders as health advocates',
                    'Provide interpretation services at healthcare facilities',
                    'Respect cultural beliefs while providing medical guidance'
                ]
            }
        }
        
        return recommendations
    
    def _generate_summary(self, barrier_scores: Dict, key_barriers: List) -> Dict:
        """Generate barrier analysis summary"""
        
        # Calculate average scores
        all_impacts = []
        all_prevalences = []
        
        for category, data in barrier_scores.items():
            for barrier_name, scores in data['barriers'].items():
                all_impacts.append(scores['impact_score'])
                all_prevalences.append(scores['prevalence_score'])
        
        summary = {
            'avg_impact': round(np.mean(all_impacts), 1),
            'avg_prevalence': round(np.mean(all_prevalences), 1),
            'top_barrier': key_barriers[0]['barrier'] if key_barriers else 'N/A',
            'top_category': key_barriers[0]['category'] if key_barriers else 'N/A',
            'critical_barriers_count': len([b for b in key_barriers if b['priority'] == 'Very High']),
            'recommendation_priority': 'Immediate Action Required' if any(
                b['priority'] == 'Very High' for b in key_barriers
            ) else 'Action Recommended'
        }
        
        return summary
