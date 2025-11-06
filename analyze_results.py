"""
Experiment Results Analysis Script
Analyzes booking system experiment data comparing 'text' vs 'coloured' interfaces
Generates statistics and visualizations considering order effects
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from datetime import datetime

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def load_data(filepath='experiment-results.json'):
    """Load experiment results from JSON file"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def process_data(raw_data):
    """
    Convert raw JSON data into structured DataFrame
    Separates trials and tracks order effects
    """
    records = []
    
    for experiment in raw_data:
        timestamp = experiment['timestamp']
        first_system = experiment['firstSystem']
        
        # Process both trials
        for trial_num in [1, 2]:
            trial_key = f'trial{trial_num}'
            trial = experiment[trial_key]
            
            records.append({
                'timestamp': timestamp,
                'trial_number': trial_num,
                'system': trial['system'],
                'duration_ms': trial['duration'],
                'duration_s': trial['duration'] / 1000,
                'first_system': first_system,
                'is_first_trial': trial_num == 1,
                'order_position': 'first' if trial_num == 1 else 'second'
            })
    
    return pd.DataFrame(records)

def calculate_statistics(df):
    """Calculate comprehensive statistics"""
    stats = {}
    
    # Overall statistics by system
    stats['overall'] = df.groupby('system')['duration_ms'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max')
    ]).round(2)
    
    # Statistics by order position
    stats['by_position'] = df.groupby(['order_position', 'system'])['duration_ms'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std')
    ]).round(2)
    
    # When each system appears first
    stats['when_first'] = df[df['is_first_trial']].groupby('system')['duration_ms'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std')
    ]).round(2)
    
    # When each system appears second (potential learning effect)
    stats['when_second'] = df[~df['is_first_trial']].groupby('system')['duration_ms'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std')
    ]).round(2)
    
    # Order effect: same system performance when first vs second
    stats['order_effect'] = {}
    for system in ['text', 'coloured']:
        first_mean = df[(df['system'] == system) & (df['is_first_trial'])]['duration_ms'].mean()
        second_mean = df[(df['system'] == system) & (~df['is_first_trial'])]['duration_ms'].mean()
        stats['order_effect'][system] = {
            'first_mean': round(first_mean, 2),
            'second_mean': round(second_mean, 2),
            'difference': round(second_mean - first_mean, 2),
            'percent_change': round((second_mean - first_mean) / first_mean * 100, 2)
        }
    
    # Performance comparison when coloured is first
    coloured_first = df[df['first_system'] == 'coloured']
    stats['coloured_first'] = coloured_first.groupby('system')['duration_ms'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median')
    ]).round(2)
    
    # Performance comparison when text is first
    text_first = df[df['first_system'] == 'text']
    stats['text_first'] = text_first.groupby('system')['duration_ms'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median')
    ]).round(2)
    
    return stats

def create_visualizations(df, output_dir='analysis_output'):
    """Create comprehensive visualizations"""
    Path(output_dir).mkdir(exist_ok=True)
    
    # 1. Overall comparison - Box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='system', y='duration_s', palette=['#FF6B6B', '#4ECDC4'])
    plt.title('Overall Task Duration: Text vs Coloured System', fontsize=16, fontweight='bold')
    plt.xlabel('System Type', fontsize=12)
    plt.ylabel('Duration (seconds)', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_overall_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Violin plot for distribution
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df, x='system', y='duration_s', palette=['#FF6B6B', '#4ECDC4'])
    plt.title('Distribution of Task Durations by System', fontsize=16, fontweight='bold')
    plt.xlabel('System Type', fontsize=12)
    plt.ylabel('Duration (seconds)', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_distribution_violin.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Order effect comparison
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='order_position', y='duration_s', hue='system', 
                palette=['#FF6B6B', '#4ECDC4'], ci=95)
    plt.title('Performance by Order Position (First vs Second Trial)', fontsize=16, fontweight='bold')
    plt.xlabel('Order Position', fontsize=12)
    plt.ylabel('Mean Duration (seconds)', fontsize=12)
    plt.legend(title='System')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_order_effect.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Performance when each system appears first
    plt.figure(figsize=(12, 6))
    first_trials = df[df['is_first_trial']]
    sns.barplot(data=first_trials, x='system', y='duration_s', palette=['#FF6B6B', '#4ECDC4'], ci=95)
    plt.title('Performance When System is Presented First', fontsize=16, fontweight='bold')
    plt.xlabel('System Type', fontsize=12)
    plt.ylabel('Mean Duration (seconds)', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/04_first_presentation.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Performance when each system appears second
    plt.figure(figsize=(12, 6))
    second_trials = df[~df['is_first_trial']]
    sns.barplot(data=second_trials, x='system', y='duration_s', palette=['#FF6B6B', '#4ECDC4'], ci=95)
    plt.title('Performance When System is Presented Second', fontsize=16, fontweight='bold')
    plt.xlabel('System Type', fontsize=12)
    plt.ylabel('Mean Duration (seconds)', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_second_presentation.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Comparison based on which system was first
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # When coloured is first
    coloured_first_df = df[df['first_system'] == 'coloured']
    sns.barplot(data=coloured_first_df, x='system', y='duration_s', ax=axes[0],
                palette=['#FF6B6B', '#4ECDC4'], ci=95)
    axes[0].set_title('Performance When Coloured System is First', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('System Type', fontsize=12)
    axes[0].set_ylabel('Mean Duration (seconds)', fontsize=12)
    
    # When text is first
    text_first_df = df[df['first_system'] == 'text']
    sns.barplot(data=text_first_df, x='system', y='duration_s', ax=axes[1],
                palette=['#FF6B6B', '#4ECDC4'], ci=95)
    axes[1].set_title('Performance When Text System is First', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('System Type', fontsize=12)
    axes[1].set_ylabel('Mean Duration (seconds)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/06_first_system_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 7. Learning effect within each system
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    for idx, system in enumerate(['text', 'coloured']):
        system_df = df[df['system'] == system]
        order_means = system_df.groupby('order_position')['duration_s'].mean()
        order_std = system_df.groupby('order_position')['duration_s'].std()
        
        colors = ['#FF6B6B' if system == 'text' else '#4ECDC4']
        axes[idx].bar(['First', 'Second'], order_means, yerr=order_std, 
                      color=colors, alpha=0.7, capsize=5)
        axes[idx].set_title(f'{system.capitalize()} System: First vs Second Trial', 
                           fontsize=14, fontweight='bold')
        axes[idx].set_ylabel('Mean Duration (seconds)', fontsize=12)
        axes[idx].set_xlabel('Trial Position', fontsize=12)
        
    plt.tight_layout()
    plt.savefig(f'{output_dir}/07_learning_effect.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 8. Time series of all experiments
    plt.figure(figsize=(14, 6))
    df_sorted = df.sort_values('timestamp')
    for system in ['text', 'coloured']:
        system_data = df_sorted[df_sorted['system'] == system]
        color = '#FF6B6B' if system == 'text' else '#4ECDC4'
        plt.scatter(range(len(system_data)), system_data['duration_s'], 
                   label=system.capitalize(), alpha=0.6, s=50, color=color)
    
    plt.title('Task Duration Over Time (All Experiments)', fontsize=16, fontweight='bold')
    plt.xlabel('Experiment Order', fontsize=12)
    plt.ylabel('Duration (seconds)', fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/08_time_series.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 9. Histogram comparison
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    for idx, system in enumerate(['text', 'coloured']):
        system_data = df[df['system'] == system]['duration_s']
        color = '#FF6B6B' if system == 'text' else '#4ECDC4'
        axes[idx].hist(system_data, bins=15, color=color, alpha=0.7, edgecolor='black')
        axes[idx].axvline(system_data.mean(), color='red', linestyle='--', 
                         linewidth=2, label=f'Mean: {system_data.mean():.2f}s')
        axes[idx].axvline(system_data.median(), color='green', linestyle='--', 
                         linewidth=2, label=f'Median: {system_data.median():.2f}s')
        axes[idx].set_title(f'{system.capitalize()} System Duration Distribution', 
                           fontsize=14, fontweight='bold')
        axes[idx].set_xlabel('Duration (seconds)', fontsize=12)
        axes[idx].set_ylabel('Frequency', fontsize=12)
        axes[idx].legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/09_histograms.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 10. Comprehensive comparison grid
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Overall
    sns.boxplot(data=df, x='system', y='duration_s', ax=axes[0, 0],
                palette=['#FF6B6B', '#4ECDC4'])
    axes[0, 0].set_title('Overall Performance', fontsize=12, fontweight='bold')
    
    # By order position
    sns.barplot(data=df, x='order_position', y='duration_s', hue='system', 
                ax=axes[0, 1], palette=['#FF6B6B', '#4ECDC4'], ci=95)
    axes[0, 1].set_title('By Order Position', fontsize=12, fontweight='bold')
    axes[0, 1].legend(title='System')
    
    # When coloured first
    sns.barplot(data=df[df['first_system'] == 'coloured'], x='system', y='duration_s',
                ax=axes[1, 0], palette=['#FF6B6B', '#4ECDC4'], ci=95)
    axes[1, 0].set_title('When Coloured Presented First', fontsize=12, fontweight='bold')
    
    # When text first
    sns.barplot(data=df[df['first_system'] == 'text'], x='system', y='duration_s',
                ax=axes[1, 1], palette=['#FF6B6B', '#4ECDC4'], ci=95)
    axes[1, 1].set_title('When Text Presented First', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/10_comprehensive_grid.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ All visualizations saved to '{output_dir}/' directory")

def generate_report(stats, df, output_dir='analysis_output'):
    """Generate comprehensive text report"""
    Path(output_dir).mkdir(exist_ok=True)
    
    report_file = f'{output_dir}/statistical_report.txt'
    
    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("EXPERIMENT RESULTS ANALYSIS REPORT\n")
        f.write("Comparison of Text vs Coloured Booking Systems\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Overall statistics
        f.write("1. OVERALL PERFORMANCE STATISTICS\n")
        f.write("-" * 80 + "\n")
        f.write(stats['overall'].to_string())
        f.write("\n\n")
        
        # Key findings
        text_mean = stats['overall'].loc['text', 'mean']
        coloured_mean = stats['overall'].loc['coloured', 'mean']
        diff = text_mean - coloured_mean
        percent_diff = (diff / text_mean) * 100
        
        f.write("KEY FINDING:\n")
        if diff > 0:
            f.write(f"The COLOURED system was faster by {abs(diff):.2f}ms ({abs(percent_diff):.1f}%)\n")
            f.write(f"  - Text mean: {text_mean:.2f}ms\n")
            f.write(f"  - Coloured mean: {coloured_mean:.2f}ms\n")
        else:
            f.write(f"The TEXT system was faster by {abs(diff):.2f}ms ({abs(percent_diff):.1f}%)\n")
            f.write(f"  - Text mean: {text_mean:.2f}ms\n")
            f.write(f"  - Coloured mean: {coloured_mean:.2f}ms\n")
        f.write("\n\n")
        
        # Performance by order position
        f.write("2. PERFORMANCE BY ORDER POSITION\n")
        f.write("-" * 80 + "\n")
        f.write(stats['by_position'].to_string())
        f.write("\n\n")
        
        # When each system appears first
        f.write("3. PERFORMANCE WHEN SYSTEM APPEARS FIRST\n")
        f.write("-" * 80 + "\n")
        f.write(stats['when_first'].to_string())
        f.write("\n\n")
        
        # When each system appears second
        f.write("4. PERFORMANCE WHEN SYSTEM APPEARS SECOND\n")
        f.write("-" * 80 + "\n")
        f.write(stats['when_second'].to_string())
        f.write("\n\n")
        
        # Order effects
        f.write("5. ORDER EFFECTS (Learning/Fatigue)\n")
        f.write("-" * 80 + "\n")
        for system, effects in stats['order_effect'].items():
            f.write(f"\n{system.upper()} System:\n")
            f.write(f"  First trial mean:  {effects['first_mean']:.2f}ms\n")
            f.write(f"  Second trial mean: {effects['second_mean']:.2f}ms\n")
            f.write(f"  Difference:        {effects['difference']:.2f}ms ({effects['percent_change']:+.1f}%)\n")
            if effects['difference'] < 0:
                f.write(f"  → Users were FASTER on second trial (learning effect)\n")
            else:
                f.write(f"  → Users were SLOWER on second trial (fatigue effect)\n")
        f.write("\n\n")
        
        # When coloured is first
        f.write("6. PERFORMANCE WHEN COLOURED SYSTEM IS PRESENTED FIRST\n")
        f.write("-" * 80 + "\n")
        f.write(stats['coloured_first'].to_string())
        f.write("\n\n")
        
        # When text is first
        f.write("7. PERFORMANCE WHEN TEXT SYSTEM IS PRESENTED FIRST\n")
        f.write("-" * 80 + "\n")
        f.write(stats['text_first'].to_string())
        f.write("\n\n")
        
        # Sample size information
        f.write("8. EXPERIMENT DETAILS\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total experiments conducted: {len(df) // 2}\n")
        f.write(f"Total trials: {len(df)}\n")
        f.write(f"Text system trials: {len(df[df['system'] == 'text'])}\n")
        f.write(f"Coloured system trials: {len(df[df['system'] == 'coloured'])}\n")
        f.write(f"Experiments starting with text: {len(df[df['first_system'] == 'text']) // 2}\n")
        f.write(f"Experiments starting with coloured: {len(df[df['first_system'] == 'coloured']) // 2}\n")
        f.write("\n\n")
        
        # Conclusions
        f.write("9. CONCLUSIONS AND INSIGHTS\n")
        f.write("-" * 80 + "\n")
        
        # Overall winner
        if coloured_mean < text_mean:
            f.write(f"• Overall, the COLOURED system performed better (faster completion times)\n")
        else:
            f.write(f"• Overall, the TEXT system performed better (faster completion times)\n")
        
        # Order effects analysis
        text_order_effect = stats['order_effect']['text']['difference']
        coloured_order_effect = stats['order_effect']['coloured']['difference']
        
        if abs(text_order_effect) > abs(coloured_order_effect):
            f.write(f"• The TEXT system showed stronger order effects\n")
        else:
            f.write(f"• The COLOURED system showed stronger order effects\n")
        
        if text_order_effect < 0 and coloured_order_effect < 0:
            f.write(f"• Both systems showed learning effects (faster on second trial)\n")
        elif text_order_effect > 0 and coloured_order_effect > 0:
            f.write(f"• Both systems showed fatigue effects (slower on second trial)\n")
        else:
            f.write(f"• Systems showed different order effects:\n")
            f.write(f"  - Text: {'learning' if text_order_effect < 0 else 'fatigue'} effect\n")
            f.write(f"  - Coloured: {'learning' if coloured_order_effect < 0 else 'fatigue'} effect\n")
        
        # Consistency
        text_std = stats['overall'].loc['text', 'std']
        coloured_std = stats['overall'].loc['coloured', 'std']
        
        if text_std < coloured_std:
            f.write(f"• TEXT system showed more consistent performance (lower std dev: {text_std:.2f}ms)\n")
        else:
            f.write(f"• COLOURED system showed more consistent performance (lower std dev: {coloured_std:.2f}ms)\n")
        
        f.write("\n")
        f.write("=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")
    
    print(f"✓ Statistical report saved to '{report_file}'")

def save_processed_data(df, output_dir='analysis_output'):
    """Save processed data to CSV for further analysis"""
    Path(output_dir).mkdir(exist_ok=True)
    
    # Save full processed data
    df.to_csv(f'{output_dir}/processed_data.csv', index=False)
    
    # Save summary statistics
    summary = df.groupby('system').agg({
        'duration_ms': ['count', 'mean', 'median', 'std', 'min', 'max'],
        'duration_s': ['mean', 'median']
    }).round(2)
    summary.to_csv(f'{output_dir}/summary_statistics.csv')
    
    print(f"✓ Processed data saved to '{output_dir}/' directory")

def main():
    """Main analysis pipeline"""
    print("\n" + "=" * 80)
    print("EXPERIMENT RESULTS ANALYSIS")
    print("=" * 80 + "\n")
    
    # Load data
    print("Loading experiment data...")
    raw_data = load_data()
    print(f"✓ Loaded {len(raw_data)} experiments\n")
    
    # Process data
    print("Processing data...")
    df = process_data(raw_data)
    print(f"✓ Processed {len(df)} trials\n")
    
    # Calculate statistics
    print("Calculating statistics...")
    stats = calculate_statistics(df)
    print("✓ Statistics calculated\n")
    
    # Create visualizations
    print("Generating visualizations...")
    create_visualizations(df)
    print()
    
    # Generate report
    print("Generating statistical report...")
    generate_report(stats, df)
    print()
    
    # Save processed data
    print("Saving processed data...")
    save_processed_data(df)
    print()
    
    # Quick summary to console
    print("=" * 80)
    print("QUICK SUMMARY")
    print("=" * 80)
    print("\nOverall Performance:")
    print(stats['overall'][['mean', 'median', 'std']])
    print("\nOrder Effects:")
    for system, effects in stats['order_effect'].items():
        print(f"\n{system.upper()}: {effects['difference']:+.2f}ms ({effects['percent_change']:+.1f}%) when second")
    
    print("\n" + "=" * 80)
    print("Analysis complete! Check the 'analysis_output' directory for all results.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
