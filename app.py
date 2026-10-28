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

num_residential_units = st.number_input(
    "Number of residential units",
    min_value=0,
    step=1,
    help="Total number of new dwelling units proposed (e.g., single-family homes, apartments, or townhome units)."
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
involves_parkland = st.checkbox(
    "Contagious to public parkland or recreation area",
    help="Includes properties that share a common boundary with or are directly adjacent to publicly owned parkland, forest preserves, or active recreation facilities."
)

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
    # Evaluation Engine with Statutory Precedence, Mixed-Use Guardrails & Type II Exemption Rules
    is_type_i = False
    is_type_ii = False
    reasons = []

    # 1. Type I Threshold Checks (6 NYCRR 617.4)
    if disturbance_acres >= 10.0:
        is_type_i = True
        reasons.append(f"Physical disturbance ({disturbance_acres} acres) meets or exceeds the Type I threshold of 10 acres.")

    if non_res_sqft >= 100000:
        is_type_i = True
        reasons.append(f"Non-residential gross floor area ({non_res_sqft} sq. ft.) meets or exceeds the Type I threshold of 100,000 sq. ft.")

    # 2. Mixed-Use Guardrail: Non-residential footprint >= 4,000 sq ft blocks residential-only Type II exemptions
    mixed_use_triggered = non_res_sqft >= 4000

    if mixed_use_triggered:
        reasons.append(f"Non-residential gross floor area ({non_res_sqft} sq. ft.) meets or exceeds the 4,000 sq. ft. mixed-use guardrail, disqualifying pure residential Type II exemptions.")

    # 3. Overlay / 25% Threshold Checks (Ag District, Historic, Parkland)
    # If unlisted action takes place in/near an overlay and affects >= threshold amounts
    has_overlay_trigger = False
    if involves_ag and disturbance_acres >= 2.5:
        has_overlay_trigger = True
        reasons.append("Project is within an enrolled agricultural district and exceeds the 2.5-acre overlay review threshold.")
    if involves_historic and disturbance_acres >= 1.0:
        has_overlay_trigger = True
        reasons.append("Project is adjacent to a historic resource and exceeds the 1-acre overlay review threshold.")
    if involves_parkland and disturbance_acres >= 1.0:
        has_overlay_trigger = True
        reasons.append("Project is adjacent to public parkland and exceeds the 1-acre overlay review threshold.")

    # 4. Type II Potential Check (e.g., 1-3 single family homes not in an overlay, low disturbance)
    # Type II actions are exempt from further review under SEQRA (6 NYCRR 617.5)
    if not is_type_i and not mixed_use_triggered and not has_overlay_trigger and not involves_zoning_conflict:
        if num_residential_units > 0 and num_residential_units <= 3 and disturbance_acres < 1.0:
            is_type_ii = True
            reasons.append(f"Construction of {num_residential_units} residential unit(s) with minimal disturbance qualifies as a Type II exempt action.")

    # Determine Classification with Statutory Precedence (Type I overrides Type II)
    if is_type_i:
        classification = "Type I Action (Full EAF Required)"
        status_color = "error"
        explanation = "The project triggers one or more Type I thresholds under 6 NYCRR 617.4. Statutory precedence dictates that Type I classifications override potential Type II exemptions. Type I actions require the submission of a Full Environmental Assessment Form (Full EAF)."
    elif is_type_ii:
        classification = "Type II Action (Exempt from Review)"
        status_color = "success"
        explanation = "The project falls under statutory Type II exemption categories (6 NYCRR 617.5) with no significant adverse environmental impacts anticipated. No further review under SEQRA is required."
    elif mixed_use_triggered:
        classification = "Unlisted Action (Subject to Mixed-Use Guardrail)"
        status_color = "warning"
        explanation = "Due to the non-residential square footage exceeding statutory thresholds, standard residential exemptions do not apply. Prepare either a Short EAF or Full EAF for lead agency review."
    else:
        classification = "Unlisted Action"
        status_color = "info"
        explanation = "Preliminary screening completed. Review individual overlay thresholds and local planning board guidelines. Complete the Short Environmental Assessment Form (Short EAF)."

    # Display Results
    if status_color == "error":
        st.error(f"### Classification: {classification}")
    elif status_color == "success":
        st.success(f"### Classification: {classification}")
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
