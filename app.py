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

st.subheader("3. Specific Type II Statutory Exemption Categories")
st.caption("💡 *Note: Check any box that explicitly describes your proposed action.*")

type2_maint_repair = st.checkbox(
    "Maintenance, repair, routine replacement of existing structures in-kind, code upgrades, or green infrastructure retrofits",
    help="Routine maintenance, in-kind reconstruction, or energy/fire code upgrades without exceeding Type I thresholds."
)

type2_ag_ops = st.checkbox(
    "Agricultural farm management practices, farm buildings, structures, and allowable land use changes",
    help="Standard agricultural farm management practices, farm structures, silos, and barns on a farm operation."
)

type2_infrastructure = st.checkbox(
    "Highway repaving (no new lanes), utility line repairs/openings, or trenchless/aerial telecom cables in existing rights-of-way",
    help="Repaving existing roads without new lanes, utility opening repairs, or utility right-of-way cable placement."
)

type2_minor_nonres = st.checkbox(
    "Construction or expansion of a primary or accessory non-residential structure under 4,000 sq. ft.",
    help="Primary or accessory non-residential structures involving less than 4,000 sq. ft. of gross floor area."
)

type2_edu_routine = st.checkbox(
    "Routine activities of educational institutions or facility expansions under 10,000 sq. ft.",
    help="Routine school activities or minor expansions under 10,000 sq. ft. (excluding closures with use changes)."
)

type2_1to3_family = st.checkbox(
    "Construction of 1, 2, or 3-family residential structures, minor accessory structures, or utility connections",
    help="Single, double, or triple-family homes, garages, decks, pools, fences, or utility extensions on approved lots."
)

type2_solar_disturbed = st.checkbox(
    "Solar energy arrays (25 acres or less) on closed landfills, brownfields, wastewater plants, industrial sites, or parking lots",
    help="Solar installations up to 25 acres of physical alteration on designated disturbed or brownfield locations."
)

type2_solar_roof = st.checkbox(
    "Solar energy arrays installed on an existing structure (not listed or eligible for historic registers)",
    help="Rooftop solar arrays on structures not listed or eligible for historic registers."
)

type2_variances_reuse = st.checkbox(
    "Granting of setback/area variances for 1-3 family homes, or permitted reuse of existing residential/commercial structures",
    help="Individual setback, lot line, or residential area variances, or reuse of compliant residential/commercial structures."
)

type2_planning_admin = st.checkbox(
    "Routine agency administration, planning referrals (GML 239-m/n), ministerial permits, or silviculture under 10 acres",
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

with st.expander("ℹ️ What does 'inconsistency with local land use controls' mean
