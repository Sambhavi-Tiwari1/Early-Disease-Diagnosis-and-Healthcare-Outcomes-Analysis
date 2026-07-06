#!/usr/bin/env python
"""
Main execution script for Early Disease Diagnosis Analysis
"""
import os
import sys
import argparse
import yaml
import logging
import json
from datetime import datetime
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.disease_data_generator import DiseaseDataGenerator
from data.patient_data_generator import PatientDataGenerator
from data.screening_data_generator import ScreeningDataGenerator
from analysis.survival_analyzer import SurvivalAnalyzer
from analysis.cost_benefit_analyzer import CostBenefitAnalyzer
from analysis.outcome_analyzer import OutcomeAnalyzer
from analysis.barrier_analyzer import BarrierAnalyzer
from analysis.screening_evaluator import ScreeningEvaluator
from visualization.visualizer import Visualizer

logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path='config.yaml'):
    """Load configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def create_directories():
    """Create necessary directories"""
    dirs = ['output/reports', 'output/figures', 'data/raw', 'data/processed']
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def generate_all_data():
    """Generate all synthetic data"""
    logger.info("Generating disease data...")
    disease_gen = DiseaseDataGenerator()
    disease_data = disease_gen.generate_disease_incidence()
    survival_data = disease_gen.generate_survival_data()
    progression_data = disease_gen.generate_disease_progression_data()
    
    disease_data.to_csv('data/raw/disease_incidence.csv', index=False)
    survival_data.to_csv('data/raw/survival_data.csv', index=False)
    progression_data.to_csv('data/raw/progression_data.csv', index=False)
    
    logger.info("Generating patient data...")
    patient_gen = PatientDataGenerator()
    patient_data = patient_gen.generate_patient_outcomes(1000)
    qol_data = patient_gen.generate_quality_of_life_data()
    
    patient_data.to_csv('data/raw/patient_outcomes.csv', index=False)
    qol_data.to_csv('data/raw/qol_data.csv', index=False)
    
    logger.info("Generating screening data...")
    screen_gen = ScreeningDataGenerator()
    screening_data = screen_gen.generate_screening_data()
    
    screening_data.to_csv('data/raw/screening_data.csv', index=False)
    
    return disease_data, survival_data, patient_data, qol_data, screening_data

def run_full_analysis():
    """Run complete analysis pipeline"""
    logger.info("="*60)
    logger.info("EARLY DISEASE DIAGNOSIS & HEALTHCARE OUTCOMES ANALYSIS")
    logger.info("="*60)
    
    # Generate data
    disease_data, survival_data, patient_data, qol_data, screening_data = generate_all_data()
    
    # Survival Analysis
    logger.info("\n📊 Running Survival Analysis...")
    survival_analyzer = SurvivalAnalyzer()
    survival_results = survival_analyzer.analyze(patient_data, survival_data)
    
    # Cost-Benefit Analysis
    logger.info("\n💰 Running Cost-Benefit Analysis...")
    cost_analyzer = CostBenefitAnalyzer()
    cost_results = cost_analyzer.analyze(patient_data)
    
    # Outcome Analysis
    logger.info("\n📈 Running Outcome Analysis...")
    outcome_analyzer = OutcomeAnalyzer()
    outcome_results = outcome_analyzer.analyze(patient_data, qol_data)
    
    # Barrier Analysis
    logger.info("\n🚧 Running Barrier Analysis...")
    barrier_analyzer = BarrierAnalyzer()
    barrier_results = barrier_analyzer.analyze()
    
    # Screening Evaluation
    logger.info("\n🔬 Running Screening Evaluation...")
    screen_evaluator = ScreeningEvaluator()
    screening_results = screen_evaluator.analyze(screening_data)
    
    # Generate Visualizations
    logger.info("\n🎨 Generating Visualizations...")
    visualizer = Visualizer()
    visualizer.create_all_visualizations(
        survival_data, patient_data, qol_data, 
        cost_results, barrier_results
    )
    
    # Generate Report
    logger.info("\n📄 Generating Report...")
    generate_report(
        survival_results, cost_results, outcome_results,
        barrier_results, screening_results
    )
    
    logger.info("\n✅ Analysis Complete!")
    return {
        'survival': survival_results,
        'cost': cost_results,
        'outcome': outcome_results,
        'barrier': barrier_results,
        'screening': screening_results
    }

def generate_report(survival_results, cost_results, outcome_results,
                   barrier_results, screening_results):
    """Generate comprehensive report"""
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'survival_analysis': survival_results,
        'cost_benefit_analysis': cost_results,
        'outcome_analysis': outcome_results,
        'barrier_analysis': barrier_results,
        'screening_evaluation': screening_results,
        'strategic_recommendations': generate_strategic_recommendations(
            survival_results, cost_results, barrier_results
        )
    }
    
    with open('output/reports/full_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info("Report generated successfully")

def generate_strategic_recommendations(survival_results, cost_results, barrier_results):
    """Generate strategic recommendations"""
    
    recommendations = {
        'awareness_campaigns': [
            'Launch public awareness campaigns on early diagnosis benefits',
            'Target high-risk populations with tailored messaging',
            'Use social media and digital platforms for education',
            'Partner with community organizations and influencers'
        ],
        'screening_optimization': [
            'Implement risk-based screening guidelines',
            'Expand mobile screening units for rural areas',
            'Reduce screening costs through government subsidies',
            'Integrate screening into routine healthcare visits'
        ],
        'access_improvement': [
            'Increase healthcare providers in underserved areas',
            'Implement telemedicine for remote consultations',
            'Provide transportation support for patients',
            'Reduce wait times for diagnostic services'
        ],
        'policy_recommendations': [
            'Mandate insurance coverage for preventive screenings',
            'Provide tax incentives for screening participation',
            'Fund research on early diagnostic tools',
            'Develop national screening guidelines'
        ],
        'technology_adoption': [
            'Implement AI-powered risk assessment tools',
            'Develop mobile apps for symptom checking',
            'Use data analytics for population health management',
            'Integrate electronic health records for tracking'
        ]
    }
    
    return recommendations

def main():
    parser = argparse.ArgumentParser(description='Early Disease Diagnosis Analysis')
    parser.add_argument('--full', action='store_true', help='Run full analysis')
    parser.add_argument('--survival', action='store_true', help='Run survival analysis only')
    parser.add_argument('--cost', action='store_true', help='Run cost-benefit analysis only')
    parser.add_argument('--barriers', action='store_true', help='Run barrier analysis only')
    parser.add_argument('--report', action='store_true', help='Generate report only')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    create_directories()
    
    if args.interactive:
        interactive_mode()
    elif args.full:
        run_full_analysis()
    elif args.survival:
        run_survival_only()
    elif args.cost:
        run_cost_only()
    elif args.barriers:
        run_barriers_only()
    elif args.report:
        generate_report_only()
    else:
        print("Use --help for usage information")

def interactive_mode():
    """Interactive CLI mode"""
    print("\n" + "="*60)
    print("🏥 EARLY DISEASE DIAGNOSIS ANALYZER")
    print("="*60 + "\n")
    
    print("1. Run Full Analysis")
    print("2. Run Survival Analysis Only")
    print("3. Run Cost-Benefit Analysis Only")
    print("4. Run Barrier Analysis Only")
    print("5. View Results")
    print("6. Exit")
    
    choice = input("\nSelect option (1-6): ")
    
    if choice == '1':
        run_full_analysis()
    elif choice == '2':
        run_survival_only()
    elif choice == '3':
        run_cost_only()
    elif choice == '4':
        run_barriers_only()
    elif choice == '5':
        view_results()
    else:
        print("Exiting...")

def view_results():
    """View analysis results"""
    try:
        with open('output/reports/full_report.json', 'r') as f:
            report = json.load(f)
        
        print("\n" + "="*60)
        print("📊 ANALYSIS RESULTS")
        print("="*60)
        
        survival = report['survival_analysis']
        print(f"\n📈 Survival Analysis:")
        print(f"  • Early Stage 5-Year Survival: {survival['survival_metrics']['average']['early_stage_survival']:.1f}%")
        print(f"  • Late Stage 5-Year Survival: {survival['survival_metrics']['average']['late_stage_survival']:.1f}%")
        print(f"  • Improvement: {survival['improvement']['average_improvement']:.1f}%")
        
        cost = report['cost_benefit_analysis']
        print(f"\n💰 Cost-Benefit Analysis:")
        print(f"  • Savings per Patient: ${cost['cost_analysis']['savings']['per_patient']:,.0f}")
        print(f"  • ROI: {cost['roi_analysis']['roi_percentage']:.1f}%")
        
        barrier = report['barrier_analysis']
        print(f"\n🚧 Key Barriers:")
        top_barriers = barrier['key_barriers'][:3]
        for b in top_barriers:
            print(f"  • {b['barrier']} ({b['category']}) - Priority: {b['priority']}")
        
    except FileNotFoundError:
        print("No results found. Please run the analysis first.")

def run_survival_only():
    disease_data, survival_data, patient_data, _, _ = generate_all_data()
    analyzer = SurvivalAnalyzer()
    results = analyzer.analyze(patient_data, survival_data)
    print("\nSurvival Analysis Results:")
    print(f"Early Stage Survival: {results['survival_metrics']['average']['early_stage_survival']:.1f}%")
    print(f"Late Stage Survival: {results['survival_metrics']['average']['late_stage_survival']:.1f}%")
    print(f"Improvement: {results['improvement']['average_improvement']:.1f}%")

def run_cost_only():
    _, _, patient_data, _, _ = generate_all_data()
    analyzer = CostBenefitAnalyzer()
    results = analyzer.analyze(patient_data)
    print("\nCost-Benefit Analysis Results:")
    print(f"Savings per Patient: ${results['cost_analysis']['savings']['per_patient']:,.0f}")
    print(f"ROI: {results['roi_analysis']['roi_percentage']:.1f}%")

def run_barriers_only():
    analyzer = BarrierAnalyzer()
    results = analyzer.analyze()
    print("\nBarrier Analysis Results:")
    print(f"Top Barrier: {results['key_barriers'][0]['barrier']}")
    print(f"Critical Barriers: {results['summary']['critical_barriers_count']}")

if __name__ == "__main__":
    main()
