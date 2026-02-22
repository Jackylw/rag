import streamlit as st

import config_data
from rag import RagService

st.set_page_config(page_title="智能客服", page_icon="🤖")
st.title("🤖 智能客服")
st.divider()

# ── 初始化 session_state ──
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "你好，我是智能客服，有什么问题我可以帮助你吗？"}
    ]

if "rag_service" not in st.session_state:
    st.session_state["rag_service"] = RagService()

# ── 渲染历史消息 ──
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── 用户输入 ──
if prompt := st.chat_input("请输入你的问题..."):
    # 显示用户消息并追加到历史
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 流式输出助手回复
    with st.chat_message("assistant"):
        # 使用 st.write_stream 配合 chain.stream 实现逐字流式输出
        response = st.write_stream(
            st.session_state["rag_service"].chain.stream(
                {"question": prompt},
                config=config_data.session_config,
            )
        )

    # 将完整回复追加到历史
    st.session_state["messages"].append({"role": "assistant", "content": response})
