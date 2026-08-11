# Birimler ve sözleşmeler

## Kanonik iç birimler

Hesap çekirdeğinin kanonik sistemi SI'dır:

| Büyüklük | Birim |
|---|---|
| Kütle | `kg` |
| Kuvvet/ağırlık/kaldırma | `N` |
| Uzunluk | `m` |
| Alan | `m²` |
| Moment | `N m` |
| Foil loading | `N/m² = Pa` |
| Hız | `m/s` |

Foil loading `W/S`, bir referans alanı başına kuvvettir. Dynamic pressure da
pascal birimini kullanabilir; aynı birim bu iki büyüklüğü fiziksel olarak aynı
yapmaz.

## Dönüşüm sabitleri

Tek kaynak `constants.py`, test edilebilir fonksiyonlar `units.py` içindedir:

- `1 kgf = 9.80665 N`;
- `1 lbf = 4.4482216152605 N`;
- `1 ft = 0.3048 m`;
- `1 in = 0.0254 m`;
- `1 nmi = 1852 m`;
- `1 knot = 1852/3600 m/s`;
- `1 psf = 47.88025898033584 Pa`;
- `1 psi = 6894.757293168361 Pa = 144 psf`.

Fonksiyon isimleri giriş ve çıkış birimlerini taşır:

- `kgf_to_n`;
- `kgf_per_m2_to_n_per_m2`;
- `psf_to_pa`;
- `psi_to_pa`;
- `knots_to_m_s`.

Fonksiyonlar NaN, infinity, bool ve sayı olmayan türleri reddeder.

## Yayın aralıkları

| Yayın sınıfı | Legacy aralık | SI aralık |
|---|---:|---:|
| Genel program/tarama | `3000-7000 kgf/m²` | `29419.950-68646.550 N/m²` |
| Önerilen/pratik | `3800-5700 kgf/m²` | `37265.270-55897.905 N/m²` |

Bu aralıklar ayrı isimli sabitlerdir, fakat hesap fonksiyonlarında gizli
varsayılan değildir. Kullanıcı veya örnek açıkça seçim yapmalıdır.

Pratik aralığın diğer birimleri:

- `778.301-1167.452 psf`;
- `5.40487-8.10731 psi`.

Dolayısıyla yayınlardaki `800-1200 PSI` ifadesi hesaplarda kullanılmaz ve
muhtemel `PSF` dizgi hatası olarak korunur.

