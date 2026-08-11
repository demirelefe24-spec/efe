# Faz 3 doğrulaması

## Doğrulama yaklaşımı

Faz 3 hesapları oluşturulduktan sonra girdi denklemlerinden bağımsız bir
doğrulama geçişi çalışır. Bu geçiş:

- bütün reel girdilerde `bool`, yanlış tür, NaN ve infinity değerlerini reddeder;
- pozitif alan/açıklık ile `0 < Gamma < 90 deg` sınırlarını denetler;
- `0 < d < h_f` gerçek surface-piercing koşulunu denetler;
- bütün temel uzunlukları, alanları ve oranları yeniden hesaplar;
- kuru/referans alan, ıslak alan ve düşey yükseklik residuallarını denetler;
- Faz 2 alan sonucu içindeki alan toplamını, oranları ve saklanan residualları
  kendi alanlarından kontrol eder;
- ön/arka alanların Faz 2'den Faz 3'e değiştirilmeden aktarıldığını doğrular.

Faz 3, yalnız `FoilAreaResult` içinden geri kazanılabilen Faz 2 tutarlılığını
kontrol eder. Faz 1 girdilerini tekrar istemez ve yük/alan hesabını yeniden
çalıştırmaz.

## Analitik test örneği

Bağımsız el hesabı için seçilen değerler:

- `S_ref = 0.4 m²`;
- `b_dev = 2.0 m`;
- `Gamma = 30 deg`;
- `d = 0.25 m`.

Beklenen sonuçlar:

| Büyüklük | Beklenen değer |
|---|---:|
| Tek panel uzunluğu | `1.0 m` |
| Ortalama kord | `0.2 m` |
| Düşey foil yüksekliği | `0.5 m` |
| Yatay izdüşümlü açıklık | `sqrt(3) m` |
| Islak panel uzunluğu | `0.5 m` |
| Toplam ıslak alan | `0.2 m²` |
| Islak oran | `0.5` |
| Su dışındaki panel uzunluğu | `0.5 m` |
| Emerged uç yüksekliği | `0.25 m` |
| Su hattı kesişim genişliği | `sqrt(3)/2 m` |

## Entegrasyon demosu

Demo zinciri Faz 1'deki `1299 kg`, `x_A = 0.750 m`, `x_G = 1.987 m`,
`x_F = 3.250 m` değerlerini; Faz 2'de açıkça seçilmiş `5000 kgf/m²` loading'i;
Faz 3'te ise aşağıdaki örnek geometrileri kullanır:

| Girdi | Ön foil | Arka foil |
|---|---:|---:|
| Geliştirilmiş toplam açıklık | `1.60 m` | `1.80 m` |
| Diyedral | `35 deg` | `30 deg` |
| Apeks batması | `0.22 m` | `0.20 m` |

Bu değerler yalnız yazılım demosudur; seçilmiş veya nihai tasarım değildir.
Faz 2 alanları `0.128549040 m²` ve `0.131250960 m²` olarak değiştirilmeden
aktarılır. İki Faz 3 referans alanının toplamı ile Faz 2 toplam alanı arasındaki
demo residualı yaklaşık `5.55e-17 m²`'dir.

## Test sonucu

Faz 3, 29 yeni test durumu ekler. Tam paketteki 98 test; analitik geometriyi,
su hattı bağıntısını, residualları, yuvarlamasız hesabı, bütün sınırları,
yanlış türleri, NaN/infinity değerlerini, bağımsız ön/arka geometriyi, loading
değişiminin Faz 2 alanları üzerinden aktarımını ve bozulmuş Faz 2/Faz 3
sonuçlarının reddini kapsar.
