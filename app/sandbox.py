import io
import contextlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

def run_code_sandboxed(code, df):
    """
    Executes the generated code in a restricted environment.
    Returns output dict and error (if any).
    """
    output = {}
    error = None
    local_vars = {'df': df, 'pd': pd, 'np': np, 'plt': plt, 'sns': sns}
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {}, local_vars)
        # Capture the figure before any plt.clf() or plt.close() is called in user code
        figs = [plt.figure(num) for num in plt.get_fignums()]
        if figs:
            fig = figs[-1]  # get the last created figure
            output = {"type": "plot", "figure": fig}
        elif 'result' in local_vars and isinstance(local_vars['result'], pd.DataFrame):
            output = {"type": "table", "data": local_vars['result']}
        elif 'result' in local_vars:
            output = {"type": "text", "data": local_vars['result']}
        else:
            output = {"type": "text", "data": stdout.getvalue()}
    except Exception as e:
        error = str(e)
        output = {}
    return output, error
