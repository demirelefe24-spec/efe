# Faz 3 geometri tanımları

## Kapsam

Faz 3, düz, simetrik ve sabit kordlu bir surface-piercing V-foilin durgun su
hattındaki geometrisini tanımlar. İki panel aynı fiziksel uzunluğa, korda ve
diyedral açısına sahiptir. Bu model taper, sweep, flat-bottom-V, double-V, W,
strut alanı veya eğrisel panel içermez.

R1, surface-piercing foilde alanın hız ve yükselme durumuna göre yeniden
hesaplandığını, spanların diyedral/eğim açısına göre ayarlandığını ve V ailesi
konfigürasyonlarını belirtir. R2, programda surface-piercing girdi ve çizim
ekranlarını gösterir fakat bu kısmın yöntemini yayımlamadığını açıkça söyler.
İki kaynak da aşağıdaki tam geometrik dönüşüm sırasını ve span eksenini
eksiksiz tanımlamaz. Bu nedenle `VG-*` denklemleri yayın denklem numarası değil,
Faz 3 şartnamesiyle kesinleştirilmiş proje geometrisi tanımlarıdır.

## Kaynak-kanonik eşleme

| Yerel kaynak dosyası | Sayfa / denklem | Kaynakta açıkça verilen | Yazılım karşılığı ve sınıfı |
|---|---|---|---|
| `references/Preliminary design dimensioning of hydrofoil boats with fully submerged and surface piercing foils.pdf` | Journal s.57 / PDF s.5, Denklem (13) | Foil alanı `S`, span `b` ile chord `c` çarpımıdır. Span ekseni burada açık değildir. | `S_ref = c b_dev`; `b_dev` seçimi **proje konvansiyonu**, `S=bc` alan ilişkisi **doğrudan kaynak tanımıdır**. |
| Aynı R1 dosyası | Journal s.59 / PDF s.7, numaralı denklem yok | Surface-piercing foilde bir bölüm su dışındadır; ıslak `S` hız ve yükselme durumunda yeniden hesaplanır. Spanlar diyedral/eğime göre ayarlanır. | Bir sakin-su-hattı durumu için `S_wet`; **kaynaktan yönlendirilen fakat P3 geometrisinden türetilen ilişki**. Dinamik hız/yükselme çözümü değildir. |
| Aynı R1 dosyası | Journal s.62-64 / PDF s.10-12, Şekil 15-16 ve Tablo 3 | V/double-V/W/flat-bottom-V düzenleri ile foil height, dihedral, submergence/emersion girdileri gösterilir. | Bu sürüm yalnız düz simetrik V'yi uygular; eksenler ve `VG-*` cebiri **proje konvansiyonudur**. |
| Aynı R1 dosyası | Journal s.57 / PDF s.5, Denklem (17) | `h_f`, yüzey-kesen aspect-ratio düzeltmesinde “foil submersion” olarak anılır. | `foil_vertical_height_m` ile özdeşliği **kaynakta belirsizdir**; Faz 3 bu denklemdeki sembolü kullanmaz. |
| `references/Development of a Computer Program for the Dimensioning of Hydrofoil Boats.pdf` | PDF s.1, s.8-11; numaralı geometri denklemi yok | Program surface-piercing foil destekler ve ilgili girdi/çizim ekranları vardır; yöntem bu bildiride sunulmaz. | Konfigürasyon kapsamı için **çapraz kontrol**; hiçbir `VG-*` denklemi R2'ye atfedilmez. |

## Referanslar ve işaretler

- Sakin su hattı yatay referanstır.
- Diyedral `Gamma`, her panelin yatayla yaptığı açıdır; API girdisi derecedir.
- V apeksi geometrinin en düşük noktasıdır.
- Apeks batması `d`, sakin su hattından aşağı doğru pozitiftir.
- `S_ref`, iki tam panelin kendi foil düzlemlerinde ölçülen toplam kuru/referans
  planform alanıdır.
- `b_dev`, sol ve sağ eğik panellerin fiziksel uzunlukları toplamıdır; yatay
  izdüşüm değildir.
- Her panelin sabit kordu `c`'dir.
- `h_f`, apeks ile fiziksel panel ucu arasındaki düşey geometri yüksekliğidir.
  R1 Denklem (17) çevresinde “foil submersion” olarak anılan `h_f` ile otomatik
  olarak özdeş kabul edilmez.

## Kanonik denklemler

| Kimlik | Denklem | Açıklama |
|---|---|---|
| VG-01 | `l = b_dev / 2` | Tek panelin fiziksel uzunluğu |
| VG-02 | `h_f = l sin(Gamma)` | Apeks-uç düşey yüksekliği |
| VG-03 | `b_h = 2 l cos(Gamma) = b_dev cos(Gamma)` | Toplam yatay izdüşümlü açıklık |
| VG-04 | `c = S_ref / b_dev` | Sabit ortalama kord |
| VG-05 | `l_wet = d / sin(Gamma)` | Her panelin ıslak fiziksel uzunluğu |
| VG-06 | `S_wet = 2 c l_wet` | İki panelin toplam ıslak referans alanı |
| VG-07 | `f_wet = S_wet/S_ref = l_wet/l = d/h_f` | Islak alan oranı |
| VG-08 | `b_WL = 2 l_wet cos(Gamma) = 2 d cot(Gamma)` | Su hattı kesişim genişliği |
| VG-09 | `l_dry = l - l_wet` | Her panelde su dışında kalan fiziksel uzunluk |
| VG-10 | `e = h_f - d` | Panel ucunun su hattı üstündeki düşey yüksekliği |

Gerçek surface-piercing durumu için sınırlar `S_ref > 0`, `b_dev > 0`,
`0 deg < Gamma < 90 deg` ve `0 < d < h_f` şeklindedir. `d = h_f` tam batmış
panel ucunu, `d <= 0` ise bu modelin işaret sözleşmesinde geçerli bir batmış
apeksi temsil etmediği için kabul edilmez.

## Kapanış denklemleri

Çekirdek üç bağımsız residual döndürür:

- `r_area = S_ref - c b_dev`;
- `r_wet = S_wet - f_wet S_ref`;
- `r_height = h_f - (d + e)`.

Hesap çekirdeğinde yuvarlama yapılmaz. Mutlak tolerans tabanına ölçeğe bağlı
`1e-12` göreli terim eklenir.

## Faz 2 alan aktarımı

`SurfacePiercingVFoilPairInputs`, mevcut bir `FoilAreaResult` nesnesini doğrudan
alır. Ön geometri `fore_area_m2`, arka geometri `aft_area_m2` kullanır; Faz 1
yükleri veya Faz 2 alanları yeniden hesaplanmaz. Sonuç, aynı Faz 2 nesnesini
korur ve şu aktarım kapanışlarını raporlar:

- ön geometri alanı eksi Faz 2 ön alanı;
- arka geometri alanı eksi Faz 2 arka alanı;
- iki geometri referans alanı toplamı eksi Faz 2 toplam alanı.

## Yorumlama sınırı

Hesaplanan `S_wet`, kullanıcı tarafından verilen tek bir sakin-su-hattı apeks
batması için geometrik ıslak referans alanıdır. Teknenin hız, heave, pitch,
dalga, ventilasyon, spray veya elastik deformasyonla değişen gerçek zamanlı
ıslak alanını çözmez. Hidrodinamik kaldırma veya çalışma noktası da Faz 3
kapsamında değildir.
