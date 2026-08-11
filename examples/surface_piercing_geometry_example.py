"""Run the Phase 3 surface-piercing geometry demonstration."""

from hydrofoil_designer import (
    FoilAreaInputs,
    LoadBalanceInputs,
    SurfacePiercingVFoilPairInputs,
    calculate_foil_areas,
    calculate_static_load_balance,
    calculate_surface_piercing_v_foil_pair,
    kgf_per_m2_to_n_per_m2,
)


# All arrangement and geometry values below are illustrative demo inputs. They
# are not a selected or final hydrofoil design.
DEMO_AFT_FOIL_FROM_STERN_M = 0.750
DEMO_LCG_FROM_STERN_M = 1.987
DEMO_FORE_FOIL_FROM_STERN_M = 3.250
DEMO_FOIL_LOADING_KGF_M2 = 5000.0


def main() -> None:
    """Run the 1299 kg Phase 1 -> Phase 2 -> Phase 3 demonstration chain."""

    load_balance = calculate_static_load_balance(
        LoadBalanceInputs(
            mass_kg=1299.0,
            lcg_from_stern_m=DEMO_LCG_FROM_STERN_M,
            aft_foil_from_stern_m=DEMO_AFT_FOIL_FROM_STERN_M,
            fore_foil_from_stern_m=DEMO_FORE_FOIL_FROM_STERN_M,
        )
    )
    phase_2 = calculate_foil_areas(
        FoilAreaInputs(
            load_balance=load_balance,
            foil_loading_n_m2=kgf_per_m2_to_n_per_m2(
                DEMO_FOIL_LOADING_KGF_M2
            ),
        )
    )
    phase_3 = calculate_surface_piercing_v_foil_pair(
        SurfacePiercingVFoilPairInputs(
            foil_area_result=phase_2,
            fore_total_developed_span_m=1.60,
            fore_dihedral_deg=35.0,
            fore_apex_submergence_m=0.22,
            aft_total_developed_span_m=1.80,
            aft_dihedral_deg=30.0,
            aft_apex_submergence_m=0.20,
        )
    )

    print("UYARI: Tüm konum, yükleme ve geometri değerleri yalnız demodur.")
    print("Bunlar nihai foil yerleşimi veya seçilmiş bir tasarım değildir.")
    print()
    print("Tekne kütlesi         : 1299.000 kg")
    print(f"Foil loading          : {phase_2.foil_loading_n_m2:,.3f} N/m²")
    print(f"Faz 2 toplam alan     : {phase_2.total_area_m2:.9f} m²")
    print(
        "Faz 2 ön/arka alan    : "
        f"{phase_2.fore_area_m2:.9f} / {phase_2.aft_area_m2:.9f} m²"
    )
    print()
    for label, geometry in (
        ("Ön foil", phase_3.fore_geometry),
        ("Arka foil", phase_3.aft_geometry),
    ):
        print(label)
        print(
            "  Geliştirilmiş açıklık : "
            f"{geometry.total_developed_span_m:.6f} m"
        )
        print(f"  Diyedral               : {geometry.dihedral_deg:.6f} deg")
        print(f"  Apeks batması          : {geometry.apex_submergence_m:.9f} m")
        print(f"  Faz 2 referans alanı   : {geometry.reference_area_m2:.9f} m²")
        print(f"  Ortalama chord         : {geometry.mean_chord_m:.9f} m")
        print(
            "  Düşey foil yüksekliği  : "
            f"{geometry.foil_vertical_height_m:.9f} m"
        )
        print(f"  Islak referans alanı   : {geometry.wetted_area_m2:.9f} m²")
        print(f"  Islak oran             : {geometry.wetted_fraction:.9f}")
        print(
            "  Su hattı genişliği     : "
            f"{geometry.waterline_intersection_width_m:.9f} m"
        )
        print()
    print(
        "Faz 2 -> Faz 3 alan residual : "
        f"{phase_3.pair_area_sum_residual_m2:.12g} m²"
    )
    print(f"İki foil surface-piercing    : {phase_3.is_surface_piercing_pair}")


if __name__ == "__main__":
    main()
