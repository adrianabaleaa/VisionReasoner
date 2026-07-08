import os
import tempfile
import streamlit as st
from OBJECT_DETECTION import detect_objects, build_prompt
from scene_analyzer import analyze_scene
from LLM import ask_llm


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="VisionReasoner",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 VisionReasoner")

st.markdown(
    """
Upload an image and ask questions about it.

The assistant analyzes the image and answers using visual reasoning.
"""
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "scene_analysis" not in st.session_state:
    st.session_state.scene_analysis = None

if "image_loaded" not in st.session_state:
    st.session_state.image_loaded = False

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("Controls")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

    st.markdown("---")

    st.markdown(
        """
### Example questions

- Is this place safe?
- Describe the environment.
- How many objects are visible?
- Could someone work here?
- What stands out in this image?
"""
    )


# ==========================================================
# IMAGE UPLOAD
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    suffix = os.path.splitext(uploaded_file.name)[1]

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    temp.write(uploaded_file.read())
    temp.close()

    image_path = temp.name

    with st.spinner("Analyzing image..."):

        detected_objects, result, width, height = detect_objects(image_path)

        scene_analysis = analyze_scene(
            detected_objects,
            width,
            height
        )

    st.session_state.scene_analysis = scene_analysis
    st.session_state.image_loaded = True
    st.session_state.uploaded_image = image_path


# ==========================================================
# MAIN LAYOUT
# ==========================================================

left, right = st.columns([1, 1.2])

# ----------------------------------------------------------
# IMAGE
# ----------------------------------------------------------

with left:

    if st.session_state.image_loaded:

        st.image(
            st.session_state.uploaded_image,
            use_container_width=True
        )

    else:

        st.info("Upload an image to begin.")


# ----------------------------------------------------------
# CHAT
# ----------------------------------------------------------

with right:

    st.subheader("💬 Chat")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    if st.session_state.image_loaded:

        question = st.chat_input(
            "Ask something about the image..."
        )

        if question:

            with st.chat_message("user"):

                st.markdown(question)

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            prompt = build_prompt(
                st.session_state.scene_analysis,
                question
            )

            with st.spinner("Reasoning..."):

                answer = ask_llm(prompt)

            with st.chat_message("assistant"):

                st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

    else:

        st.info("Upload an image to start chatting.")