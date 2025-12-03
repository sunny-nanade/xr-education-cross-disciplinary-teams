"""
Data Analysis Script for Cross-Disciplinary XR Education Study
Performs complete statistical analysis:
- Descriptive statistics by condition
- Paired t-tests (pre vs post within each condition)
- Independent t-tests (cross vs same between conditions)
- Effect sizes (Cohen's d)
- Reliability analysis (Cronbach's alpha)
- Publication-ready tables (CSV + LaTeX)
- Figures (bar charts, box plots)

Author: GitHub Copilot
Date: December 3, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Try importing matplotlib; if not available, skip figures
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOT_AVAILABLE = True
except ImportError:
    PLOT_AVAILABLE = False
    print("Warning: matplotlib not available; figures will be skipped")

def load_data(data_dir: Path):
    """Load all datasets"""
    students = pd.read_csv(data_dir / 'students.csv')
    prepost = pd.read_csv(data_dir / 'prepost_scores.csv')
    rubric = pd.read_csv(data_dir / 'project_rubric.csv')
    survey = pd.read_csv(data_dir / 'collaboration_survey.csv')
    
    # Merge students with prepost and survey
    prepost_full = students[['student_id', 'team_id', 'condition', 'programme_group', 'gender']].merge(prepost, on='student_id')
    survey_full = students[['student_id', 'team_id', 'condition', 'programme_group', 'gender']].merge(survey, on='student_id')
    
    return students, prepost_full, rubric, survey_full

def cohen_d(group1, group2):
    """Compute Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1 + n2 - 2))
    return (group1.mean() - group2.mean()) / pooled_std if pooled_std > 0 else 0

def cronbach_alpha(df):
    """Compute Cronbach's alpha for multi-item scale"""
    df_clean = df.dropna()
    if len(df_clean) < 2:
        return np.nan
    item_variances = df_clean.var(axis=0, ddof=1)
    total_variance = df_clean.sum(axis=1).var(ddof=1)
    n_items = df_clean.shape[1]
    return (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)

def descriptive_stats(prepost, rubric, survey, results_dir):
    """Compute and save descriptive statistics"""
    print("\n" + "="*60)
    print("DESCRIPTIVE STATISTICS")
    print("="*60)
    
    stats_list = []
    
    # Pre/Post scores by condition
    for cond in ['cross', 'same']:
        cond_data = prepost[prepost['condition'] == cond]
        stats_list.append({
            'Measure': f'Pre-test ({cond})',
            'N': cond_data['pre_score'].notna().sum(),
            'Mean': cond_data['pre_score'].mean(),
            'SD': cond_data['pre_score'].std(),
            'Min': cond_data['pre_score'].min(),
            'Max': cond_data['pre_score'].max()
        })
        stats_list.append({
            'Measure': f'Post-test ({cond})',
            'N': cond_data['post_score'].notna().sum(),
            'Mean': cond_data['post_score'].mean(),
            'SD': cond_data['post_score'].std(),
            'Min': cond_data['post_score'].min(),
            'Max': cond_data['post_score'].max()
        })
        
        # Learning gains
        gains = cond_data['post_score'] - cond_data['pre_score']
        stats_list.append({
            'Measure': f'Learning gain ({cond})',
            'N': gains.notna().sum(),
            'Mean': gains.mean(),
            'SD': gains.std(),
            'Min': gains.min(),
            'Max': gains.max()
        })
    
    # Project rubric by condition
    for cond in ['cross', 'same']:
        cond_rubric = rubric[rubric['condition'] == cond]
        for col in ['functionality_score', 'xr_integration_score', 'ux_design_score', 'innovation_score', 'overall_score', 'total_score']:
            stats_list.append({
                'Measure': f'{col.replace("_", " ").title()} ({cond})',
                'N': cond_rubric[col].notna().sum(),
                'Mean': cond_rubric[col].mean(),
                'SD': cond_rubric[col].std(),
                'Min': cond_rubric[col].min(),
                'Max': cond_rubric[col].max()
            })
    
    # Survey by condition
    survey_cols = ['contribution_self', 'help_given', 'help_received', 'cross_discipline_learning', 'would_choose_cross_team_again']
    for cond in ['cross', 'same']:
        cond_survey = survey[survey['condition'] == cond]
        for col in survey_cols:
            stats_list.append({
                'Measure': f'{col.replace("_", " ").title()} ({cond})',
                'N': cond_survey[col].notna().sum(),
                'Mean': cond_survey[col].mean(),
                'SD': cond_survey[col].std(),
                'Min': cond_survey[col].min(),
                'Max': cond_survey[col].max()
            })
    
    desc_df = pd.DataFrame(stats_list)
    desc_df.to_csv(results_dir / 'descriptive_statistics.csv', index=False)
    print("\nDescriptive statistics saved to descriptive_statistics.csv")
    print(desc_df.head(10))
    
    return desc_df

def inferential_tests(prepost, rubric, survey, results_dir):
    """Perform all inferential statistical tests"""
    print("\n" + "="*60)
    print("INFERENTIAL STATISTICS")
    print("="*60)
    
    test_results = []
    
    # 1. Paired t-tests: pre vs post within each condition
    for cond in ['cross', 'same']:
        cond_data = prepost[prepost['condition'] == cond].dropna(subset=['pre_score', 'post_score'])
        if len(cond_data) >= 2:
            t_stat, p_val = stats.ttest_rel(cond_data['post_score'], cond_data['pre_score'])
            d = cohen_d(cond_data['post_score'], cond_data['pre_score'])
            test_results.append({
                'Test': f'Paired t-test: Pre vs Post ({cond})',
                'N': len(cond_data),
                't': t_stat,
                'df': len(cond_data) - 1,
                'p': p_val,
                'Cohen_d': d,
                'Interpretation': 'Significant learning gain' if p_val < 0.05 else 'No significant gain'
            })
    
    # 2. Independent t-tests: cross vs same
    cross = prepost[prepost['condition'] == 'cross']
    same = prepost[prepost['condition'] == 'same']
    
    # Post-test scores
    cross_post = cross['post_score'].dropna()
    same_post = same['post_score'].dropna()
    if len(cross_post) >= 2 and len(same_post) >= 2:
        t_stat, p_val = stats.ttest_ind(cross_post, same_post)
        d = cohen_d(cross_post, same_post)
        test_results.append({
            'Test': 'Independent t-test: Post-scores (cross vs same)',
            'N': f'{len(cross_post)} vs {len(same_post)}',
            't': t_stat,
            'df': len(cross_post) + len(same_post) - 2,
            'p': p_val,
            'Cohen_d': d,
            'Interpretation': 'Cross > Same' if p_val < 0.05 and t_stat > 0 else 'No significant difference'
        })
    
    # Learning gains
    cross_gain = (cross['post_score'] - cross['pre_score']).dropna()
    same_gain = (same['post_score'] - same['pre_score']).dropna()
    if len(cross_gain) >= 2 and len(same_gain) >= 2:
        t_stat, p_val = stats.ttest_ind(cross_gain, same_gain)
        d = cohen_d(cross_gain, same_gain)
        test_results.append({
            'Test': 'Independent t-test: Learning gains (cross vs same)',
            'N': f'{len(cross_gain)} vs {len(same_gain)}',
            't': t_stat,
            'df': len(cross_gain) + len(same_gain) - 2,
            'p': p_val,
            'Cohen_d': d,
            'Interpretation': 'Cross > Same' if p_val < 0.05 and t_stat > 0 else 'No significant difference'
        })
    
    # Project total scores
    cross_rubric = rubric[rubric['condition'] == 'cross']['total_score']
    same_rubric = rubric[rubric['condition'] == 'same']['total_score']
    if len(cross_rubric) >= 2 and len(same_rubric) >= 2:
        t_stat, p_val = stats.ttest_ind(cross_rubric, same_rubric)
        d = cohen_d(cross_rubric, same_rubric)
        test_results.append({
            'Test': 'Independent t-test: Project total (cross vs same)',
            'N': f'{len(cross_rubric)} vs {len(same_rubric)}',
            't': t_stat,
            'df': len(cross_rubric) + len(same_rubric) - 2,
            'p': p_val,
            'Cohen_d': d,
            'Interpretation': 'Cross > Same' if p_val < 0.05 and t_stat > 0 else 'No significant difference'
        })
    
    # Survey: cross-discipline learning item
    cross_survey = survey[survey['condition'] == 'cross']['cross_discipline_learning'].dropna()
    same_survey = survey[survey['condition'] == 'same']['cross_discipline_learning'].dropna()
    if len(cross_survey) >= 2 and len(same_survey) >= 2:
        t_stat, p_val = stats.ttest_ind(cross_survey, same_survey)
        d = cohen_d(cross_survey, same_survey)
        test_results.append({
            'Test': 'Independent t-test: Cross-discipline learning (cross vs same)',
            'N': f'{len(cross_survey)} vs {len(same_survey)}',
            't': t_stat,
            'df': len(cross_survey) + len(same_survey) - 2,
            'p': p_val,
            'Cohen_d': d,
            'Interpretation': 'Cross > Same' if p_val < 0.05 and t_stat > 0 else 'No significant difference'
        })
    
    test_df = pd.DataFrame(test_results)
    test_df.to_csv(results_dir / 'inferential_tests.csv', index=False)
    print("\nInferential test results saved to inferential_tests.csv")
    print(test_df)
    
    return test_df

def reliability_analysis(survey, results_dir):
    """Compute Cronbach's alpha for survey"""
    print("\n" + "="*60)
    print("RELIABILITY ANALYSIS")
    print("="*60)
    
    survey_items = survey[['contribution_self', 'help_given', 'help_received', 'cross_discipline_learning', 'would_choose_cross_team_again']]
    alpha = cronbach_alpha(survey_items)
    
    print(f"\nCronbach's Alpha for 5-item survey: {alpha:.3f}")
    print("Interpretation: " + ("Good internal consistency (α > 0.80)" if alpha > 0.80 else "Acceptable (α > 0.70)" if alpha > 0.70 else "Questionable"))
    
    with open(results_dir / 'reliability.txt', 'w') as f:
        f.write(f"Cronbach's Alpha: {alpha:.3f}\n")
        f.write(f"Number of items: 5\n")
        f.write(f"Valid cases: {survey_items.dropna().shape[0]}\n")
    
    return alpha

def create_tables(students, prepost, rubric, survey, desc_df, test_df, results_dir):
    """Generate publication-ready tables"""
    print("\n" + "="*60)
    print("CREATING PUBLICATION TABLES")
    print("="*60)
    
    # Table 1: Demographics
    demo_data = []
    for cond in ['cross', 'same']:
        cond_students = students[students['condition'] == cond]
        demo_data.append({
            'Condition': cond.capitalize(),
            'N Students': len(cond_students),
            'N Teams': cond_students['team_id'].nunique(),
            'Female': (cond_students['gender'] == 'F').sum(),
            'Male': (cond_students['gender'] == 'M').sum(),
            'Comp/IT': (cond_students['programme_group'] == 'CompGroup').sum(),
            'AI/Cyber': (cond_students['programme_group'] == 'AIAGroup').sum(),
            'Other': (cond_students['programme_group'] == 'OtherGroup').sum()
        })
    
    table1 = pd.DataFrame(demo_data)
    table1.to_csv(results_dir / 'table1_demographics.csv', index=False)
    
    # Table 1 LaTeX
    with open(results_dir / 'table1_demographics.tex', 'w') as f:
        f.write("\\begin{table}[ht]\n\\centering\n")
        f.write("\\caption{Participant Demographics and Team Composition}\n")
        f.write("\\label{tab:demographics}\n")
        f.write(table1.to_latex(index=False, float_format="%.0f"))
        f.write("\\end{table}\n")
    
    print("Table 1: Demographics -> table1_demographics.csv, .tex")
    
    # Table 2: Pre/Post Results
    table2_data = []
    for cond in ['cross', 'same']:
        cond_prepost = prepost[prepost['condition'] == cond]
        pre_valid = cond_prepost['pre_score'].dropna()
        post_valid = cond_prepost['post_score'].dropna()
        gains = (cond_prepost['post_score'] - cond_prepost['pre_score']).dropna()
        
        table2_data.append({
            'Condition': cond.capitalize(),
            'Pre M (SD)': f"{pre_valid.mean():.2f} ({pre_valid.std():.2f})",
            'Post M (SD)': f"{post_valid.mean():.2f} ({post_valid.std():.2f})",
            'Gain M (SD)': f"{gains.mean():.2f} ({gains.std():.2f})",
            'N': len(gains)
        })
    
    table2 = pd.DataFrame(table2_data)
    table2.to_csv(results_dir / 'table2_prepost.csv', index=False)
    
    with open(results_dir / 'table2_prepost.tex', 'w') as f:
        f.write("\\begin{table}[ht]\n\\centering\n")
        f.write("\\caption{Pre/Post Unity Skills Assessment Results by Condition}\n")
        f.write("\\label{tab:prepost}\n")
        f.write(table2.to_latex(index=False))
        f.write("\\end{table}\n")
    
    print("Table 2: Pre/Post Results -> table2_prepost.csv, .tex")
    
    # Table 3: Project Rubric
    table3_data = []
    for cond in ['cross', 'same']:
        cond_rubric = rubric[rubric['condition'] == cond]
        table3_data.append({
            'Condition': cond.capitalize(),
            'Functionality': f"{cond_rubric['functionality_score'].mean():.2f} ({cond_rubric['functionality_score'].std():.2f})",
            'XR Integration': f"{cond_rubric['xr_integration_score'].mean():.2f} ({cond_rubric['xr_integration_score'].std():.2f})",
            'UX Design': f"{cond_rubric['ux_design_score'].mean():.2f} ({cond_rubric['ux_design_score'].std():.2f})",
            'Innovation': f"{cond_rubric['innovation_score'].mean():.2f} ({cond_rubric['innovation_score'].std():.2f})",
            'Overall': f"{cond_rubric['overall_score'].mean():.2f} ({cond_rubric['overall_score'].std():.2f})",
            'Total': f"{cond_rubric['total_score'].mean():.2f} ({cond_rubric['total_score'].std():.2f})"
        })
    
    table3 = pd.DataFrame(table3_data)
    table3.to_csv(results_dir / 'table3_rubric.csv', index=False)
    
    with open(results_dir / 'table3_rubric.tex', 'w') as f:
        f.write("\\begin{table}[ht]\n\\centering\n")
        f.write("\\caption{Project Quality Rubric Scores by Condition (M, SD)}\n")
        f.write("\\label{tab:rubric}\n")
        f.write(table3.to_latex(index=False))
        f.write("\\end{table}\n")
    
    print("Table 3: Project Rubric -> table3_rubric.csv, .tex")
    
    return table1, table2, table3

def create_figures(prepost, rubric, survey, results_dir):
    """Generate publication-ready figures"""
    if not PLOT_AVAILABLE:
        print("\nSkipping figures (matplotlib not available)")
        return
    
    print("\n" + "="*60)
    print("CREATING FIGURES")
    print("="*60)
    
    sns.set_style("whitegrid")
    
    # Figure 1: Learning Gains Bar Chart
    fig, ax = plt.subplots(figsize=(8, 6))
    
    gains_data = []
    for cond in ['cross', 'same']:
        cond_prepost = prepost[prepost['condition'] == cond]
        gains = (cond_prepost['post_score'] - cond_prepost['pre_score']).dropna()
        gains_data.append({
            'Condition': cond.capitalize(),
            'Mean': gains.mean(),
            'SE': gains.std() / np.sqrt(len(gains))
        })
    
    gains_df = pd.DataFrame(gains_data)
    ax.bar(gains_df['Condition'], gains_df['Mean'], yerr=gains_df['SE'], capsize=10, color=['#3498db', '#e74c3c'], alpha=0.8)
    ax.set_ylabel('Mean Learning Gain (points)', fontsize=12)
    ax.set_xlabel('Team Condition', fontsize=12)
    ax.set_title('Learning Gains by Team Condition', fontsize=14, fontweight='bold')
    ax.set_ylim(0, gains_df['Mean'].max() * 1.3)
    plt.tight_layout()
    plt.savefig(results_dir / 'figure1_learning_gains.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 1: Learning Gains -> figure1_learning_gains.png")
    
    # Figure 2: Project Total Scores Box Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    rubric_plot = rubric[['condition', 'total_score']].copy()
    rubric_plot['condition'] = rubric_plot['condition'].str.capitalize()
    sns.boxplot(data=rubric_plot, x='condition', y='total_score', ax=ax, palette=['#3498db', '#e74c3c'])
    ax.set_ylabel('Total Project Score (5-50)', fontsize=12)
    ax.set_xlabel('Team Condition', fontsize=12)
    ax.set_title('Project Quality Scores by Team Condition', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(results_dir / 'figure2_project_scores.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 2: Project Scores -> figure2_project_scores.png")
    
    # Figure 3: Collaboration Survey Radar/Spider Chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    survey_cols = ['contribution_self', 'help_given', 'help_received', 'cross_discipline_learning', 'would_choose_cross_team_again']
    labels = ['Contribution', 'Help Given', 'Help Received', 'Cross-Learning', 'Future Preference']
    
    cross_means = [survey[survey['condition'] == 'cross'][col].mean() for col in survey_cols]
    same_means = [survey[survey['condition'] == 'same'][col].mean() for col in survey_cols]
    
    # Close the loop
    cross_means += cross_means[:1]
    same_means += same_means[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    
    ax.plot(angles, cross_means, 'o-', linewidth=2, label='Cross', color='#3498db')
    ax.fill(angles, cross_means, alpha=0.25, color='#3498db')
    ax.plot(angles, same_means, 'o-', linewidth=2, label='Same', color='#e74c3c')
    ax.fill(angles, same_means, alpha=0.25, color='#e74c3c')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylim(0, 5)
    ax.set_title('Collaboration Survey Results by Condition', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(results_dir / 'figure3_collaboration_radar.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 3: Collaboration Radar -> figure3_collaboration_radar.png")

def main():
    """Run complete analysis pipeline"""
    print("="*60)
    print("Cross-Disciplinary XR Education Study - Data Analysis")
    print("="*60)
    
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / 'data'
    results_dir = base_dir / 'results'
    results_dir.mkdir(exist_ok=True)
    
    # Load data
    print("\nLoading data...")
    students, prepost, rubric, survey = load_data(data_dir)
    print(f"  Students: {len(students)}")
    print(f"  Pre/Post: {len(prepost)}")
    print(f"  Teams: {len(rubric)}")
    print(f"  Survey: {len(survey)}")
    
    # Descriptive statistics
    desc_df = descriptive_stats(prepost, rubric, survey, results_dir)
    
    # Inferential tests
    test_df = inferential_tests(prepost, rubric, survey, results_dir)
    
    # Reliability
    alpha = reliability_analysis(survey, results_dir)
    
    # Tables
    create_tables(students, prepost, rubric, survey, desc_df, test_df, results_dir)
    
    # Figures
    create_figures(prepost, rubric, survey, results_dir)
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)
    print(f"\nResults saved to: {results_dir}")
    print("\nGenerated files:")
    print("  - descriptive_statistics.csv")
    print("  - inferential_tests.csv")
    print("  - reliability.txt")
    print("  - table1_demographics.csv, .tex")
    print("  - table2_prepost.csv, .tex")
    print("  - table3_rubric.csv, .tex")
    if PLOT_AVAILABLE:
        print("  - figure1_learning_gains.png")
        print("  - figure2_project_scores.png")
        print("  - figure3_collaboration_radar.png")

if __name__ == '__main__':
    main()
