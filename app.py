import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Fact-Check Agent",
    page_icon="🕵️",
    layout="wide"
)

from utils.extractor import (
    extract_text_from_pdf,
    extract_claims
)

from utils.verifier import (
    search_claim_online,
    classify_claim
)

st.set_page_config(
    page_title="Fact-Check Agent",
    layout="wide"
)

st.title("🕵️ AI Fact-Check Agent")

st.caption(
    "Upload PDFs and automatically verify claims using live web intelligence."
)

st.sidebar.title("About")

st.sidebar.write(
    """
    This AI-powered Fact-Check Agent:

    • Extracts claims from PDFs

    • Searches live web data

    • Verifies authenticity

    • Flags misinformation
    """
)

st.write(
    "Upload a PDF and verify claims using live web search."
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success(
        "PDF Uploaded Successfully ✅"
    )

    extracted_text = extract_text_from_pdf(
        uploaded_file
    )

    st.subheader("Extracted Text")

    if extracted_text.strip() == "":

        st.error(
            "No readable text found."
        )

    else:

        st.write(extracted_text[:3000])

        claims = extract_claims(
            extracted_text
        )

        st.subheader("Detected Claims")
        
        results_data = []

        if claims:

            for idx, claim in enumerate(
                claims,
                start=1
            ):

                st.markdown("---")

                st.subheader(
                    f"Claim {idx}"
                )

                st.write(claim)

                with st.spinner(
                    "🔍 Verifying claim using live web data..."
                ):

                    results = search_claim_online(
                        claim
                    )

                    status, confidence = classify_claim(
                        claim,
                        results
                    )
                    
                    results_data.append({

                        "Claim": claim,

                        "Status": status,

                        "Confidence": f"{confidence}%"
                    })
                    
                st.markdown("---")

                st.subheader("📊 Verification Summary")

                df = pd.DataFrame(results_data)

                st.dataframe(
                    df,
                    use_container_width=True
                )
                
                verified_count = len(
                    df[df["Status"] == "Verified"]
                )

                false_count = len(
                    df[df["Status"] == "False"]
                )

                inaccurate_count = len(
                    df[df["Status"] == "Inaccurate"]
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "✅ Verified",
                    verified_count
                )

                col2.metric(
                    "❌ False",
                    false_count
                )

                col3.metric(
                    "⚠️ Inaccurate",
                    inaccurate_count
                )

                # Status UI
                st.write(
                    f"Confidence Score: {confidence}%"
                )
                
                if status == "Verified":

                    st.success(
                        f"✅ {status}"
                    )

                elif status == "False":

                    st.error(
                        f"❌ {status}"
                    )

                else:

                    st.warning(
                        f"⚠️ {status}"
                    )

                st.subheader(
                    "Evidence Sources"
                )

                for result in results:

                    st.write(
                        f"### {result['title']}"
                    )

                    st.write(
                        result['content']
                    )

                    st.write(
                        result['url']
                    )

        else:

            st.warning(
                "No claims detected."
            )