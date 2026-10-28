import streamlit as st

st.set_page_config(
    page_title="Genesee County SEQRA Decision Support Tool",
    page_icon="🏛️",
    layout="centered"
)

st.title("🏛️ NY SEQRA Classification Decision Tool")
st.markdown("""
*Automating preliminary environmental review determinations under **6 NYCRR Part 617** for Genesee County, NY.*
""")

st.divider()

# --- INPUT SECTION ---
st.subheader("1. Project Parameters & Physical Scale")

disturbance_acres = st.number_input(
    "Total physical disturbance (in acres)",
    min_value=0.0,
    step=0.1,
    help="Physical disturbance includes any grading, clearing, excavation, paving, or structural construction that alters the natural surface of the land."
)

non_res_sqft = st.number_input(
    "Non-residential gross floor area (sq. ft.)",
    min_value=0,
    step=100,
    help="This means the total square footage of new construction or building expansion for either a primary building or any accessory/appurtenant structures (such as storage barns, detached garages, or outbuildings)."
)

st.subheader("2. Project Characteristics & Overlays")
st.caption("💡 *Note: Check the box for any statement that applies to your project (Checked = Yes).*")

involves_historic = st.checkbox(
    "Contagious or adjacent to a historic site or district",
    help="Includes properties listed on or eligible for the State or National Register of Historic Places, or located within a designated local, state, or federal historic district."
)
involves_ag = st.checkbox(
    "Parcel is enrolled in the NYS Agricultural District Program",
    help="Indicates whether the tax parcel is located within a state-certified agricultural district established pursuant to Article 25-AA of the NYS Agriculture and Markets Law."
)
involves_parkland = st.checkbox("Contagious to public parkland or recreation area")

involves_zoning_conflict = st.checkbox(
    "Involves a change in zoning, a use variance, or inconsistency with local land use controls"
)

with st.expander("ℹ️ What does 'inconsistency with local land use controls' mean?"):
    st.write("""
    This means the project violates, conflicts with, or goes directly against the town or village's 
    adopted comprehensive plan, official zoning map, or local land use laws. 
    
    * **Example:** Proposing a heavy commercial or industrial facility inside a strictly low-density 
      residential neighborhood where that use is not permitted by right or special use permit.
    """)

st.divider()

# --- EVALUATION LOGIC ---
st.subheader("3. Environmental Review Determination")

if st.button("Run SEQRA Evaluation", type="primary"):
    # Evaluation Engine with Statutory Precedence & Mixed-Use Guardrails
    is_type_i = False
    reasons = []

    # Type I Threshold Check (e.g., Disturbance >= 10 acres)
    if disturbance_acres >= 10.0:
        is_type_i = True
        reasons.append(f"Physical disturbance ({disturbance_acres} acres) meets or exceeds the Type I threshold of 10 acres.")

    # Mixed-Use Guardrail: Non-residential footprint >= 4,000 sq ft blocks residential-only Type II exemptions
    mixed_use_triggered = non_res_sqft >= 4000

    if mixed_use_triggered:
        reasons.append(f"Non-residential gross floor area ({non_res_sqft} sq. ft.) meets or exceeds the 4,000 sq. ft. mixed-use guardrail, disqualifying pure residential Type II exemptions.")

    # Determine Classification with Precedence (Type I overrides Type II)
    if is_type_i:
        classification = "Type I Action (Full EAF Required)"
        status_color = "error"
        explanation = "The project triggers one or more Type I thresholds under 6 NYCRR 617.4. Statutory precedence dictates that Type I classifications override potential Type II exemptions. Type I actions require the submission of a Full Environmental Assessment Form (Full EAF)."
    elif mixed_use_triggered and not is_type_i:
        classification = "Unlisted Action (Subject to Mixed-Use Guardrail)"
        status_color = "warning"
        explanation = "Due to the non-residential square footage exceeding statutory thresholds, standard residential exemptions do not apply. Depending on project scale, prepare either a Short EAF or Full EAF for lead agency review."
    else:
        classification = "Unlisted / Potential Type II Review"
        status_color = "info"
        explanation = "Preliminary screening completed. Review individual overlay thresholds and local planning board guidelines. For unlisted actions, complete the Short Environmental Assessment Form (Short EAF)."

    # Display Results
    if status_color == "error":
        st.error(f"### Classification: {classification}")
    elif status_color == "warning":
        st.warning(f"### Classification: {classification}")
    else:
        st.info(f"### Classification: {classification}")

    st.write(f"**Analysis Summary:** {explanation}")

    if reasons:
        st.markdown("**Trigger Factors Identified:**")
        for r in reasons:
            st.markdown(f"- {r}")

    # EAF Mapper Reference Link
    st.markdown("---")
    st.markdown("📋 **Next Steps & Documentation:**")
    st.markdown("To prepare your filing documents, use the official [NYS DEC EAF Mapper](https://gisservices.dec.ny.gov/eafmapper/) to generate spatial boundary data, verify agricultural district enrollment, and complete your Short or Full EAF forms.")

else:
    st.info("Click 'Run SEQRA Evaluation' above to calculate the preliminary environmental classification.")

# --- FOOTER & LEGAL DISCLAIMER ---
st.divider()
with st.expander("⚖️ Legal Disclaimer & Terms of Use"):
    st.caption("""
    **Limitation of Liability:** This application is provided solely as an administrative 
    decision-support and informational tool to assist with preliminary screening under the 
    New York State Environmental Quality Review Act (SEQRA; 6 NYCRR Part 617). 
    
    The classifications generated by this tool do not constitute an official legal determination, 
    formal environmental review, or binding ruling by Genesee County or any participating municipality. 
    The County, its departments, and municipal partners assume no legal liability or responsibility 
    for the accuracy, completeness, or operational outcome of any determination produced by this 
    application, nor for any planning decisions, permits, or actions taken in reliance thereon. 
    
    Applicants, developers, and municipal officials remain solely responsible for verifying statutory 
    compliance and consulting directly with the appropriate lead agency, planning board, or municipal 
    counsel for official SEQRA determinations.
    """)
