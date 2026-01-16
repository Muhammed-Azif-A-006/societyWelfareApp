import streamlit as st


def render_lottie(url: str, height: int = 220, key: str | None = None) -> None:
    if st.session_state.get("reduce_motion"):
        return
    st.components.v1.html(
        f"""
        <div class="lottie-wrapper">
            <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
            <lottie-player src="{url}" background="transparent" speed="1" style="width: 100%; height: {height}px;" loop autoplay></lottie-player>
        </div>
        """,
        height=height,
    )
