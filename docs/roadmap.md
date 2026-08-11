# Yol haritası

Her faz, bir sonraki mühendislik modülüne geçilmeden önce kaynak, birim ve test
bakımından doğrulanacaktır.

| Faz | İçerik | Durum |
|---|---|---|
| 0 | Kaynak, yöntem, denklem, birim ve belirsizlik haritası | Tamamlandı |
| 1 | Statik ön/arka foil yük dağılımı ve doğrulama | Tamamlandı |
| 2 | Kuvvet tabanlı `W/S`, temel referans alanları ve loading taraması | Tamamlandı |
| 3 | Düz, simetrik surface-piercing V-foil geometrisi ve Faz 2 entegrasyonu | Tamamlandı |
| 4 | Hidrodinamik çalışma noktası | Uygulanmadı |
| 5 | Basitleştirilmiş yapısal sınır | Uygulanmadı |
| 6 | Kavitasyon sınırı | Uygulanmadı |
| 7 | Uygun tasarım bölgesi ve aday karşılaştırması | Uygulanmadı |
| 8 | Kalkış, direnç ve güç | Uygulanmadı |
| 9 | PySide6 masaüstü uygulaması | Uygulanmadı |
| 10 | PyInstaller ile Windows dağıtımı | Uygulanmadı |

Faz 3'te geliştirilmiş/yatay span ayrımı, diyedral ve batma işaretleri,
sabit-kord V-foil denklemleri, sakin su hattındaki geometrik ıslak alan ve Faz 2
alan aktarımı kesinleştirilmiştir. Bir sonraki çalışma Faz 4 hidrodinamik çalışma
noktasına geçmeden önce `C_L`, aspect ratio ve serbest yüzey bağıntılarının birim
ve sembol denetimini yapmalıdır.
