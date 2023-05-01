import pandas as pd
import numpy as np
from statsmodels.stats.multicomp import MultiComparison
from scipy.stats import f
from scipy.stats import f_oneway, ttest_ind

# Load the data from the spreadsheet
df = pd.read_excel('templatesdata.xlsx')

# Set the group column as a categorical variable
df['group'] = df['group'].astype('category')

# Define a function for performing ANOVA and multiple comparisons
def perform_anova_and_multiple_comparisons(dep_vars):
    for dep_var in dep_vars:
        # Calculate the mean and standard deviation for each group
        means = df.groupby('group')[dep_var].mean()
        stds = df.groupby('group')[dep_var].std()

        # Calculate the ANOVA statistics
        n_groups = len(df['group'].unique())
        n_obs = len(df[dep_var])
        n_total = n_groups * n_obs
        ss_total = np.sum((df[dep_var] - np.mean(df[dep_var]))**2)
        ss_between = np.sum((means - np.mean(df[dep_var]))**2 * n_obs)
        ss_within = ss_total - ss_between
        ms_between = ss_between / (n_groups - 1)
        ms_within = ss_within / (n_total - n_groups)
        f_value = ms_between / ms_within
        p_value = f.sf(f_value, n_groups - 1, n_total - n_groups)

        # Perform multiple comparisons using LSD, Scheffe, and letter marking methods
        mc = MultiComparison(df[dep_var], df['group'])
        lsd_results = mc.allpairtest(ttest_ind, method='bonf')[1]
        lsd_results = mc.allpairtest(ttest_ind, method='bonferroni')[1]
        letter_results = mc.allpairtest(ttest_ind, method='hs')[1]

        # Print the results for LSD, Scheffe, and letter marking methods
        print(f"Analysis of variance for {dep_var}:")
        print(f"Mean for each group:\n{means}")
        print(f"Standard deviation for each group:\n{stds}")
        print(f"Overall mean: {np.mean(df[dep_var])}")
        print(f"Overall standard deviation: {np.std(df[dep_var])}")
        print(f"Difference between each group:")
        for i in range(n_groups):
            for j in range(i+1, n_groups):
                group_i = df[df['group'] == df['group'].unique()[i]][dep_var]
                group_j = df[df['group'] == df['group'].unique()[j]][dep_var]
                diff = np.mean(group_i) - np.mean(group_j)
                print(f"{df['group'].unique()[i]} - {df['group'].unique()[j]}: {diff}")
        print(f"F-value: {f_value}")
        print(f"P-value: {p_value}")
        print("LSD:")
        print(lsd_results)
        print("Scheffe:")
        # print(scheffe_results)
        print("Letter marking:")
        print(letter_results)
        print()
        
# Call the function with the list of dependent variables to analyze
perform_anova_and_multiple_comparisons(['x1', 'x2', 'x3'])
