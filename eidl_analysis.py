#!/usr/bin/env python3
"""
EIDL Loans Analysis Script
Analyzes the DATAACT_EIDL_LOANS_20200401-20200609.csv dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")

def load_and_explore_data(filename):
    """Load the CSV file and perform initial exploration"""
    print("Loading EIDL loans dataset...")
    
    # Load data with appropriate data types, handling parsing errors
    try:
        df = pd.read_csv(filename, low_memory=False)
    except pd.errors.ParserError:
        print("Parser error encountered. Trying with error handling...")
        df = pd.read_csv(filename, low_memory=False, on_bad_lines='skip')
        print("Loaded with some lines skipped due to parsing errors.")
    
    print(f"Dataset shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print("\nColumn names and types:")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype}")
    
    print("\nFirst few rows:")
    print(df.head())
    
    print("\nBasic statistics:")
    print(df.describe(include='all'))
    
    print("\nMissing values:")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    
    return df

def clean_data(df):
    """Clean and prepare data for analysis"""
    print("\nCleaning data...")
    
    # Convert date columns
    date_columns = ['ACTIONDATE', 'PERIODOFPERFORMANCESTARTDATE', 'PERIODOFPERFORMANCECURRENTENDDATE']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Convert numeric columns
    numeric_columns = ['FEDERALACTIONOBLIGATION', 'NONFEDERALFUNDINGAMOUNT', 
                      'FACEVALUEOFDIRECTLOANORLOANGUARANTEE', 'ORIGINALLOANSUBSIDYCOST']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Clean state codes
    if 'LEGALENTITYSTATECD' in df.columns:
        df['LEGALENTITYSTATECD'] = df['LEGALENTITYSTATECD'].str.strip().str.upper()
    
    print("Data cleaning completed.")
    return df

def analyze_geography(df):
    """Analyze loan distribution by geography"""
    print("\n" + "="*50)
    print("GEOGRAPHIC ANALYSIS")
    print("="*50)
    
    # State analysis
    if 'LEGALENTITYSTATECD' in df.columns and 'FACEVALUEOFDIRECTLOANORLOANGUARANTEE' in df.columns:
        state_stats = df.groupby('LEGALENTITYSTATECD').agg({
            'FACEVALUEOFDIRECTLOANORLOANGUARANTEE': ['count', 'sum', 'mean', 'median'],
            'ORIGINALLOANSUBSIDYCOST': ['sum', 'mean']
        }).round(2)
        
        state_stats.columns = ['Loan_Count', 'Total_Loan_Amount', 'Mean_Loan_Amount', 
                              'Median_Loan_Amount', 'Total_Subsidy_Cost', 'Mean_Subsidy_Cost']
        
        print("\nTop 15 states by loan count:")
        print(state_stats.sort_values('Loan_Count', ascending=False).head(15))
        
        print("\nTop 15 states by total loan amount:")
        print(state_stats.sort_values('Total_Loan_Amount', ascending=False).head(15))
        
        # Create state visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Top states by count
        top_states_count = state_stats.sort_values('Loan_Count', ascending=False).head(15)
        axes[0,0].bar(range(len(top_states_count)), top_states_count['Loan_Count'])
        axes[0,0].set_title('Top 15 States by Loan Count')
        axes[0,0].set_xlabel('State')
        axes[0,0].set_ylabel('Number of Loans')
        axes[0,0].set_xticks(range(len(top_states_count)))
        axes[0,0].set_xticklabels(top_states_count.index, rotation=45)
        
        # Top states by amount
        top_states_amount = state_stats.sort_values('Total_Loan_Amount', ascending=False).head(15)
        axes[0,1].bar(range(len(top_states_amount)), top_states_amount['Total_Loan_Amount'] / 1e9)
        axes[0,1].set_title('Top 15 States by Total Loan Amount')
        axes[0,1].set_xlabel('State')
        axes[0,1].set_ylabel('Total Loan Amount (Billions $)')
        axes[0,1].set_xticks(range(len(top_states_amount)))
        axes[0,1].set_xticklabels(top_states_amount.index, rotation=45)
        
        # Average loan amount by state
        avg_loan_states = state_stats.sort_values('Mean_Loan_Amount', ascending=False).head(15)
        axes[1,0].bar(range(len(avg_loan_states)), avg_loan_states['Mean_Loan_Amount'] / 1000)
        axes[1,0].set_title('Top 15 States by Average Loan Amount')
        axes[1,0].set_xlabel('State')
        axes[1,0].set_ylabel('Average Loan Amount (Thousands $)')
        axes[1,0].set_xticks(range(len(avg_loan_states)))
        axes[1,0].set_xticklabels(avg_loan_states.index, rotation=45)
        
        # Subsidy cost analysis
        subsidy_states = state_stats.sort_values('Total_Subsidy_Cost', ascending=False).head(15)
        axes[1,1].bar(range(len(subsidy_states)), subsidy_states['Total_Subsidy_Cost'] / 1e6)
        axes[1,1].set_title('Top 15 States by Total Subsidy Cost')
        axes[1,1].set_xlabel('State')
        axes[1,1].set_ylabel('Total Subsidy Cost (Millions $)')
        axes[1,1].set_xticks(range(len(subsidy_states)))
        axes[1,1].set_xticklabels(subsidy_states.index, rotation=45)
        
        plt.tight_layout()
        plt.savefig('geographic_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return state_stats

def analyze_temporal_patterns(df):
    """Analyze loan patterns over time"""
    print("\n" + "="*50)
    print("TEMPORAL ANALYSIS")
    print("="*50)
    
    if 'ACTIONDATE' in df.columns:
        # Daily loan statistics
        daily_stats = df.groupby(df['ACTIONDATE'].dt.date).agg({
            'FACEVALUEOFDIRECTLOANORLOANGUARANTEE': ['count', 'sum', 'mean'],
            'ORIGINALLOANSUBSIDYCOST': ['sum', 'mean']
        }).round(2)
        
        daily_stats.columns = ['Daily_Loan_Count', 'Daily_Total_Amount', 'Daily_Mean_Amount',
                              'Daily_Total_Subsidy', 'Daily_Mean_Subsidy']
        
        print("\nDaily loan statistics (first 10 days):")
        print(daily_stats.head(10))
        
        print("\nDaily loan statistics (last 10 days):")
        print(daily_stats.tail(10))
        
        # Create temporal visualizations
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Daily loan count
        axes[0,0].plot(daily_stats.index, daily_stats['Daily_Loan_Count'])
        axes[0,0].set_title('Daily Loan Count Over Time')
        axes[0,0].set_xlabel('Date')
        axes[0,0].set_ylabel('Number of Loans')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Daily total amount
        axes[0,1].plot(daily_stats.index, daily_stats['Daily_Total_Amount'] / 1e6)
        axes[0,1].set_title('Daily Total Loan Amount Over Time')
        axes[0,1].set_xlabel('Date')
        axes[0,1].set_ylabel('Total Amount (Millions $)')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Daily average amount
        axes[1,0].plot(daily_stats.index, daily_stats['Daily_Mean_Amount'] / 1000)
        axes[1,0].set_title('Daily Average Loan Amount Over Time')
        axes[1,0].set_xlabel('Date')
        axes[1,0].set_ylabel('Average Amount (Thousands $)')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Cumulative loans
        cumulative_loans = daily_stats['Daily_Loan_Count'].cumsum()
        axes[1,1].plot(daily_stats.index, cumulative_loans)
        axes[1,1].set_title('Cumulative Loan Count Over Time')
        axes[1,1].set_xlabel('Date')
        axes[1,1].set_ylabel('Cumulative Number of Loans')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('temporal_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return daily_stats

def analyze_loan_amounts(df):
    """Analyze loan amounts and distributions"""
    print("\n" + "="*50)
    print("LOAN AMOUNT ANALYSIS")
    print("="*50)
    
    if 'FACEVALUEOFDIRECTLOANORLOANGUARANTEE' in df.columns:
        loan_amounts = df['FACEVALUEOFDIRECTLOANORLOANGUARANTEE'].dropna()
        
        print(f"\nLoan amount statistics:")
        print(f"Total loans: {len(loan_amounts):,}")
        print(f"Total amount: ${loan_amounts.sum():,.2f}")
        print(f"Average loan: ${loan_amounts.mean():,.2f}")
        print(f"Median loan: ${loan_amounts.median():,.2f}")
        print(f"Min loan: ${loan_amounts.min():,.2f}")
        print(f"Max loan: ${loan_amounts.max():,.2f}")
        print(f"Standard deviation: ${loan_amounts.std():,.2f}")
        
        # Percentiles
        percentiles = [10, 25, 50, 75, 90, 95, 99]
        print(f"\nLoan amount percentiles:")
        for p in percentiles:
            value = np.percentile(loan_amounts, p)
            print(f"{p}th percentile: ${value:,.2f}")
        
        # Create loan amount visualizations
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Histogram of loan amounts
        axes[0,0].hist(loan_amounts / 1000, bins=50, alpha=0.7, edgecolor='black')
        axes[0,0].set_title('Distribution of Loan Amounts')
        axes[0,0].set_xlabel('Loan Amount (Thousands $)')
        axes[0,0].set_ylabel('Frequency')
        
        # Log scale histogram
        axes[0,1].hist(np.log10(loan_amounts + 1), bins=50, alpha=0.7, edgecolor='black')
        axes[0,1].set_title('Distribution of Loan Amounts (Log Scale)')
        axes[0,1].set_xlabel('Log10(Loan Amount + 1)')
        axes[0,1].set_ylabel('Frequency')
        
        # Box plot
        axes[1,0].boxplot(loan_amounts / 1000)
        axes[1,0].set_title('Box Plot of Loan Amounts')
        axes[1,0].set_ylabel('Loan Amount (Thousands $)')
        
        # Cumulative distribution
        sorted_amounts = np.sort(loan_amounts)
        cumulative_pct = np.arange(1, len(sorted_amounts) + 1) / len(sorted_amounts) * 100
        axes[1,1].plot(sorted_amounts / 1000, cumulative_pct)
        axes[1,1].set_title('Cumulative Distribution of Loan Amounts')
        axes[1,1].set_xlabel('Loan Amount (Thousands $)')
        axes[1,1].set_ylabel('Cumulative Percentage')
        
        plt.tight_layout()
        plt.savefig('loan_amount_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return loan_amounts

def analyze_business_types(df):
    """Analyze business types and characteristics"""
    print("\n" + "="*50)
    print("BUSINESS TYPE ANALYSIS")
    print("="*50)
    
    if 'BUSINESSTYPES' in df.columns:
        business_stats = df.groupby('BUSINESSTYPES').agg({
            'FACEVALUEOFDIRECTLOANORLOANGUARANTEE': ['count', 'sum', 'mean'],
            'ORIGINALLOANSUBSIDYCOST': ['sum', 'mean']
        }).round(2)
        
        business_stats.columns = ['Count', 'Total_Amount', 'Mean_Amount', 'Total_Subsidy', 'Mean_Subsidy']
        business_stats = business_stats.sort_values('Count', ascending=False)
        
        print("\nBusiness types analysis:")
        print(business_stats)
        
        # Create business type visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Count by business type
        top_business_types = business_stats.head(10)
        axes[0,0].bar(range(len(top_business_types)), top_business_types['Count'])
        axes[0,0].set_title('Top 10 Business Types by Count')
        axes[0,0].set_xlabel('Business Type')
        axes[0,0].set_ylabel('Number of Loans')
        axes[0,0].set_xticks(range(len(top_business_types)))
        axes[0,0].set_xticklabels(top_business_types.index, rotation=45)
        
        # Total amount by business type
        axes[0,1].bar(range(len(top_business_types)), top_business_types['Total_Amount'] / 1e9)
        axes[0,1].set_title('Top 10 Business Types by Total Amount')
        axes[0,1].set_xlabel('Business Type')
        axes[0,1].set_ylabel('Total Amount (Billions $)')
        axes[0,1].set_xticks(range(len(top_business_types)))
        axes[0,1].set_xticklabels(top_business_types.index, rotation=45)
        
        # Average amount by business type
        axes[1,0].bar(range(len(top_business_types)), top_business_types['Mean_Amount'] / 1000)
        axes[1,0].set_title('Top 10 Business Types by Average Amount')
        axes[1,0].set_xlabel('Business Type')
        axes[1,0].set_ylabel('Average Amount (Thousands $)')
        axes[1,0].set_xticks(range(len(top_business_types)))
        axes[1,0].set_xticklabels(top_business_types.index, rotation=45)
        
        # Pie chart of business type distribution
        axes[1,1].pie(top_business_types['Count'], labels=top_business_types.index, autopct='%1.1f%%')
        axes[1,1].set_title('Distribution of Loans by Business Type')
        
        plt.tight_layout()
        plt.savefig('business_type_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return business_stats

def generate_summary_report(df, state_stats, daily_stats, loan_amounts, business_stats):
    """Generate a comprehensive summary report"""
    print("\n" + "="*70)
    print("EIDL LOANS COMPREHENSIVE ANALYSIS REPORT")
    print("="*70)
    
    report = []
    report.append("EXECUTIVE SUMMARY")
    report.append("="*50)
    
    # Overall statistics
    total_loans = len(df)
    total_amount = df['FACEVALUEOFDIRECTLOANORLOANGUARANTEE'].sum()
    total_subsidy = df['ORIGINALLOANSUBSIDYCOST'].sum()
    avg_loan = df['FACEVALUEOFDIRECTLOANORLOANGUARANTEE'].mean()
    
    report.append(f"Dataset Period: April 1, 2020 - June 9, 2020")
    report.append(f"Total Number of Loans: {total_loans:,}")
    report.append(f"Total Loan Amount: ${total_amount:,.2f}")
    report.append(f"Total Subsidy Cost: ${total_subsidy:,.2f}")
    report.append(f"Average Loan Amount: ${avg_loan:,.2f}")
    report.append("")
    
    # Geographic insights
    report.append("GEOGRAPHIC INSIGHTS")
    report.append("-" * 30)
    top_state = state_stats.sort_values('Loan_Count', ascending=False).index[0]
    top_state_count = state_stats.loc[top_state, 'Loan_Count']
    top_amount_state = state_stats.sort_values('Total_Loan_Amount', ascending=False).index[0]
    top_amount_value = state_stats.loc[top_amount_state, 'Total_Loan_Amount']
    
    report.append(f"State with most loans: {top_state} ({top_state_count:,} loans)")
    report.append(f"State with highest total amount: {top_amount_state} (${top_amount_value:,.2f})")
    report.append(f"Number of states represented: {len(state_stats)}")
    report.append("")
    
    # Temporal insights
    report.append("TEMPORAL INSIGHTS")
    report.append("-" * 30)
    peak_day = daily_stats.sort_values('Daily_Loan_Count', ascending=False).index[0]
    peak_count = daily_stats.loc[peak_day, 'Daily_Loan_Count']
    
    report.append(f"Peak loan day: {peak_day} ({peak_count:,} loans)")
    report.append(f"Average daily loans: {daily_stats['Daily_Loan_Count'].mean():.0f}")
    report.append(f"Analysis period: {len(daily_stats)} days")
    report.append("")
    
    # Loan amount insights
    report.append("LOAN AMOUNT INSIGHTS")
    report.append("-" * 30)
    report.append(f"Median loan amount: ${np.median(loan_amounts):,.2f}")
    report.append(f"Loans under $50K: {(loan_amounts < 50000).sum():,} ({(loan_amounts < 50000).mean()*100:.1f}%)")
    report.append(f"Loans over $100K: {(loan_amounts > 100000).sum():,} ({(loan_amounts > 100000).mean()*100:.1f}%)")
    report.append(f"Loans over $1M: {(loan_amounts > 1000000).sum():,} ({(loan_amounts > 1000000).mean()*100:.1f}%)")
    report.append("")
    
    # Business type insights
    if business_stats is not None:
        report.append("BUSINESS TYPE INSIGHTS")
        report.append("-" * 30)
        top_business = business_stats.index[0]
        top_business_count = business_stats.loc[top_business, 'Count']
        
        report.append(f"Most common business type: {top_business} ({top_business_count:,} loans)")
        report.append(f"Number of business types: {len(business_stats)}")
        report.append("")
    
    # Key findings
    report.append("KEY FINDINGS")
    report.append("-" * 30)
    report.append("1. This dataset represents EIDL loans during the early COVID-19 pandemic period")
    report.append("2. The program provided significant economic relief to businesses across all states")
    report.append("3. Loan amounts varied widely, indicating diverse business needs and sizes")
    report.append("4. Geographic distribution shows concentration in states with larger economies")
    report.append("5. Temporal patterns may reflect program rollout and business application timing")
    
    # Print and save report
    full_report = "\n".join(report)
    print(full_report)
    
    with open('eidl_analysis_report.txt', 'w') as f:
        f.write(full_report)
    
    return full_report

def main():
    """Main analysis function"""
    filename = 'DATAACT_EIDL_LOANS_20200401-20200609.csv'
    
    # Load and explore data
    df = load_and_explore_data(filename)
    
    # Clean data
    df = clean_data(df)
    
    # Perform analyses
    state_stats = analyze_geography(df)
    daily_stats = analyze_temporal_patterns(df)
    loan_amounts = analyze_loan_amounts(df)
    business_stats = analyze_business_types(df)
    
    # Generate summary report
    generate_summary_report(df, state_stats, daily_stats, loan_amounts, business_stats)
    
    print("\nAnalysis complete! Generated files:")
    print("- geographic_analysis.png")
    print("- temporal_analysis.png") 
    print("- loan_amount_analysis.png")
    print("- business_type_analysis.png")
    print("- eidl_analysis_report.txt")

if __name__ == "__main__":
    main()