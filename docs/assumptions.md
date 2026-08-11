# Faz 1 ve Faz 2 kabulleri

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
    temel referans alanlarıdır. Bunlar kord/span/dihedral geometrisi veya
    surface-piercing foilin hızla değişen gerçek ıslak alanı değildir.
14. Foil loading `[N/m²]` ile dinamik basınç `[Pa]` aynı boyuta sahiptir, ancak
    fiziksel olarak farklı büyüklüklerdir ve birbirinin yerine kullanılmaz.
15. `3000-7000 kgf/m²` genel tarama aralığı ile `3800-5700 kgf/m²` pratik
    aralık ayrı kaynak verileridir. Yazılım hiçbirini gizli varsayılan seçmez.
16. Faz 2 demosu pratik yayın aralığını yalnız doğrulama amacıyla kullanır;
    tekne için nihai foil loading veya alan seçimi değildir.

Bu kabuller kaldırıldığında mevcut statik yük ve ortak-loading alan modeli
yeterli olmayabilir; ek denge denklemleri, geometri ve hidrodinamik girdiler
gerekir.
