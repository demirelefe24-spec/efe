"""Run a transparent static load-balance demonstration."""

from hydrofoil_designer import LoadBalanceInputs, calculate_static_load_balance


# These foil positions are software test/demo values only. They are not a real
# design decision and must be replaced by the user when the geometry is known.
DEMO_AFT_FOIL_FROM_STERN_M = 0.750
DEMO_FORE_FOIL_FROM_STERN_M = 3.250


def main() -> None:
    """Calculate and print the reference-boat demonstration."""

    inputs = LoadBalanceInputs(
        mass_kg=1299.0,
        lcg_from_stern_m=1.987,
        aft_foil_from_stern_m=DEMO_AFT_FOIL_FROM_STERN_M,
        fore_foil_from_stern_m=DEMO_FORE_FOIL_FROM_STERN_M,
    )
    result = calculate_static_load_balance(inputs)

    print("UYARI: x_A=0.750 m ve x_F=3.250 m yalnız test/demo değerleridir.")
    print("Bunlar gerçek tasarım kararı değildir ve kullanıcı tarafından değiştirilmelidir.")
    print()
    print(f"Toplam ağırlık       : {result.weight_n:,.3f} N")
    print(f"Ön foil kaldırması   : {result.fore_lift_n:,.3f} N")
    print(f"Arka foil kaldırması : {result.aft_lift_n:,.3f} N")
    print(f"Ön yük payı          : {result.fore_load_percent:.3f} %")
    print(f"Arka yük payı        : {result.aft_load_percent:.3f} %")
    print(f"Kuvvet residual      : {result.vertical_force_residual_n:.12g} N")
    print(f"Moment residual      : {result.moment_residual_nm:.12g} N m")


if __name__ == "__main__":
    main()

