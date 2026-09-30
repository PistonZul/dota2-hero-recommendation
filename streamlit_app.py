import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Dota 2 Draft Assistant",
    page_icon="🎮",
    layout="centered"
)

st.title("Dota 2 Draft Recommendation System")
st.markdown(
    "Aplikacja wspomagająca decyzje w fazie draftu gry **Dota 2** "
    "na podstawie analizy danych historycznych."
)

st.divider()

with st.form("input_form"):
    match_id = st.text_input("Match ID", placeholder="np. 8551366369")
    hero_name = st.text_input("Hero name", placeholder="np. Jakiro")
    submitted = st.form_submit_button("Generate recommendations")

if submitted:
    if not match_id or not hero_name:
        st.warning("Uzupełnij wszystkie pola.")
    else:
        with st.spinner("Analiza draftu..."):
            payload = {
                "match_id": int(match_id),
                "hero_name": hero_name
            }

            r = requests.post(f"{API_URL}/recommend", json=payload, timeout=90)

            if r.status_code != 200:
                st.error(r.json().get("detail", "Błąd serwera"))
            else:
                data = r.json()

                st.success("Rekomendacje wygenerowane!")

                st.markdown(
                    f"**Side:** {data['side'].capitalize()}  \n"
                    f"**Pick index:** {data['pick_index']}  \n"
                    f"**Picked hero:** {data['picked_hero']['name']}"
                )

                st.divider()
                st.subheader("Recommended heroes")

                for rec in data["recommendations"]:
                    cols = st.columns([1, 4, 2])

                    with cols[0]:
                        st.image(rec["icon_url"], width=64)

                    with cols[1]:
                        st.markdown(f"### {rec['name']}")
                        st.caption(f"Hero ID: {rec['hero_id']}")

                    with cols[2]:
                        st.metric(
                            "Probability",
                            f"{rec['probability'] * 100:.1f}%"
                        )

                    st.divider()
