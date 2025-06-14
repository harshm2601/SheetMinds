import streamlit as st
import pandas as pd
import tempfile
from llm import ask_llm
from sandbox import run_code_sandboxed
from utils import get_file_extension, get_data_overview

st.set_page_config(page_title="CSV Analyzer", layout="wide")
st.title("CSV/Sheet Analyzer with LLM")

uploaded_file = st.file_uploader("Upload a CSV, XLSX, or sheet file", type=["csv", "xlsx"]) 

if uploaded_file:
    ext = get_file_extension(uploaded_file.name)
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}') as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    if ext == 'csv':
        df = pd.read_csv(tmp_path)
    elif ext == 'xlsx':
        df = pd.read_excel(tmp_path)
    else:
        st.error("Unsupported file format.")
        st.stop()
    st.dataframe(df.head(100))
    st.markdown("---")
    user_query = st.text_area("Ask a question or request a visualization:")
    if st.button("Submit Query") and user_query:
        schema, sample = get_data_overview(df)
        context = {
            "schema": schema,
            "sample": sample,
            "query": user_query
        }
        code = None
        error = None
        for i in range(10):
            code = ask_llm(context, error=error)
            if not code or not isinstance(code, str):
                st.error("LLM did not return valid code. Please try again.")
                st.stop()
            st.markdown("**Generated Code:**")
            st.code(code, language="python")
            output, error = run_code_sandboxed(code, df)
            st.markdown("**Raw Output:**")
            st.write(output)
            if error is None:
                break
            context["last_error"] = error
        if error:
            st.error(f"Error: {error}")
        else:
            if output.get("type") == "plot":
                fig = output.get("figure")
                import matplotlib.figure
                import matplotlib.pyplot as plt
                if isinstance(fig, matplotlib.figure.Figure):
                    st.pyplot(fig, clear_figure=False)
                    import io
                    buf = io.BytesIO()
                    fig.savefig(buf, format="png")
                    buf.seek(0)
                    img_bytes = buf.read()
                    buf.close()
                    plt.close(fig)
                    # Ask Gemini for insights about the plot, passing the image
                    insight_prompt = f"Given the following user query and the attached plot image, provide concise insights and observations about the data and the visualization.\n\nUser Query: {user_query}"
                    with st.spinner("Getting insights from Gemini..."):
                        insights = ask_llm({
                            "prompt": insight_prompt,
                            "schema": schema,
                            "sample": sample,
                            "query": user_query
                        }, image=img_bytes)
                    st.markdown("**Insights from Gemini:**")
                    st.write(insights)
                else:
                    st.error("Plot output is not a valid matplotlib Figure.")
            elif output.get("type") == "table":
                st.dataframe(output["data"])
            else:
                st.write(output.get("data", "No output produced."))
