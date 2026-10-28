import streamlit as st

# Page Configuration
st.set_page_config(page_title="Genesee County SEQRA Decision Tool", layout="centered")

st.title("NY SEQRA Classification Tool")
st.markdown("**6 NYCRR Part 617 Decision Support System** (Optimized for Genesee County, NY)")
st.divider()

# --- INPUT PARAMETERS ---
st.subheader("Step 1: Project Parameters")

acreage = st.number_input("Total physical disturbance area (acres)", min_value=0.0, value=0.0, step=0.1)
non_res_sqft = st.number_input("Non-residential gross floor area (sq. ft.)", min_value=0, value=0, step=100)
res_units = st.number_input("Number of new residential units", min_value=0, value=0, step=1)

# Dynamic Check for Small Non-Residential (617.5(c)(9))
non_res_variance = False
if 0 < non_res_sqft < 4000:
    st.info("ℹ️ **Small Non-Residential Structure Detected (< 4,000 sq. ft.)**")
    non_res_variance = st.checkbox("Does this action involve a change in zoning, a use variance, or inconsistency with local land use controls?")
elif non_res_sqft >= 4000:
    st.warning("⚠️ **Substantial Non-Residential Footprint (>= 4,000 sq. ft.) Detected:** Exceeds the small commercial Type II threshold (`617.5(c)(9)`). Mixed-use buildings with this commercial scale do not qualify for standard residential Type II exemptions.")

st.markdown("---")
st.markdown("#### General Exemptions & Contextual Triggers")

col1, col2 = st.columns(2)
with col1:
    is_maintenance = st.checkbox("Routine maintenance or repair [6 NYCRR 617.5(c)(1)]")
    is_single_family = st.checkbox("Construction of 1-, 2-, or 3-family residences [6 NYCRR 617.5(c)(11)]")
with col2:
    is_replacement = st.checkbox("Replacement or rehabilitation in-kind [6 NYCRR 617.5(c)(2)]")
    is_emergency = st.checkbox("Emergency action to protect life/property [6 NYCRR 617.5(c)(33)]")

st.markdown("#### Spatial & Environmental Overlays")
is_near_historic = st.checkbox("Contiguous to a State/National Register Historic Site or District [6 NYCRR 617.4(b)(9)]")
is_near_park = st.checkbox("Contiguous to public parkland or recreation area [6 NYCRR 617.4(b)(10)]")
in_ag_district = st.checkbox("Located within a Certified Agricultural District [6 NYCRR 617.4(b)(8)]")

st.divider()

# --- UNIFIED EVALUATION ENGINE ---
if st.button("Evaluate SEQRA Classification", type="primary"):
    
    # Helper to check if project exceeds 25% of any primary Type I threshold
    exceeds_25_percent_threshold = (
        acreage > 2.5 or 
        non_res_sqft > 25000 or 
        res_units >= 13
    )

    # 1. Gather all Type I Triggers
    type_i_triggers = []

    if acreage > 10.0:
        type_i_triggers.append(f"Physical disturbance ({acreage} acres) exceeds the 10-acre Type I threshold [**6 NYCRR 617.4(b)(6)(i)**]")
    
    if non_res_sqft > 100000:
        type_i_triggers.append(f"Non-residential floor area ({non_res_sqft:,} sq. ft.) exceeds 100,000 sq. ft. in a municipality under 150k population [**6 NYCRR 617.4(b)(6)(iv)**]")
        
    if res_units >= 50:
        type_i_triggers.append(f"New residential units ({res_units}) meet or exceed major threshold criteria [**6 NYCRR 617.4(b)(5)**]")

    if in_ag_district and exceeds_25_percent_threshold:
        type_i_triggers.append("Non-agricultural use within an Agricultural District exceeding 25% of a Type I threshold [**6 NYCRR 617.4(b)(8)**]")

    if is_near_historic and exceeds_25_percent_threshold:
        type_i_triggers.append("Action contiguous to a historic property/district AND exceeds 25% of a Type I threshold [**6 NYCRR 617.4(b)(9)**]")

    if is_near_park and exceeds_25_percent_threshold:
        type_i_triggers.append("Action contiguous to public parkland/recreation area AND exceeds 25% of a Type I threshold [**6 NYCRR 617.4(b)(10)**]")

    # 2. Gather all Type II Exemptions (with mixed-use guardrails)
    type_ii_matches = []

    if is_maintenance:
        type_ii_matches.append("Routine maintenance or repair [**6 NYCRR 617.5(c)(1)**]")
    if is_replacement:
        type_ii_matches.append("Replacement or rehabilitation in-kind [**6 NYCRR 617.5(c)(2)**]")
    
    # Guardrail: Residential exemption ONLY applies if non-residential space is under 4,000 sq. ft.
    if is_single_family:
        if non_res_sqft < 4000:
            type_ii_matches.append("Construction of 1-, 2-, or 3-family residences [**6 NYCRR 617.5(c)(11)**]")
        else:
            type_ii_matches.append("⚠️ *Residential exemption disqualified: Non-residential footprint (>= 4,000 sq. ft.) indicates a mixed-use/commercial building rather than a pure 1-3 family home.*")

    if is_emergency:
        type_ii_matches.append("Emergency action to protect life/property [**6 NYCRR 617.5(c)(33)**]")
    
    if 0 < non_res_sqft < 4000 and not non_res_variance:
        type_ii_matches.append(f"Non-residential structure ({non_res_sqft} sq. ft.) under 4,000 sq. ft. consistent with local controls [**6 NYCRR 617.5(c)(9)**]")

    # Filter out warning notes from actual valid exemptions for final determination
    valid_type_ii_matches = [m for m in type_ii_matches if "⚠️" not in m]

    # 3. Holistic Determination & Precedence Resolution
    st.subheader("Evaluation Summary & Analysis")

    if type_i_triggers:
        st.markdown(f"🔴 **Type I Triggers Detected ({len(type_i_triggers)}):**")
        for t in type_i_triggers:
            st.markdown(f"- {t}")
    else:
        st.markdown("🟢 **Type I Triggers Detected:** None")

    if type_ii_matches:
        st.markdown(f"🔵 **Type II Exemptions / Notes Evaluated ({len(type_ii_matches)}):**")
        for m in type_ii_matches:
            st.markdown(f"- {m}")
    else:
        st.markdown("⚪ **Type II Exemptions Matched:** None")

    st.markdown("---")

    # Final Classification Logic
    if type_i_triggers:
        st.warning("### Final Classification: TYPE I ACTION")
        st.markdown("This action triggers **Type I** review criteria under **6 NYCRR 617.4**.")
        if valid_type_ii_matches:
            st.caption("⚠️ Note: Type I thresholds supersede and override Type II exemptions.")
        st.markdown("**Required Action:** Coordinated Review and Full EAF are required.")
        
    elif valid_type_ii_matches:
        st.error("### Final Classification: TYPE II ACTION")
        st.markdown("This action is exempt under **6 NYCRR 617.5**. No further SEQRA review is required.")
        st.markdown(f"**Matched Exemption:** {valid_type_ii_matches[0]}")
        
    else:
        st.success("### Final Classification: UNLISTED ACTION")
        st.markdown("This action does not meet Type I thresholds (`6 NYCRR 617.4`) and does not qualify for a valid Type II exemption (`6 NYCRR 617.5`). It is classified as an **Unlisted Action**.")
        if non_res_sqft >= 4000 and is_single_family:
            st.caption("ℹ️ *Mixed-use logic note:* Because the non-residential area is 4,000+ sq. ft., it cannot use the residential Type II exemption, correctly resulting in an Unlisted classification.")
        st.markdown("You may proceed with filing a **Short Environmental Assessment Form (Short EAF)** or Full EAF.")
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
