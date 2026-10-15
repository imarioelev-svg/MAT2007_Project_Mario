import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ==========================================
# STEP 1: Load and Merge Data
# ==========================================
demo_df = pd.read_sas('D:\MyCode\.vscode\Project_Sleep_Pressure\DEMO_L.XPT')
slq_df = pd.read_sas('D:\MyCode\.vscode\Project_Sleep_Pressure\SLQ_L.XPT')
bp_df = pd.read_sas('D:\MyCode\.vscode\Project_Sleep_Pressure\BPXO_L.XPT')

df = pd.merge(demo_df, slq_df, on='SEQN', how='inner')
df = pd.merge(df, bp_df, on='SEQN', how='inner')

# ==========================================
# STEP 2: Data Cleaning and Feature Engineering
# ==========================================
df['Sleep_Hours'] = df['SLD013'].replace({77: np.nan, 99: np.nan})
df['Mean_Systolic_BP'] = df[['BPXOSY1', 'BPXOSY2', 'BPXOSY3']].mean(axis=1)
df['Age'] = df['RIDAGEYR']

analysis_df = df[['SEQN', 'Sleep_Hours', 'Age', 'Mean_Systolic_BP']].dropna()

# ==========================================
# STEP 3: Normalization and Age Binning
# ==========================================
# Z-score Normalization: (Value - Population Mean) / Standard Deviation
bp_mean = analysis_df['Mean_Systolic_BP'].mean()
bp_std = analysis_df['Mean_Systolic_BP'].std()
analysis_df['Normalized_BP'] = (analysis_df['Mean_Systolic_BP'] - bp_mean) / bp_std

# Create clinical age bins
bins = [17, 39, 59, 150] # Cutoffs
labels = ['18-39 (Young Adult)', '40-59 (Middle Age)', '60+ (Older Adult)']
analysis_df['Age_Group'] = pd.cut(analysis_df['Age'], bins=bins, labels=labels)

# ==========================================
# STEP 4: Visualization (Updated)
# ==========================================
sns.set_theme(style="whitegrid")

# Graph 1: Line Plot connecting the means (The "Zig-Zag" approach)
plt.figure(figsize=(10, 6))

sns.lineplot(
    x='Sleep_Hours', 
    y='Normalized_BP', 
    hue='Age_Group', 
    data=analysis_df, 
    marker='o',          # Places a distinct dot at each sleep hour mark
    errorbar=('ci', 95), # Displays a 95% confidence interval band around the line
    palette="viridis",
    linewidth=2
)

plt.title('Average Normalized Systolic BP by Sleep Duration and Age Group')
plt.xlabel('Hours of Sleep per Night')
plt.ylabel('Normalized Systolic BP (Z-Score)')

# Move the legend outside the plot so it doesn't cover your data
plt.legend(title='Age Group', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('D:\MyCode\.vscode\Project_Sleep_Pressure\sleep_bp_age_lineplot.png', dpi=300)
plt.show()

# Graph 2: Statistical Correlation Matrix (Heatmap)
plt.figure(figsize=(7, 5))
# Calculate Pearson correlation for the continuous variables
corr_matrix = analysis_df[['Sleep_Hours', 'Age', 'Mean_Systolic_BP']].corr()

# Draw the heatmap
sns.heatmap(
    corr_matrix, 
    annot=True,        # Show the exact correlation numbers
    cmap='coolwarm',   # Red = positive correlation, Blue = negative
    fmt=".3f",         # Format to 3 decimal places
    vmin=-1, vmax=1,   # Anchor the color scale
    center=0
)
plt.title('Pearson Correlation Matrix')
plt.savefig('D:\MyCode\.vscode\Project_Sleep_Pressure\correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

####################TRIPLE GRAHH: Binned Heatmaps for Sleep Duration Brackets####################

# 1. Define the 3 specific sleep bins
bins = [0, 5.5, 9.5, 24]
labels = ['Short Sleep (<6 hrs)', 'Normal Sleep (5-9 hrs)', 'Long Sleep (>9 hrs)']
analysis_df['Sleep_Bin'] = pd.cut(analysis_df['Sleep_Hours'], bins=bins, labels=labels)

# 2. Set up a 1x3 grid for the heatmaps to display side-by-side
# This is ideal for a 2-page report or a wide presentation slide
fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
fig.suptitle('Pearson Correlation by Sleep Duration Bracket', fontsize=16, y=1.05)

# Variables to correlate
cols = ['Sleep_Hours', 'Age', 'Mean_Systolic_BP']

# 3. Iterate through each bin and generate its specific heatmap
for i, bin_name in enumerate(labels):
    # Isolate data for the current bin
    subset = analysis_df[analysis_df['Sleep_Bin'] == bin_name]
    
    # Calculate the correlation matrix
    corr_matrix = subset[cols].corr()
    
    # Generate the heatmap on the specific subplot axis (axes[i])
    sns.heatmap(
        corr_matrix, 
        ax=axes[i],
        annot=True, 
        cmap='coolwarm', 
        fmt=".3f", 
        vmin=-1, vmax=1,  # Crucial: Locks the color scale so reds/blues mean the exact same thing across all 3 graphs
        cbar=True if i == 2 else False, # Only show the color legend on the final graph to reduce clutter
        square=True
    )
    
    axes[i].set_title(f'{bin_name}\n(n={len(subset)})') # Adding 'n' shows the sample size for each bin
    axes[i].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('D:\MyCode\.vscode\Project_Sleep_Pressure\sleep_binned_heatmaps.png', dpi=300, bbox_inches='tight')
plt.show()