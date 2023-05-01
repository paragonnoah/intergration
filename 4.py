import pandas as pd
from mediation.utils import ModelSpecificationError
from mediation import Mediation


def perform_mediation(dependent_var, mediator_var, independent_var, data):
    model_spec = f"{dependent_var} ~ {independent_var}\n" \
                 f"{mediator_var} ~ {independent_var}\n" \
                 f"{dependent_var} ~ {independent_var} + {mediator_var}"
    try:
        mediation_analysis = Mediation(data=data, model=model_spec, seed=123)
        mediation_analysis.run()
        print(f"Mediation analysis for {dependent_var}, {mediator_var}, and {independent_var}:")
        print(f"Direct effect of {independent_var} on {dependent_var}: {mediation_analysis.summary().de}")
        print(f"Indirect effect of {independent_var} on {dependent_var} through {mediator_var}: {mediation_analysis.summary().ie}")
        print(f"Total effect of {independent_var} on {dependent_var}: {mediation_analysis.summary().total}")
        print()
    except ModelSpecificationError:
        print(f"Invalid model specification for {dependent_var}, {mediator_var}, and {independent_var}.\n")
        pass


if __name__ == '__main__':
    data_file = "templatesdata.xlsx"
    sheet_name = "Sheet1"
    data = pd.read_excel(data_file, sheet_name=sheet_name)
    dependent_vars = ["x1", "x2", "x3"]
    mediator_vars = ["z1", "z2", "z3"]
    independent_vars = ["y1", "y2", "y3"]
    
    for d_var, m_var, i_var in zip(dependent_vars, mediator_vars, independent_vars):
        perform_mediation(d_var, m_var, i_var, data)
