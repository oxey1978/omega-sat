import streamlit as st

# --- Local detectors (Omega-1 required, Omega-2 optional) ---
from omega1_detector_ref import (
    detect_omega1, read_dimacs,
    F_prime, F_doubleprime, F_tripleprime, F_hex
)

# Try to import Omega-2 if you add it later
try:
    from omega2_detector import is_omega2
    HAVE_OMEGA2 = True
except Exception:
    HAVE_OMEGA2 = False

st.set_page_config(page_title="Ω-SAT Detector", page_icon="🔎", layout="centered")
st.title("Ω-SAT Detector (Ω1 / Ω1.5 and Ω2)")

st.markdown(
    "Upload a DIMACS `.cnf`, or run built-in fixtures. "
    "If `omega2_detector.py` is present, Ω2 results will appear too."
)

def pretty_omega1(res):
    st.subheader("Ω1 Result")
    st.write({
        "is_omega1": getattr(res, "is_omega1", None),
        "witness_seed": getattr(res, "witness_seed", None),
        "witness_literal": getattr(res, "witness_literal", None),
        "witness_depth": getattr(res, "witness_depth", None),
        "conflict_kind": getattr(res, "conflict_kind", None),
    })
    reasons = getattr(res, "reasons", None)
    if reasons:
        st.markdown("**Reasons**")
        for r in reasons:
            st.write("- " + str(r))
    path = getattr(res, "witness_path", None)
    if path:
        st.markdown("**Witness Path**")
        st.write(path)

def pretty_omega2(F):
    if not HAVE_OMEGA2:
        st.info("Ω2 module not present. Add `omega2_detector.py` to enable.")
        return
    try:
        res = is_omega2(F)
    except Exception as e:
        st.warning(f"Ω2 failed: {e}")
        return
    st.subheader("Ω2 Result")
    st.write({
        "is_omega2": getattr(res, "is_omega2", None),
        "screen_omega1_singletons": getattr(res, "screen_omega1_singletons", None),
        "witness_pair": getattr(res, "witness_pair", None),
        "conflict_kind": getattr(res, "conflict_kind", None),
        "flowdepth2": getattr(res, "flowdepth2", None),
    })
    reasons = getattr(res, "reasons", None)
    if reasons:
        st.markdown("**Reasons**")
        for r in reasons:
            st.write("- " + str(r))

# --- UI tabs ---
tab_upload, tab_fixtures = st.tabs(["Upload CNF", "Run Fixtures"])

with tab_upload:
    f = st.file_uploader("Upload a DIMACS .cnf file", type=["cnf", "txt"])
    if f is not None:
        import tempfile, os
        try:
            bytestr = f.read()
            with tempfile.NamedTemporaryFile("wb", delete=False, suffix=".cnf") as tmp:
                tmp.write(bytestr)
                tmp_path = tmp.name
            F = read_dimacs(tmp_path)
            os.unlink(tmp_path)
        except Exception as e:
            st.error(f"Failed to parse DIMACS: {e}")
            F = None

        if F is not None:
            try:
                res1 = detect_omega1(F)
                pretty_omega1(res1)
            except Exception as e:
                st.error(f"Ω1 failed: {e}")
            try:
                pretty_omega2(F)
            except Exception as e:
                st.warning(f"Ω2 skipped or failed: {e}")

with tab_fixtures:
    st.markdown("Run built-in Ω1 fixtures from the library.")
    choice = st.selectbox(
        "Pick a fixture",
        ["F′ (depth≈3)", "F″ (depth≈4)", "F‴ (depth≈5)", "F⁴ (depth≈6)"]
    )
    if st.button("Run Fixture"):
        if choice.startswith("F′"):
            F = F_prime()
        elif choice.startswith("F″"):
            F = F_doubleprime()
        elif choice.startswith("F‴"):
            F = F_tripleprime()
        else:
            F = F_hex()
        try:
            res1 = detect_omega1(F)
            pretty_omega1(res1)
        except Exception as e:
            st.error(f"Ω1 failed on fixture: {e}")
        try:
            pretty_omega2(F)
        except Exception as e:
            st.warning(f"Ω2 skipped or failed: {e}")

st.caption("Built with Streamlit. Add `omega2_detector.py` + `omega2_family.py` to enable Ω2.")
