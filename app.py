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
    help="Total square footage of new construction or building expansion for non-residential primary or accessory structures."
)

num_residential_units = st.number_input(
    "Number of residential units proposed",
    min_value=0,
    step=1,
    help="Total number of new dwelling units proposed."
)

unsewered_water_sewer = st.checkbox(
    "Residential units will NOT connect to existing public/community water and sewer systems at habitation",
    help="Triggers Type I review at 50 or more residential units under 6 NYCRR 617.4(b)(5)(ii)."
)

parking_spaces = st.number_input(
    "Number of parking spaces proposed",
    min_value=0,
    step=10,
    help="Total number of vehicle parking spaces included in the project design."
)

water_gpd = st.number_input(
    "Estimated water usage (gallons per day)",
    min_value=0.0,
    step=1000.0,
    help="Projected daily ground or surface water withdrawal or consumption."
)

st.subheader("2. Agency, Policy & Zoning Actions")
st.caption("💡 *Note: Select any agency-sponsored policy action or zoning amendment that applies.*")

type1_comp_plan = st.checkbox(
    "Adoption of a municipal land use plan, comprehensive resource management plan, or initial zoning regulations",
    help="Type I Action under 6 NYCRR 617.4(b)(1)."
)

zoning_change_acres = st.number_input(
    "Zoning district change / allowable use changes (affected area in acres)",
    min_value=0.0,
    step=1.0,
    help="Triggers Type I classification if changes in allowable uses within a zoning district affect 25 or more acres (6 NYCRR 617.4(b)(2))."
)

land_transfer_acres = st.number_input(
    "Public agency land acquisition, sale, lease, annexation, or transfer (in contiguous acres)",
    min_value=0.0,
    step=5.0,
    help="Triggers Type I classification if the transfer involves 100 or more contiguous acres of land by a State or local agency (6 NYCRR 617.4(b)(4))."
)

st.subheader("3. Comprehensive Type II Statutory Exemption Categories (6 NYCRR 617.5(c))")
st.caption("💡 *Note: Check any category below that explicitly describes your proposed action.*")

type2_maint_repair = st.checkbox(
    "(c)(1)-(2) Maintenance, in-kind replacement, rehabilitation, reconstruction, code upgrades, or green infrastructure retrofits",
    help="Routine maintenance, in-kind reconstruction, or energy/fire code upgrades without exceeding Type I thresholds."
)

type2_ag_ops = st.checkbox(
    "(c)(3) Agricultural farm management practices, farm buildings, structures, and allowable land use changes",
    help="Standard agricultural farm management practices, farm structures, silos, and barns on a farm operation."
)

type2_infrastructure = st.checkbox(
    "(c)(4)-(7) Highway repaving, utility maintenance/openings, trenchless/aerial telecom cables",
    help="Repaving existing roads without new lanes, utility opening repairs, or utility right-of-way cable placement."
)

type2_minor_nonres = st.checkbox(
    "(c)(9) Non-residential construction/expansion under 4,000 sq. ft. consistent with zoning/land use controls",
    help="Primary or accessory non-residential structures involving less than 4,000 sq. ft. of gross floor area."
)

type2_edu_routine = st.checkbox(
    "(c)(10) Routine educational institution activities or facility expansions under 10,000 sq. ft.",
    help="Routine school activities or minor expansions under 10,000 sq. ft. (excluding closures with use changes)."
)

type2_1to3_family = st.checkbox(
    "(c)(11)-(12) Construction of 1, 2, or 3-family residences, minor accessory structures, & utility extensions",
    help="Single, double, or triple-family homes, garages, decks, pools, fences, or utility extensions on approved lots."
)

type2_solar_disturbed = st.checkbox(
    "(c)(14) Solar energy arrays (<= 25 acres) on closed landfills, brownfields, WWTPs, industrial sites, or parking lots",
    help="Solar installations up to 25 acres of physical alteration on designated disturbed or brownfield locations."
)

type2_solar_roof = st.checkbox(
    "(c)(15) Solar energy arrays on an existing structure (outside historic registers/districts)",
    help="Rooftop solar arrays on structures not listed or eligible for historic registers."
)

type2_variances_reuse = st.checkbox(
    "(c)(16)-(18) Setback/area variances for 1-3 family homes or permitted building reuses",
    help="Individual setback, lot line, or residential area variances, or reuse of compliant residential/commercial structures."
)

type2_planning_admin = st.checkbox(
    "(c)(19)-(43) General planning, GML 239 referrals, silviculture (<10 acres), ministerial permits, admin & enforcement",
    help="County GML 239-m/n reviews, minor forestry, ministerial building permits, enforcement, and routine administration."
)

st.subheader("4. Project Characteristics & Environmental Overlays")
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
st.subheader("5. Environmental Review Determination")

if st.button("Run SEQRA Evaluation", type="primary"):
    is_type_i = False
    is_type_ii = False
    reasons = []

    # 1. Policy & Agency Type I Triggers (6 NYCRR 617.4(b))
    if type1_comp_plan:
        is_type_i = True
        reasons.append("Adoption of a municipal land use plan, comprehensive management plan, or initial zoning code is a Type I action under 617.4(b)(1).")

    if zoning_change_acres >= 25.0:
        is_type_i = True
        reasons.append(f"Zoning map or text amendment affecting allowable uses across {zoning_change_acres} acres meets or exceeds the Type I threshold of 25 acres under 617.4(b)(2).")

    if land_transfer_acres >= 100.0:
        is_type_i = True
        reasons.append(f"Public agency land transfer/annexation involving {land_transfer_acres} contiguous acres meets or exceeds the Type I threshold of 100 acres under 617.4(b)(4).")

    # 2. Residential Threshold Checks (6 NYCRR 617.4(b)(5))
    if unsewered_water_sewer and num_residential_units >= 50:
        is_type_i = True
        reasons.append(f"Unsewered residential development ({num_residential_units} units) meets or exceeds the Type I threshold of 50 units under 617.4(b)(5)(ii).")
    elif not unsewered_water_sewer and num_residential_units >= 200:
        is_type_i = True
        reasons.append(f"Sewered residential unit count ({num_residential_units}) meets or exceeds the Type I threshold of 200 units for municipalities under 150,000 population under 617.4(b)(5)(iii).")

    # 3. Commercial & Physical Scale Type I Triggers (6 NYCRR 617.4(b)(6))
    if disturbance_acres >= 10.0:
        is_type_i = True
        reasons.append(f"Physical disturbance ({disturbance_acres} acres) meets or exceeds the Type I threshold of 10 acres.")

    if water_gpd >= 2000000.0:
        is_type_i = True
        reasons.append(f"Water usage ({water_gpd:,.0f} gallons/day) meets or exceeds the Type I threshold of 2,000,000 gpd.")

    if parking_spaces >= 500:
        is_type_i = True
        reasons.append(f"Proposed parking spaces ({parking_spaces}) meet or exceed the Type I threshold of 500 vehicles for municipalities under 150,000 population.")

    if non_res_sqft >= 100000:
        is_type_i = True
        reasons.append(f"Non-residential gross floor area ({non_res_sqft:,} sq. ft.) meets or exceeds the Type I threshold of 100,000 sq. ft. for municipalities under 150,000 population.")

    # 4. 25% Threshold Rules for Overlays (6 NYCRR 617.4(b)(8), (9), (10))
    overlay_25_pct_triggered = False
    overlay_reasons = []

    is_exceeding_25_pct = (
        disturbance_acres >= 2.5 or
        non_res_sqft >= 25000 or
        parking_spaces >= 125 or
        num_residential_units >= 50
    )

    if is_exceeding_25_pct:
        if involves_ag:
            overlay_25_pct_triggered = True
            overlay_reasons.append("Project has non-agricultural use within an enrolled agricultural district and meets or exceeds 25% of a Type I threshold (617.4(b)(8)).")
        if involves_historic:
            overlay_25_pct_triggered = True
            overlay_reasons.append("Project is within/adjacent to a historic resource and meets or exceeds 25% of a Type I threshold (617.4(b)(9)).")
        if involves_parkland:
            overlay_25_pct_triggered = True
            overlay_reasons.append("Project is within/adjacent to public parkland and meets or exceeds 25% of a Type I threshold (617.4(b)(10)).")

    if overlay_25_pct_triggered:
        is_type_i = True
        reasons.extend(overlay_reasons)

    # 5. Mixed-Use Guardrail
    mixed_use_triggered = non_res_sqft >= 4000

    if mixed_use_triggered and not type2_ag_ops:
        reasons.append(f"Non-residential gross floor area ({non_res_sqft:,} sq. ft.) meets or exceeds the 4,000 sq. ft. mixed-use guardrail, disqualifying pure residential/accessory Type II exemptions.")

    # 6. Comprehensive Type II Exemption Evaluation
    type2_checked = any([
        type2_maint_repair, type2_ag_ops, type2_infrastructure, type2_minor_nonres,
        type2_edu_routine, type2_1to3_family, type2_solar_disturbed, type2_solar_roof,
        type2_variances_reuse, type2_planning_admin
    ]) or (0 < non_res_sqft < 4000)

    if type2_checked and not is_type_i and not involves_zoning_conflict:
        if mixed_use_triggered and not type2_ag_ops:
            is_type_ii = False  # Blocked by mixed-use guardrail
        else:
            is_type_ii = True
            if type2_maint_repair:
                reasons.append("Qualifies under Type II 6 NYCRR 617.5(c)(1)-(2): Maintenance, in-kind replacement, or code/green infrastructure upgrades.")
            if type2_ag_ops or (0 < non_res_sqft < 4000 and type2_ag_ops):
                reasons.append("Qualifies under Type II 6 NYCRR 617.5(c)(3): Agricultural farm management practices and structures.")
            if type2_infrastructure:
                reasons.append("Qualifies under Type II 6 NYCRR 617.5(c)(4)-(7): Routine utility, highway, or telecommunication infrastructure maintenance.")
            if type2_minor_nonres or (0 < non_res_sqft < 4000):
                reasons.append(f"Qualifies under Type II 6 NYCRR 617.5(c)(9): Non-residential structure/expansion ({non_res_sqft:,} sq. ft.) is under 4,000 sq. ft.")
            if type2_edu_routine:
                reasons.append("Qualifies under Type II 6 NYCRR 617.5(c)(10): Routine educational institution activity or minor expansion under 10,000 sq. ft.")
            if type2_1to3_family:
                reasons.append("Qualifies under Type II 6 NYCRR 617.5(c)(11)-(13): Residential construction of 1-3 units, accessory structures, or utility extensions.")
            if type2_solar_disturbed:
                reasons.append("Qualifies under Type II 6 NYCRR 617.5(c)(14): Solar energy array (<= 25 acres) on a qualified disturbed/brownfield/industrial site.")
            if type2_solar_roof:
                reasons.append("Qualifies under Type II 6 NYCRR 617.5(c)(15): Rooftop solar energy installation on a non-historic structure.")
            if type2_variances_reuse:
                reasons.append("Qualifies under Type II 6 NYCRR 617.5(c)(16)-(18): Area/setback variances or compliant building/structure reuses.")
            if type2_planning_admin:
                reasons.append("Qualifies under Type II 6 NYCRR 617.5(c)(19)-(43): General planning, GML 239 referrals, ministerial permits, or routine agency administration.")

    # Determine Classification with Statutory Precedence (Type I > Type II > Unlisted)
    if is_type_i:
        classification = "Type I Action (Full EAF Required)"
        status_color = "error"
        explanation = "The project triggers one or more Type I thresholds under 6 NYCRR 617.4 (including major project scale, agency policy thresholds, or the 25% overlay rules). Statutory precedence dictates that Type I classifications override potential Type II exemptions. Type I actions require the submission of a Full Environmental Assessment Form (Full EAF)."
    elif is_type_ii:
        classification = "Type II Action (Exempt from Review)"
        status_color = "success"
        explanation = "The project falls under statutory Type II exemption categories (6 NYCRR 617.5) with no significant adverse environmental impacts anticipated. No further review under SEQRA is required."
    elif mixed_use_triggered:
        classification = "Unlisted Action (Subject to Mixed-Use Guardrail)"
        status_color = "warning"
        explanation = "Due to non-residential square footage meeting or exceeding statutory thresholds, standard residential exemptions do not apply. Prepare either a Short EAF or Full EAF for lead agency review."
    else:
        classification = "Unlisted Action"
        status_color = "info"
        explanation = "Preliminary screening completed. The action is neither explicitly Type I nor exempt Type II. Complete the Short Environmental Assessment Form (Short EAF) for lead agency evaluation."

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
        st.markdown("**Trigger & Classification Factors Identified:**")
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
