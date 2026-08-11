"""Run the Phase 2 foil-loading and reference-area demonstration."""

from hydrofoil_designer import (
    PUBLICATION_PRACTICAL_FOIL_LOADING_MAX_KGF_M2,
    PUBLICATION_PRACTICAL_FOIL_LOADING_MIN_KGF_M2,
    FoilAreaResult,
    FoilLoadingScanInputs,
    LoadBalanceInputs,
    calculate_static_load_balance,
    kgf_per_m2_to_n_per_m2,
    scan_foil_loadings,
)


# These positions and the selected publication range are demo/validation inputs.
# They are not a final foil arrangement or a design-point selection for the boat.
DEMO_AFT_FOIL_FROM_STERN_M = 0.750
DEMO_LCG_FROM_STERN_M = 1.987
DEMO_FORE_FOIL_FROM_STERN_M = 3.250


def print_area_point(label: str, point: FoilAreaResult) -> None:
    """Print one endpoint using presentation-only rounding."""

    print(label)
    print(f"  Foil loading       : {point.foil_loading_n_m2:,.3f} N/m²")
    print(f"  Toplam alan        : {point.total_area_m2:.9f} m²")
    print(f"  Ön foil alanı      : {point.fore_area_m2:.9f} m²")
    print(f"  Arka foil alanı    : {point.aft_area_m2:.9f} m²")
    print(f"  Alan residual      : {point.area_sum_residual_m2:.12g} m²")
    print(f"  Toplam kuvvet res. : {point.total_force_residual_n:.12g} N")
    print(f"  Ön kuvvet res.     : {point.fore_force_residual_n:.12g} N")
    print(f"  Arka kuvvet res.   : {point.aft_force_residual_n:.12g} N")


def main() -> None:
    """Calculate and print the Phase 2 validation example."""

    load_balance = calculate_static_load_balance(
        LoadBalanceInputs(
            mass_kg=1299.0,
            lcg_from_stern_m=DEMO_LCG_FROM_STERN_M,
            aft_foil_from_stern_m=DEMO_AFT_FOIL_FROM_STERN_M,
            fore_foil_from_stern_m=DEMO_FORE_FOIL_FROM_STERN_M,
        )
    )
    practical_min_n_m2 = kgf_per_m2_to_n_per_m2(
        PUBLICATION_PRACTICAL_FOIL_LOADING_MIN_KGF_M2
    )
    practical_max_n_m2 = kgf_per_m2_to_n_per_m2(
        PUBLICATION_PRACTICAL_FOIL_LOADING_MAX_KGF_M2
    )
    scan = scan_foil_loadings(
        FoilLoadingScanInputs(
            load_balance=load_balance,
            min_foil_loading_n_m2=practical_min_n_m2,
            max_foil_loading_n_m2=practical_max_n_m2,
            sample_count=2,
        )
    )

    print("UYARI: Aşağıdaki değerler yalnız Faz 2 demo/doğrulama girdileridir.")
    print("Gerçek foil yerleşimi, alanı veya nihai tasarım noktası değildir.")
    print()
    print(f"Toplam ağırlık       : {load_balance.weight_n:,.6f} N")
    print(f"Ön foil yükü         : {load_balance.fore_lift_n:,.6f} N")
    print(f"Arka foil yükü       : {load_balance.aft_lift_n:,.6f} N")
    print(
        "Pratik yayın aralığı : "
        f"{PUBLICATION_PRACTICAL_FOIL_LOADING_MIN_KGF_M2:.0f}-"
        f"{PUBLICATION_PRACTICAL_FOIL_LOADING_MAX_KGF_M2:.0f} kgf/m²"
    )
    print(
        f"SI karşılığı         : {practical_min_n_m2:,.3f}-"
        f"{practical_max_n_m2:,.3f} N/m²"
    )
    print()
    print_area_point("Minimum loading -> maksimum alan", scan.points[0])
    print()
    print_area_point("Maksimum loading -> minimum alan", scan.points[-1])


if __name__ == "__main__":
    main()
