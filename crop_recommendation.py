# ============================================================
# KISANAI CROP RECOMMENDATION
# ============================================================

def recommend_crops(
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    rainfall,
    soil_type
):

    recommendations = []

    # --------------------------------------------------------
    # RICE
    # --------------------------------------------------------

    if (
        rainfall > 150
        and humidity > 60
        and temperature > 20
    ):

        recommendations.append(
            (
                "Rice",
                "High suitability because of suitable rainfall, humidity and temperature."
            )
        )


    # --------------------------------------------------------
    # COTTON
    # --------------------------------------------------------

    if (
        temperature > 22
        and 50 < rainfall < 150
    ):

        recommendations.append(
            (
                "Cotton",
                "Good suitability for the given temperature and rainfall."
            )
        )


    # --------------------------------------------------------
    # MAIZE
    # --------------------------------------------------------

    if (
        18 <= temperature <= 30
        and 50 <= rainfall <= 120
    ):

        recommendations.append(
            (
                "Maize",
                "Good suitability for the given climate conditions."
            )
        )


    # --------------------------------------------------------
    # GROUNDNUT
    # --------------------------------------------------------

    if (
        temperature > 20
        and 50 <= rainfall <= 100
    ):

        recommendations.append(
            (
                "Groundnut",
                "Suitable under warm conditions with moderate rainfall."
            )
        )


    # --------------------------------------------------------
    # WHEAT
    # --------------------------------------------------------

    if (
        10 <= temperature <= 25
        and rainfall < 100
    ):

        recommendations.append(
            (
                "Wheat",
                "Suitable under cooler conditions and lower rainfall."
            )
        )


    # --------------------------------------------------------
    # PULSES
    # --------------------------------------------------------

    if (
        nitrogen < 60
        and rainfall < 120
    ):

        recommendations.append(
            (
                "Pulses",
                "Suitable option for relatively lower nitrogen soil."
            )
        )


    # --------------------------------------------------------
    # SOIL BASED RECOMMENDATION
    # --------------------------------------------------------

    if soil_type == "Black Soil":

        recommendations.append(
            (
                "Cotton",
                "Black soil is generally suitable for cotton."
            )
        )

    elif soil_type == "Alluvial Soil":

        recommendations.append(
            (
                "Rice",
                "Alluvial soil can support rice cultivation."
            )
        )

    elif soil_type == "Red Soil":

        recommendations.append(
            (
                "Groundnut",
                "Groundnut can be a suitable option for red soil."
            )
        )


    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    unique = []

    for crop, reason in recommendations:

        already_exists = False

        for existing_crop, existing_reason in unique:

            if existing_crop == crop:

                already_exists = True
                break

        if not already_exists:

            unique.append(
                (
                    crop,
                    reason
                )
            )


    return unique