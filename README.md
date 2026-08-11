# hydrofoil-designer

`hydrofoil-designer`, hydrofoil teknelerin ön boyutlandırmasını kaynaklara kadar
izlenebilir ve test edilebilir bir hesap çekirdeğiyle gerçekleştirmeyi amaçlayan
bir bilimsel Python projesidir. Uzun vadeli hedef, surface-piercing foil tasarımını
da kapsayan ve Windows uygulaması olarak dağıtılabilen bir masaüstü aracıdır.

## Mevcut kapsam

Sürüm `0.2.0` Faz 0, Faz 1 ve Faz 2'yi kapsar:

- iki ana kaynağın yöntem, denklem, birim ve belirsizlik haritası;
- tekne kütlesinden SI biriminde ağırlık hesabı;
- normal `x_A < x_G < x_F` yerleşiminde ön ve arka foil statik yük paylaşımı;
- düşey kuvvet ve LCG etrafında moment residual kontrolleri;
- kuvvet tabanlı `W/S` foil loading hesabı ve birim dönüşümleri;
- ortak loading altında toplam, ön ve arka foil referans alanları;
- kullanıcı tarafından açıkça seçilen loading aralığında deterministik tarama;
- alan toplamı, loading-kuvvet ve alan/yük oranı residual kontrolleri;
- açık girdi doğrulaması, birim testleri ve bir demo programı.

Hesap çekirdeği kullanıcı arayüzünden bağımsızdır ve terminal çıktısı üretmez.

## Birim ve koordinat sistemi

- Bütün çekirdek hesapları SI birimleriyle yapılır: kg, m, s, N ve N m.
- Faz 2'de `W/S`, kuvvet tabanlı foil loading'dir ve kanonik birimi
  `N/m² = Pa` olarak saklanır. Aynı birimi kullanan dinamik basınçla aynı
  fiziksel büyüklük değildir.
- Boyuna orijin kıç referansıdır; pozitif `x` kıçtan başa doğrudur.
- Pozitif foil kaldırması yukarı yönlüdür.
- `x_A`: arka foil kaldırma merkezinin kıçtan konumu.
- `x_G`: LCG'nin kıçtan konumu.
- `x_F`: ön foil kaldırma merkezinin kıçtan konumu.
- Bu sürüm yalnız `x_A < x_G < x_F` normal yerleşimini kabul eder; foil adlarını
  otomatik olarak değiştirmez.

Yayınlardaki `kgf/m²` değerleri `1 kgf = 9.80665 N` sözleşmesiyle açıkça SI'ya
dönüştürülür. Yayınların `800-1200 PSI` etiketi hesaplarda kullanılmaz; sayılar
yaklaşık `778-1167 psf` ile uyumludur. Ayrıntılar
[docs/units_and_conventions.md](docs/units_and_conventions.md) içindedir.

## Kurulum

Python 3.11 veya daha yeni bir sürüm gerekir. PowerShell örneği:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -e ".[test]"
```

Çalışma zamanı için standart kütüphane dışında bağımlılık yoktur. `pytest`
yalnız test ek bağımlılığıdır.

## Testler

```powershell
.venv\Scripts\python -m pytest
```

Test toleransları isimlendirilmiş sabitlerdir; hesap çekirdeğinde yuvarlama
yapılmaz. Sürüm 0.2.0 doğrulamasında 69 test geçmektedir.

## Örnek kullanım

```powershell
.venv\Scripts\python examples\load_balance_example.py
.venv\Scripts\python examples\foil_loading_example.py
```

Örnek, `1299 kg`, `x_G = 1.987 m`, `x_A = 0.750 m` ve `x_F = 3.250 m`
kullanır. Son iki konum yalnız yazılım testi/demosu içindir; gerçek tasarım
kararı değildir ve kullanıcı tarafından değiştirilmelidir.

Kütüphane kullanımı:

```python
from hydrofoil_designer import LoadBalanceInputs, calculate_static_load_balance

inputs = LoadBalanceInputs(
    mass_kg=1299.0,
    lcg_from_stern_m=1.987,
    aft_foil_from_stern_m=0.750,   # demo only
    fore_foil_from_stern_m=3.250,  # demo only
)
result = calculate_static_load_balance(inputs)
```

Faz 2 alan hesabı, Faz 1 sonucunu doğrudan yeniden kullanır:

```python
from hydrofoil_designer import (
    FoilAreaInputs,
    calculate_foil_areas,
    kgf_per_m2_to_n_per_m2,
)

area_result = calculate_foil_areas(
    FoilAreaInputs(
        load_balance=result,
        foil_loading_n_m2=kgf_per_m2_to_n_per_m2(3800.0),
    )
)
```

Ön ve arka foil için aynı loading kullanılır. Loading sınırları zorunlu kullanıcı
girdileridir; genel veya pratik yayın aralığı gizli varsayılan değildir.

## Henüz desteklenmeyen özellikler

Kord, span ve V-foil geometrisi; hızla değişen surface-piercing ıslak alanı;
hidrodinamik çalışma noktası; hücum açısı; aspect-ratio ve serbest yüzey
düzeltmeleri; stall,
yapısal kalınlık ve kavitasyon sınırları; kalkış, direnç ve güç analizi; profil
veri tabanı; grafikler; GUI; proje dosyası; CSV/rapor; `.exe`; CFD, FEA,
optimizasyon, 3B geometri ve CAD aktarımı uygulanmamıştır.

## Belgeler

- [Yöntem ve kaynak izlenebilirliği](docs/methodology.md)
- [Kabuller](docs/assumptions.md)
- [Birimler ve sözleşmeler](docs/units_and_conventions.md)
- [Faz 2 doğrulaması](docs/phase_2_validation.md)
- [Yol haritası](docs/roadmap.md)
- [Yerel referans dosyaları](references/README.md)

## Ana kaynaklar

1. Schachter, R. D. ve Fonteles, G. T. (2022), "Preliminary design
   dimensioning of hydrofoil boats with fully submerged and surface piercing
   foils", *Marine Systems & Ocean Technology*, 17, 53-69.
   <https://doi.org/10.1007/s40868-022-00113-2>
2. Schachter, R. D. ve Fonteles, G. T. (2020), "Development of a Computer
   Program for the Dimensioning of Hydrofoil Boats with Fully Submerged Foils -
   HYDROFOIL BOAT", 28th SOBENA congress proceedings.
