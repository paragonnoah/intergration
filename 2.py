import pandas as pd
from factor_analyzer import FactorAnalyzer

# Load data from Excel file
df = pd.read_excel("templatesdata.xlsx")

# Define dependent variables
dep_vars = ["x1", "x2", "x3"]

# Perform factor analysis with maximum likelihood estimation
fa = FactorAnalyzer(n_factors=3, rotation="varimax", method="ml")
fa.fit(df[dep_vars])

# Print variance interpretation rate table
print("Variance interpretation rate table:")
print(fa.get_factor_variance())

# Print rotation factor loading coefficient table
print("\nRotation factor loading coefficient table:")
print(fa.loadings_)

# Print component score coefficient matrix
print("\nComponent score coefficient matrix:")
print(fa.transform(df[dep_vars]))

# Print gravel map
print("\nGravel map:")
print(fa.get_communalities())

# Print linear combination coefficient and weight results
print("\nLinear combination coefficient and weight results:")
print(fa.get_uniquenesses())
