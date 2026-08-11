# Faz 2 doğrulaması

## Doğrulama kapsamı

Faz 2 sonuç nesnesi oluşturulduğunda aşağıdakiler formüllerden bağımsız olarak
yeniden hesaplanır:

- `S_fore + S_aft - S_total`;
- `lambda S_total - W`;
- `lambda S_fore - L_fore`;
- `lambda S_aft - L_aft`;
- ön ve arka alan oranlarının Faz 1 yük oranlarından farkı;
- taramadaki loading artışı ve toplam alanın monoton azalması.

Alan ve kuvvet toleransları IEEE-754 kayan nokta işlemlerindeki son basamak
iptallerini kapsamak için mutlak taban ile ölçeğe bağlı `1e-12` göreli terimin
toplamıdır. Oranlar için `1e-12` mutlak tolerans kullanılır. Çekirdekte
yuvarlama yoktur.

## Demo/doğrulama girdisi

- `mass = 1299 kg`;
- `g = 9.80665 m/s²`;
- `x_A = 0.750 m`;
- `x_G = 1.987 m`;
- `x_F = 3.250 m`;
- seçilen pratik yayın aralığı: `3800-5700 kgf/m²`.

Bu değerler gerçek foil yerleşimi veya nihai tasarım noktası değildir.

## Demo sonuçları

| Sonuç | Minimum loading | Maksimum loading |
|---|---:|---:|
| Loading `[N/m²]` | `37265.270` | `55897.905` |
| Toplam alan `[m²]` | `0.341842105` (maksimum) | `0.227894737` (minimum) |
| Ön alan `[m²]` | `0.169143474` | `0.112762316` |
| Arka alan `[m²]` | `0.172698632` | `0.115132421` |
| Alan residualı `[m²]` | `-2.776e-17` | `0` |
| Üç kuvvet residualı `[N]` | `0` | `0` |

Faz 1 sonuçları: `W = 12738.838350 N`, `L_fore = 6303.177216 N`,
`L_aft = 6435.661134 N`.

## Test sonucu

Python 3.12.13 ve pytest 8.4.2 ile toplam `69` testin tamamı geçmiştir. İlk
`24` Faz 1 testi değişmeden geçmeye devam etmektedir. Testler dönüşümleri,
psi/psf ayrımını, analitik alan örneklerini, Faz 1 entegrasyonunu, residualları,
monoton taramayı, aralık sınırlarını, yanlış türleri, NaN/infinity değerlerini
ve çekirdekte yuvarlama yapılmamasını kapsar.

## Bu fazda uygulanmayanlar

Profil poları, aspect-ratio/free-surface düzeltmeleri, chord/span/dihedral,
surface-piercing ıslak alan geometrisi, kavitasyon, yapısal sınır, optimizasyon,
GUI, CFD ve CAD çıktısı uygulanmamıştır.

