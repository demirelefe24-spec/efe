# Faz 1, Faz 2 ve Faz 3 kabulleri

Bu kayıt, statik yük dağılımı modelinin sonuçları yorumlanırken geçerli olan
kabulleri görünür tutar.

1. Referans tekne için `LCG = LCB = 1.987 m` ön tasarım kabulü yapılır. Bu,
   ölçülmüş bir LCG değildir ve yeni veri geldiğinde değiştirilmelidir.
2. Tekne ve foil bağlantıları rijit kabul edilir.
3. Durgun, ivmesiz ve statik denge ele alınır; zamana bağlı hareket yoktur.
4. Ön ve arka foil kaldırmaları, ilgili kaldırma merkezlerinde etkiyen noktasal
   eşdeğer düşey kuvvetlerle temsil edilir.
5. Tekne ağırlığı LCG'de etkiyen noktasal eşdeğer kuvvet olarak temsil edilir.
6. Gövde kaldırması, itki düşey bileşeni, aerodinamik kuvvetler, dalga kuvvetleri,
   kontrol yüzeyi kuvvetleri ve başka düşey kuvvetler bu ilk modelde ihmal edilir.
7. Ön foil, arka foil ve LCG boyuna konumları aynı kıç referansından ölçülür;
   pozitif eksen başa doğrudur.
8. Kaldırma için pozitif yön yukarıdır.
9. Yalnız normal `x_A < x_G < x_F` yerleşimi geçerlidir. Yazılım foil adlarını
   veya konumlarını sessizce ters çevirmez.
10. `g = 9.80665 m/s²` varsayılanıdır ve kullanıcı girdisi olarak değiştirilebilir.
11. Demo geometrisindeki `x_A = 0.750 m` ve `x_F = 3.250 m` yalnız yazılım
    testi içindir; gerçek bir foil yerleşim kararı değildir.
12. Faz 2'de ön ve arka foil aynı kuvvet tabanlı loading değerini kullanır.
    Farklı ön/arka loading desteği bu sürümde yoktur.
13. Hesaplanan `S_total`, `S_fore` ve `S_aft`, ortak `W/S` tanımından gelen
    temel referans alanlarıdır. Faz 3 bunları sabit-kord geometriye aktarır;
    hızla değişen gerçek ıslak alan olarak yorumlamaz.
14. Foil loading `[N/m²]` ile dinamik basınç `[Pa]` aynı boyuta sahiptir, ancak
    fiziksel olarak farklı büyüklüklerdir ve birbirinin yerine kullanılmaz.
15. `3000-7000 kgf/m²` genel tarama aralığı ile `3800-5700 kgf/m²` pratik
    aralık ayrı kaynak verileridir. Yazılım hiçbirini gizli varsayılan seçmez.
16. Faz 2 demosu pratik yayın aralığını yalnız doğrulama amacıyla kullanır;
    tekne için nihai foil loading veya alan seçimi değildir.
17. Faz 3 foili iki düz, simetrik, aynı uzunlukta ve sabit kordlu panel olarak
    modeller; taper, sweep, eğrisellik, strut ve karma V türleri yoktur.
18. `S_ref`, iki tam panelin foil düzlemlerindeki toplam kuru/referans planform
    alanıdır. `b_dev`, iki panelin fiziksel eğik uzunlukları toplamıdır.
19. Diyedral her panelin yatayla yaptığı açıdır. Apeks batması sakin su hattından
    aşağı doğru pozitiftir ve gerçek surface-piercing durumunda `0 < d < h_f`dir.
20. Faz 3 ıslak alanı, kullanıcı tarafından verilen tek bir sakin su hattı için
    geometriktir; heave, pitch, dalga, ventilasyon, spray ve esneklik yoktur.
21. Ön ve arka foil kendi span, diyedral ve batma girdilerine sahiptir; referans
    alanları yalnız sağlanan Faz 2 sonuç nesnesinden alınır.

Bu kabuller kaldırıldığında mevcut statik yük ve ortak-loading alan modeli
yeterli olmayabilir; ek denge denklemleri, geometri ve hidrodinamik girdiler
gerekir.
