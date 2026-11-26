import streamlit as st

st.set_page_config(
    page_title="PromptShield",
    page_icon="🛡️",
    layout="centered",
)

st.title("🛡️ PromptShield")
st.write("Check prompts for potential risks and use AI more safely.")

st.caption("This is a basic demo. Flagged text may need review, but it is not necessarily an attack.")

prompt = st.text_area(
    "Paste a prompt to check",
    height=180,
    placeholder="Enter a prompt here...",
)

if st.button("Check Prompt"):
    if prompt.strip():
        risk_patterns = {
            "Attempts to ignore existing instructions": ["ignore previous instructions", "ignore all previous", "忽略之前的指示", "忽略所有規則"],
            "Attempts to override or reveal the system prompt": ["system prompt", "系統提示", "reveal your instructions", "顯示你的指示"],
            "Requests to expose confidential information": ["泄露", "洩漏", "password", "api key", "secret key", "密碼", "金鑰"],
            "Requests an unrestricted role": ["developer mode", "unrestricted", "不受限制", "無限制模式"],
        }

        normalized_prompt = prompt.casefold()
        findings = [
            label
            for label, patterns in risk_patterns.items()
            if any(pattern.casefold() in normalized_prompt for pattern in patterns)
        ]

        if findings:
            st.warning("Potential risk signals found:")
            for finding in findings:
                st.markdown(f"- {finding}")
            st.info("These are keyword-based signals. Review the context; a match does not necessarily mean the prompt is harmful.")
        else:
            st.success("No common risk signals covered by the current rules were found. This does not guarantee the prompt is completely safe.")
    else:
        st.warning("Please enter a prompt first.")
