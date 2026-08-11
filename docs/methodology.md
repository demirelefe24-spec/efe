# Yöntem ve kaynak izlenebilirliği

## 1. Kapsam ve kaynak hiyerarşisi

Bu belge iki yayının tamamı incelenerek hazırlanmıştır. Kaynak kodu eşlemesi:

- **R1:** Schachter ve Fonteles (2022), surface-piercing dahil ana otorite.
- **R2:** Schachter ve Fonteles (2020), fully-submerged algoritma ve program
  sırası için çapraz kontrol.
- **P1:** Bu projenin Faz 1 şartnamesi; iki yayın tarafından numaralandırılmayan
  statik ön/arka yük paylaşımı için açık kuvvet ve moment dengesi.
- **P2:** Bu projenin Faz 2 şartnamesi; SI birim sözleşmesi, toplam/ön/arka
  referans alanı çözümü ve bağımsız residual kontrolleri.
- **P3:** Bu projenin Faz 3 şartnamesi; düz, simetrik, sabit-kord V-foil için
  geometri referansları, ıslak alan ve Faz 2 alan aktarımı.

R1 ve R2, foil boyuna konumlarının ön/arka yükleri belirlemek için kullanıldığını
söyler; ancak iki foil arasındaki statik yük paylaşımını ayrı, numaralı bir
denklem olarak yayımlamaz. Bu nedenle Faz 1 denklemleri R1/R2'ye yanlış denklem
numarasıyla atfedilmemiştir.

## 2. Yayınlardaki genel hesap akışı

R1 Bölüm 3 ve R2 Bölüm 3'teki ortak sıra şöyledir:

1. Önceden tasarlanmış yüksek hızlı gövdeden deplasman, LCG/VCG, seyir hızı,
   ana boyutlar, geometri, çalışma deniz durumu, güvenlik katsayısı ve
   hidrostatik veriler alınır.
2. Ön ve arka foil için profil, malzeme, konfigürasyon, kıçtan boyuna konum ve
   yüzey pürüzlülüğü seçilir.
3. Span, strut span, eğim/dihedral ve ilgili foil geometrisi girilir; geometrik
   uygulanabilirlik kontrol edilir.
4. Bir `W/S` aralığında alan, kord, kaldırma, hücum açısı, yapısal alt kalınlık
   sınırı ve kavitasyon üst kalınlık sınırı hesaplanır; uygun/optimum nokta
   seçilir.
5. Seçilen foiller için hız adımlarıyla kalkış incelenir. Kaldırma ağırlığa
   ulaşana kadar başlangıç hücum açısı korunur, ardından kaldırmayı ağırlığa eşit
   tutmak için hücum açısı azaltılır.
6. Gövde deplasmanı foil kaldırması kadar azaltılır. R1/R2, `Fn < 0.4` için
   Holtrop, daha büyük değerler için Savitsky kullanımını ve toplam direnç/güç
   eğrilerini tarif eder.

Bu projede boyuna statik yük paylaşımı, seçilmiş ortak `W/S` değerinden temel
referans alanları ve düz/simetrik surface-piercing V-foil geometrisi
uygulanmıştır. Profil ve hidrodinamik katsayılar sonraki fazların kapsamıdır.

## 3. Koordinat ve kuvvet sistemi

R1 Bölüm 4, gövde referanslarının kıç, baseline ve merkez hattı olduğunu söyler;
R2 Bölüm 4.2.1 boyuna foil konumlarını kıçtan tanımlar. Yayınlar pozitif boyuna
ekseni ve statik yük paylaşımı işaretini açık bir denklemle tanımlamaz.

P1 için açık konvansiyon:

- orijin kıç referansı;
- pozitif `x` kıçtan başa;
- pozitif kaldırma yukarı;
- `x_A < x_G < x_F`;
- ağırlık `W` LCG'de aşağı, `L_A` ve `L_F` foil merkezlerinde yukarı.

## 4. Faz 1 statik denge denklemleri

Bu tabloda `PB-*` proje içi izlenebilirlik kimliğidir; yayın denklem numarası
değildir.

| Kimlik | Denklem | Birimler | Kaynak |
|---|---|---|---|
| PB-01 | `W = m g` | `m [kg]`, `g [m/s²]`, `W [N]` | P1 Görev 5 |
| PB-02 | `L_F + L_A = W` | bütün kuvvetler `[N]` | P1 Görev 5, düşey kuvvet dengesi |
| PB-03 | `L_F (x_F-x_G) = L_A (x_G-x_A)` | konum `[m]`, moment `[N m]` | P1 Görev 5, LCG etrafında moment dengesi |
| PB-04 | `L_F = W (x_G-x_A)/(x_F-x_A)` | `[N]` | PB-02 ve PB-03 çözümü |
| PB-05 | `L_A = W (x_F-x_G)/(x_F-x_A)` | `[N]` | PB-02 ve PB-03 çözümü |
| PB-06 | `r_F = L_F + L_A - W` | `[N]` | bağımsız kuvvet residual kontrolü |
| PB-07 | `r_M = L_F(x_F-x_G) - L_A(x_G-x_A)` | `[N m]` | bağımsız moment residual kontrolü |

Yük payları `L_F/W` ve `L_A/W`; yüzdeler bunların 100 katıdır. Çekirdek
hesabında yuvarlama yapılmaz. Residual sınırları mutlak ve ölçeğe bağlı göreli
toleransların toplamıdır; değerler `constants.py` içinde isimlendirilmiştir.

## 5. Faz 2: `W/S`, birimler ve temel alan denklemleri

### 5.1 Kaynak izlenebilirliği

R1 journal s.55 (PDF s.3), `W/S`'yi foilin taşıdığı ağırlığın foil alanına oranı
olarak açıklar; pratik aralığı `3800-5700 kgf/m²`, programın genel çizim/tarama
aralığını `3000-7000 kgf/m²` verir. R1 journal s.61 (PDF s.9), Denklem (53):

`C_L = L / (0.5 rho V² S) = (W/S) / q`, `q = 0.5 rho V²`.

R2 PDF s.2 aynı tanım ve aralıkları tekrarlar; R2 PDF s.5, Denklem (22) aynı
`C_L = (W/S)/q` ilişkisini verir. R1 daha yeni ana otoritedir; bu konuda R1 ve
R2 arasında yöntem farkı yoktur.

### 5.2 Projenin kesin SI sözleşmesi

Programda `W/S`, kuvvet tabanlı foil loading olarak temsil edilir:

`foil_loading_n_m2 = force_n / reference_area_m2`

Kanonik birimi `N/m² = Pa`'dır. Mass loading `[kg/m²]`, legacy loading
`[kgf/m²]`, force-based foil loading `[N/m²]` ve dynamic pressure `[Pa]` ayrı
kavramlardır. Foil loading ile dynamic pressure aynı boyuta sahip olsa da aynı
fiziksel büyüklük değildir.

Tam dönüşüm `1 kgf = 9.80665 N` ile yapılır:

- `3800 kgf/m² = 37265.270 N/m²`;
- `5700 kgf/m² = 55897.905 N/m²`;
- `3000 kgf/m² = 29419.950 N/m²`;
- `7000 kgf/m² = 68646.550 N/m²`.

Yayınların `3800-5700 kgf/m² = 800-1200 PSI` ifadesi doğrudan kullanılmaz.
SI değerleri yaklaşık `778.30-1167.45 psf`, fakat yalnız
`5.405-8.107 psi` eder. Bu nedenle `PSI` ifadesi muhtemel `PSF` dizgi hatası
olarak kaydedilir. Kaynak metin sessizce değiştirilmez.

Genel ve pratik aralıklar ayrı isimlendirilmiş sabitlerdir. Alan veya tarama API'si
loading sınırlarına varsayılan atamaz; kullanıcı hangi aralığı seçtiğini açıkça
belirtir.

### 5.3 Uygulanan alan denklemleri

Ön ve arka foil için aynı loading `lambda` kullanılır. `FA-*` kimlikleri proje
içi Faz 2 denklem kimliğidir; yayın denklem numarası değildir.

| Kimlik | Denklem | Birimler | Kaynak |
|---|---|---|---|
| FA-01 | `lambda = W / S_total` | `lambda [N/m²]`, `W [N]`, `S [m²]` | R1 (53), R2 (22), P2 SI sözleşmesi |
| FA-02 | `S_total = W / lambda` | `[m²]` | FA-01 çözümü, P2 |
| FA-03 | `S_fore = L_fore / lambda` | `[m²]` | P2, ortak loading kabulü |
| FA-04 | `S_aft = L_aft / lambda` | `[m²]` | P2, ortak loading kabulü |
| FA-05 | `r_S = S_fore + S_aft - S_total` | `[m²]` | bağımsız alan residualı, P2 |
| FA-06 | `r_W = lambda S_total - W` | `[N]` | bağımsız toplam kuvvet residualı, P2 |
| FA-07 | `r_F = lambda S_fore - L_fore` | `[N]` | bağımsız ön kuvvet residualı, P2 |
| FA-08 | `r_A = lambda S_aft - L_aft` | `[N]` | bağımsız arka kuvvet residualı, P2 |
| FA-09 | `S_fore/S_total - L_fore/W` | boyutsuz | alan/yük oranı residualı, P2 |
| FA-10 | `S_aft/S_total - L_aft/W` | boyutsuz | alan/yük oranı residualı, P2 |

Tarama, iki sınırı da içeren doğrusal ve deterministik `sample_count` noktası
üretir. Noktalar artan loading sırasındadır; bu nedenle ilk nokta minimum loading
ve maksimum alan, son nokta maksimum loading ve minimum alandır. Hesap çekirdeği
yuvarlama yapmaz.

## 6. Faz 3: surface-piercing V-foil geometrisi

R1 journal s.59 (PDF s.7), surface-piercing foilde bir bölümün daima su dışında
kaldığını ve ıslak alanın her hız/yükselme durumunda yeniden hesaplandığını
belirtir. Aynı bölüm spanların diyedral ve eğim açılarına göre ayarlandığını
söyler. R1 journal s.62-64 (PDF s.10-12), V/double-V/W/flat-bottom-V
konfigürasyonlarını ve foil height, dihedral, submergence/emersion girdilerini
gösterir. R2, surface-piercing arayüzünü doğrular fakat bu yöntemin bildiride
sunulmadığını belirtir.

Kaynaklar düz V için tam geometrik dönüşüm algoritmasını, span eksenini veya
`h_f` sembolünü tek anlamlı şekilde yayımlamaz. Bu nedenle aşağıdaki `VG-*`
ilişkileri P3 proje tanımlarıdır ve yayın denklem numarası değildir:

| Kimlik | Denklem | Birimler |
|---|---|---|
| VG-01 | `l = b_dev/2` | `[m]` |
| VG-02 | `h_f = l sin(Gamma)` | `[m]` |
| VG-03 | `b_h = b_dev cos(Gamma)` | `[m]` |
| VG-04 | `c = S_ref/b_dev` | `[m]` |
| VG-05 | `l_wet = d/sin(Gamma)` | `[m]` |
| VG-06 | `S_wet = 2 c l_wet` | `[m²]` |
| VG-07 | `f_wet = S_wet/S_ref = d/h_f` | boyutsuz |
| VG-08 | `b_WL = 2 d cot(Gamma)` | `[m]` |
| VG-09 | `l_dry = l-l_wet`, `e=h_f-d` | `[m]` |

Burada `S_ref` iki tam panelin foil düzlemlerindeki toplam referans alanı,
`b_dev` iki fiziksel eğik panel uzunluğunun toplamı, `Gamma` panel-yatay açısı
ve `d` sakin su hattından aşağı pozitif apeks batmasıdır. Geçerli durum
`0 < d < h_f`dir. R1 Denklem (17)'de “foil submersion” denilen `h_f`, bu
projedeki fiziksel apeks-uç yüksekliğiyle otomatik olarak özdeşleştirilmez.

Faz 2 `fore_area_m2` ve `aft_area_m2` değerleri Phase 3'te yeniden hesaplanmadan
ilgili geometrilere aktarılır. Ayrıntılı sözlük ve sınırlar
`phase_3_geometry_definitions.md` içindedir.

## 7. R1 surface-piercing hidrodinamik yöntem haritası

Aşağıdaki yüksek-faz denklemleri yalnız kaynak haritasıdır ve bu sürümde
uygulanmamıştır. Denklem (53)'ün yalnız `W/S` boyutsal tanımı Faz 2'de
kullanılmış; `C_L`, `q` veya kavitasyon hesabı uygulanmamıştır. Faz 3'ün statik
geometrik ıslak alanı bu hidrodinamik denklemlerin uygulandığı anlamına gelmez.

| R1 denklem(ler)i | İçerik | Değişken ve birim özeti |
|---|---|---|
| (13)-(15) | `L = 0.5 rho V² S C_L`, `C_L = C_Lalpha alpha_T`, iki boyutlu ince foil için `2 pi` eğim | R1 `L [kgf]`, `S [m²]`; `C_L` boyutsuz, açı radyan olmalı |
| (16) | Fully-submerged aspect-ratio düzeltmesi | `AR` boyutsuz |
| (17) | Surface-piercing düzeltmesi: `AR(1+h_f/b) / ([AR(1+h_f/b)] + 2)` | `h_f/b` boyutsuz |
| (18)-(19) | Wadlin serbest yüzey katsayısı `K` ve düzeltilmiş `C_Lalpha` | `h_f/c` boyutsuz; `C_Lalpha` radian başına |
| (21)-(24) | Drag kuvveti, toplam `C_D`, profil/sürtünme ve dalga bileşenleri | R1 `D [kgf]`; katsayılar boyutsuz; `Fn_c` boyutsuz |
| (29)-(31) | Fully-submerged indüklenmiş sürükleme, biplane katsayısı ve ayarlanmış AR | katsayılar boyutsuz; R1 surface-piercing için `C_Di=0` der |
| (32) | `alpha_T = C_L/C_Lalpha` | açı, tutarlı kullanımda radyan |
| (33)-(37) | Eğilme momenti, kesit atalet momenti ve minimum yapısal `t/c` | R1 `W/S` için "IS units" der; `g`, `sigma_y`, `b`, `c` birlikte kullanılır |
| (38)-(50) | Bernoulli ve kavitasyon sayısı türetimi | basınç ve dinamik basınç aynı birimde |
| (51)-(55) | İncipent kavitasyon bağıntısı ve maksimum `t/c` | (55) sabitleri 15 °C ve `g=9.81 m/s²` kabulüne bağlıdır |
| (56) | `(C_L/C_D)_max`; surface-piercing için `C_Di=0` notu | oran boyutsuz |

R1 ayrıca surface-piercing foilin bir kısmının daima su dışında olduğunu,
indüklenmiş sürükleme teriminin uygulanmadığını ve ıslak alan `S`'nin her hız ve
her yükselme durumunda etkileşimli olarak yeniden hesaplandığını belirtir. Foil
spanları yapısal hesapta dihedral ve eğim açılarına göre düzeltilir. Şekil 15-16,
V, double-V, W ve flat-bottom-V geometrilerini gösterir; ancak tam geometrik
dönüşüm algoritması yayımlanmaz.

## 8. R2 çapraz kontrol haritası

R2, fully-submerged bağıntıları daha kısa numaralandırır:

- kaldırma ve düzeltmeler: (1)-(6);
- drag: (7)-(13);
- hücum açısı: (14);
- yapı: (15)-(19);
- kavitasyon: (20)-(24);
- maksimum `C_L/C_D`: (25).

R2 Bölüm 1 ve 4.2.2.1, programın surface-piercing foil de işlediğini ancak bu
kısmın bildiride sunulmadığını açıkça söyler. Dolayısıyla surface-piercing için
R2'den bağımsız bir denklem veya katsayı alınmamıştır.

## 9. Kaynaklar arasındaki farklar

| Konu | R1 (2022) | R2 (2020) | Proje kararı |
|---|---|---|---|
| Kapsam | Fully-submerged ve surface-piercing | Ayrıntılı bağıntılar yalnız fully-submerged | Surface-piercing için R1 ana otorite |
| Denklem numarası | Geniş türetim nedeniyle (13)-(56) ana tasarım denklemleri | Aynı fully-submerged çekirdek (1)-(25) | Her belgede kendi numarası korunur |
| AR düzeltmesi | (16) fully-submerged, (17) surface-piercing | (4) fully-submerged | R1 (17), Faz 4+ öncesi sembol doğrulaması gerektirir |
| İndüklenmiş drag | Surface-piercing için uygulanmaz | Yalnız fully-submerged anlatılır | Bu turda kodlanmadı |
| Islak alan | Hız/yükselme başına yeniden hesaplanır | Surface-piercing algoritması sunulmaz | Faz 3 yalnız kullanıcının verdiği sakin-su-hattı geometrisini P3 ile hesaplar; dinamik algoritma uygulanmaz |
| Sonuç birimleri | Formüllerde kgf, sonuç tablolarında N/kN görülür | Formüllerde kgf, metrik arayüz | Çekirdek yalnız SI; dönüşüm doğrulanmadan aktarım yok |

## 10. Açık noktalar ve mühendislik belirsizlikleri

1. **Ön/arka statik yük denklemi:** R1/R2 boyuna konumların yük için
   kullanıldığını söyler ama yük paylaşımı denklemini yayımlamaz. Faz 1, P1'deki
   açık statik denge sistemini kullanır.
2. **`W/S` kaynak etiketi:** Her iki yayın `3800-5700 kgf/m²` değerlerini
   `800-1200 PSI` olarak verir. Faz 2 boyut analizi bunun yaklaşık
   `778-1167 psf` olması gerektiğini gösterir. Proje SI hesabı kesinleştirilmiştir,
   ancak kaynakta gerçekten `PSF` amaçlandığı yazarlar tarafından doğrulanmamıştır.
3. **`rho` tanımı:** R1/R2, `rho` için "specific gravity" ve
   `kgf s²/m⁴` kullanır. Modern SI kütle yoğunluğu `[kg/m³]` ile doğrudan kod
   eşlemesi yapılmadan önce kuvvet sistemi açıkça dönüştürülmelidir.
4. **Parantez dizgisi:** R1 (16) ve R2 (4) metin dizgisinde `AR/AR+2` görünür;
   amaçlanan parantezin `AR/(AR+2)` olduğu bağlamdan güçlü biçimde anlaşılır,
   fakat uygulama öncesi açık kaynak kaydı tutulmalıdır.
5. **Surface-piercing ıslak geometri:** Kaynaktaki tam cebirsel sıra ve sembol
   eksikleri devam eder. Faz 3 bu boşluğu açık P3 proje sözleşmesiyle doldurur;
   dinamik yükselme/hız modeli veya diğer V türleri kaynak denklemiymiş gibi
   sunulmaz.
6. **Surface-piercing drag:** R1, `C_Di=0` kabulünü açıkça verir ancak bunun
   yerine ek spray/ventilation veya serbest yüzey drag terimi tanımlamaz.
7. **Yapısal Denklem (37):** `W/S`, `g`, `sigma_y`, güvenlik katsayısı ve
   geometrik terimlerin birim sistemi metinde "IS" olarak anılır; yayınlardaki
   kgf/N kullanımı nedeniyle boyutsal doğrulama gereklidir.
8. **Kavitasyon Denklem (55):** `69.06` ve `10.045` katsayıları 15 °C akışkan
   özellikleri ile belirli basınç/kuvvet birimlerine gömülüdür. SI kökeni yeniden
   kurulmadan koda alınmamalıdır.
9. **Sembol tekrarı:** R1'de `a` hem foil/strut geometrisinde hem Denklem (52)
   çevresinde camber/mean-line yüksekliği için kullanılır; veri modelinde farklı
   isimlere ayrılmalıdır.
10. **Açı birimi:** Teorik `C_Lalpha=2 pi` radian tabanlıdır; sonuç tabloları
    hücum açısını derece gösterir. Hesap ve sunum dönüşümü açıkça ayrılmalıdır.

Bu belirsizlikler, ilgili sonraki faz başlamadan çözülmelidir. Faz 3 yalnız açık
Öklid geometrisi ve Faz 2 alan aktarımını uygular; belirsiz ampirik bağıntıları
koda aktarmaz.
