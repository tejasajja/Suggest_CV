import streamlit as st
from app_sidebar import sidebar
from llm_functions import instantiate_LLM_main, get_api_keys_from_local_env
from retrieval import retrieval_main
from resume_analyzer import resume_analyzer_main
from resume_Matcher import resume_matcher_main
from app_display_results import display_resume_analysis
from app_display_resultsm import display_resume_analysism


def ftab():
    """Analyze the uploaded resume."""

    if st.button("Analyze resume"):
        with st.spinner("Please wait..."):
            try:
                retrieval_main()
                st.session_state.llm = instantiate_LLM_main(temperature=0.0, top_p=0.95)
                st.session_state.llm_creative = instantiate_LLM_main(
                    temperature=st.session_state.temperature,
                    top_p=st.session_state.top_p,
                )
                st.session_state.SCANNED_RESUME = resume_analyzer_main(
                    llm=st.session_state.llm,
                    llm_creative=st.session_state.llm_creative,
                    documents=st.session_state.documents,
                )
                display_resume_analysis(st.session_state.SCANNED_RESUME)
            except Exception as e:
                st.error(f"An error occured: {e}")


def stab(jd):
    """Analyze the uploaded resume."""

    if st.button("Match resume"):
        with st.spinner("Please wait..."):
            try:
                retrieval_main()
                st.session_state.llm = instantiate_LLM_main(temperature=0.0, top_p=0.95)
                st.session_state.llm_creative = instantiate_LLM_main(
                    temperature=st.session_state.temperature,
                    top_p=st.session_state.top_p,
                )
                st.session_state.SCANNED_RESUME = resume_matcher_main(
                    llm=st.session_state.llm,
                    llm_creative=st.session_state.llm_creative,
                    documents=st.session_state.documents,
                    jd=jd
                )
                display_resume_analysism(st.session_state.SCANNED_RESUME)
            except Exception as e:
                st.error(f"An error occured: {e}")



if __name__ == "__main__":
    st.set_page_config(page_title="Resume Suggestions", page_icon="🚀")
    openai_api_key, google_api_key, cohere_api_key = get_api_keys_from_local_env()
    sidebar(openai_api_key, google_api_key, cohere_api_key)
    
    tab1, tab2, tab3 = st.tabs(["Scanner", "Matcher", "Overall"])
    
    with tab1:
        st.title("🔎 Resume Scanner")
        st.session_state.uploaded_file = st.file_uploader(
            label="**Upload Resume**",
            accept_multiple_files=False,
            type=(["pdf"]),
        )
        ftab()
        
        
    with tab2: 
        st.title("🔎 Resume Matcher")
        jd = st.text_area('Paste the Job description')
        
        st.session_state.uploaded_file = st.file_uploader(
            label="**Upload Resumea**",
            accept_multiple_files=False,
            type=(["pdf"]),
        )
        stab(jd)
    

    
    


