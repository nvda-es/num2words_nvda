# [NVDA için Sayıları kelimelere Dönüştürücü](https://github.com/savoirfairelinux/num2words)

Yazar: Mateo Cedillo

## Giriş:

Bu küçük eklentiyi yapmak için ilham aldım, çünkü bazı insanlar `ETI-Eloquence' gibi konuşma sentezleyicileri kullanıyorlar, bu da sayı işleme konusunda bazı kusurlara sahip, ayrılmış olsalar bile ve kullanıcının her iki sayıyı da ondalık nokta gibi boşluklarla ayırarak söylemesini karıştırıyor.  

Bu eklenti, bu durumlar için sayıların kelimelere dönüştürülerek okunmasını iyileştirir, daha büyük sayıları destekler ve ayrıca kütüphane de birçok dili destekler.

## orijinal ve dönüştürülmüş konuşma girişi arasındaki sonuçların karşılaştırılması:

Bu karşılaştırma tablosu, bir sentezleyicide sayı işleme ile Sayıları kelimelere Dönüştürücü eklentisi ile işleme arasındaki farkları gösterir.

Aşağıdaki karşılaştırma, NVDA için [IBMTTS sürücüsü](https://github.com/davidacm/NVDA-IBMTTS-Driver) kullanılarak değerlendirilmiştir.


### Uzun sayıları kullanma:

| Dil | Orijinal girdi | Dönüştürülmüş çıktı girişi |
|---|---|---|---|
| İspanyolca | 921359131290481307233416326 | nueve dos ún tres cinco nueve ún tres ún dos nueve cero cuatro ocho ún tres cero siete dos tres tres cuatro ún seis tres dos seis | novecientos veintiuno cuatrillones trescientos cincuenta y nueve mil ciento treinta y uno trillones doscientos noventa mil cuatrocientos ochenta y uno billones trescientos siete mil doscientos treinta y tres millones cuatrocientos dieciséis mil trescientos veintiséis |
| İngilizce | 921359131290481307233416326 | nine two one three five nine one three one two nine zero four eight one three zero seven two three three four one six three two six | nine hundred and twenty-one septillion, three hundred and fifty-nine sextillion, one hundred and thirty-one quintillion, two hundred and ninety quadrillion, four hundred and eighty-one trillion, three hundred and seven billion, two hundred and thirty-three million, four hundred and sixteen thousand, three hundred and twenty-six |

### Ayırıcı olarak boşluk kullanmak (yalnızca İspanyolca):

* Orjinal girdi: 12 499
* Çıktı: doce mil cuatrocientos noventa y nueve
*  Dönüştürülmüş çıktı: doce cuatrocientos noventa y nueve

## kullanım:

Bu eklentide sayıları kelimelere dönüştürmenin üç yolu bulunur:

* Gerçek zamanlı mod: NVDA konuştuğu ve herhangi bir yerinde sayı içeren bir metin olduğu sürece, dönüştürme sonucu görüntülenecek ve konuşma yoluyla iletilecektir. Bu, kullandığınız herhangi bir konuşma sentezleyicisi için geçerlidir.
	* Bir giriş hareketi ekleyerek bu özelliği geçici olarak kullanabilirsiniz (aşağıya bakın). Bu geçici bir özellik olduğundan NVDA'dan çıktığınızda devre dışı bırakılacaktır.
	* Bu özelliği NVDA başlatıldığında başlayacak şekilde de yapılandırabilirsiniz. Bunu yapmak için NVDA+N tuşlarına basın, tercihler>ayarlar...'a gidin ve Sayıdan kelimelere kategorisini seçin. Orada ilgili onay kutusunu bulacaksınız
* El ile giriş modu: aynı anda sayı veya metin yazabilir, bunu yapmak için bir iletişim kutusu aracılığıyla etkileşimde bulunabilirsiniz. İletişim kutusunda şunlar bulunur:
	* Sıralı hale dönüştürmek için bir onay kutusu.
	* Sıra kutusu işaretlenmemişse, dönüştürme modunu seçmek için bir açılan kutu görüntülenir. beş dönüştürme modu vardır ve bunlar aşağıdaki gibidir:
		* Sıralı, örneğin: 1 = ilk.
		* Sıra numarası, örneğin: 1 = ilk (sıra seçeneğiyle aynı yöntemi uygular).
		* Tarih, örneğin (gg/aa/aaaa formatı): 23/07/2023 = Yirmi üç temmuz yirmi yirmi üç.
		* Saat, örneğin: 12:30:15 = On iki saat, otuz dakika ve on beş saniyedir.
		* Yıl, örneğin: 1980 = bin dokuz yüz seksen (birçok dilde etkisi yoktur).
		* Para birimi, örneğin: iki euro, on beş sent
		* Bu seçeneği seçtiğinizde, para birimini seçmeniz için yeni bir açılır kutu görünecektir. Her dilin euro dışında farklı para birimleri vardır ve liste değişiklik gösterebilir
	* Girdinizi yazmak için bir giriş kutusu.
	* Dönüştür düğmesi. Bu düğmeye basarak, nihai sonucu içeren bir mesaj kutusu gösterilecektir.
	* İptal düğmesi: Dönüştürme iletişim kutusundan çıkar.
* Seçim modu: Kelimelerin arasında sayılar veya sayılar içeren seçilmiş bir metin varsa, sonuç dönüştürülecek ve yüksek sesle söylenecektir.

Not: Ayrıca dönüştürülen son sonucu da kopyalayabilirsiniz (aşağıya bakın)

### Girdi hareketleri:

* Sayıları kelimelere dönüştür (veya gerçek zamanlı mod): (Diğer eklentilerle karışıklığı önlemek için şimdilik bir hareket atanmamış).
* Sayıları seçilen metne göre kelimelere dönüştürür (seçim modu): Hareket atanmamış.
* Dönüştürme iletişim kutusunu aç (El ile giriş modu): alt+shift+NVDA+n.
* Son söylenen sonucu kopyala: Hareket atanmamış.
* Yakında daha fazla özellik!

#### Önemli notlar:

* Kitaplık birçok dili desteklediğinden, dönüştürmenin konuşma sentezleyicinizin dilinde yapıldığını unutmayın. Bu, sentezleyicinizin dilini değiştirdiğinizde bile geçerli olacaktır.
* NVDA başlatılırken sentezleyici dili kontrol edilir. Kullanılan dil desteklenmiyorsa, size bildirilecektir.
* num2words kütüphanesi 27 adede kadar ardışık sayıyı dönüştürebilir. Metin 27 sayıdan uzunsa, bir bip sesi ve bir konuşma mesajı ile size bildirir.
* Şu anda, dönüştürülen bir sayının imleçle söylenmesi uygulanmamaktadır ve sonuç olarak dönüştürülen sayı hecelenecektir.

## Bu eklentiyi derleme:

Not: Bu eklenti bir alt modüle bağlıdır, yani:

1. bu depoya cd: `cd num2words_nvda`
2. Modül olarak ayarlanan num2words kitaplık deposunu kopyalamak için konsola "git submodule init" ve "git submodule update" yazın.
3. Hata yoksa `scons` komutu düzgün çalışmalıdır.

## İlham aldığım eklentiler:

* [NVDA için Saat ve Takvim](https://addons.nvda-project.org/addons/clock.en.html) çünkü bana tarih ve saat dönüşümünü nasıl uygulayabileceğim konusunda temel bir fikir verdi.

## İletişim:

Bu eklentinin geliştirilmesine yardımcı olmak istiyorsanız `angelitomateocedillo@gmail.com` adresine e-posta gönderebilir veya GitHub deposunda katkılarınızı yapabilirsiniz.

---

# Değişiklik günlüğü:

## 0.5

* Eklendi: NVDA 2024.1 desteği yeniden sunuldu ve Sayıdan Kelimelere anahtarı için gerçek zamanlı olarak İsteğe Bağlı mod desteği eklendi.
* Eklendi: yeni komut
	* Seçilen metne göre sayıları kelimelere dönüştürün.
	* Son dönüştürülen sonucu kopyalayın, teşekkürler 'mk360'.
* Düzeltildi: geçersiz ondalık sayılarla ilgili hatalar. Şimdi, örneğin, gerçek zamanlı modda Sayıdan kelimelere etkinleştirildiğinde, NVDA bu durumlarda sessiz kalmayacak veya günlükte bir hata görüntülemeyecektir.
* Güncellendi: Sayıdan kelimelere kütüphanesi.
	* Bu güncelleme yeni diller olarak: İspanyolca Kosta Rika, Galce ve Çeçence dillerini bulundurur
	* Kod iyileştirmeleri, python 3.12 uyumluluğu.
* Eklentinin tamamında kod düzenlemesi yeniden yapıldı. Bu şekilde katkıda bulunanlar için daha okunabilir ve organize edilebilir.

## 0.4.1

* Bu yamada NVDA'nın son test edilen sürümü için bir gerileme yaptım. Dürüst olmak gerekirse, bu eklentiyi 2024.1 alpha ile test etmiş olmama ve 2024.1'in henüz yayınlanmamasına rağmen, eklenti mağazasında yayınlamayla ilgili sorunları önlemek için memnuniyetle geri döneceğim. En son test edilen sürüm olarak 2023.3.
* Ayrıca okunabilirliği artırmak için koddaki bazı işlevlerdeki değişkenler netleştirildi.

## 0.4

* Artık, dönüştürme modunu para birimine göre seçerken, seçilen dil tarafından desteklenen ve sentezleyici tarafından belirlenen para birimlerinin listesi aracılığıyla dönüştürülecek para birimini seçmek için bir açılır kutu eklendi.
* Başlatma sırasında gerçek zamanlı modda kelimelerin sayılarını okumayı etkinleştirmek için NVDA ayarları paneline bir seçenek eklendi.
* George ve Volodymyr Pyrig sayesinde Ukrayna dili eklendi.
* num2words 0.5.13'e güncellendi
	* Belarusça ve Slovakça için destek eklendi.
	* Rusça ve Ukraynaca için güncellemeler ve kod yeniden düzenlemeleri.
* Eklenti artık ayarlar paneli > gelişmiş bölümündeki karalama defteri seçeneğinin etkin olup olmadığını kontrol etmiyor.
* Düzeltildi: Web sitelerine göz atarken dize dizini aralık dışı hatası. Teşekkürler Volodymyr.
* Düzeltildi: Gerçek zamanlı dönüştürme ve NVDA konuşma ayırıcıları. Eklenti artık dönüştürülen kelimeleri doğru şekilde ayırmalıdır.
* Düzeltildi: NVDA 2024.1 ile uyumluluk.
* Düzeltildi: Saat dönüşümünde yanlış çeviri kullanımı. Dil koruyucularının, dilin düzgün çalışması için yeni girişleri güncellemesi gerekecektir.
* Daha iyi okunabilirlik için kodu düzelttim.

## 0.3

* Türkçe dil eklendi, Umut KORKMAZ'a teşekkürler.
* El ile  dönüştürme GUI'sine tarih ve saat dönüşümleri eklendi.

## 0.2

* Şimdi sayılardan kelimelere sonuç büyük harfle yazılır.
* 'da48a319179f19b900d5b01ed394b304e94d31cf' işlemek için num2words kitaplığı güncellendi.
* Elle dönüştürme GUI'sinde num2words kitaplığı tarafından desteklenen dönüştürme modları eklendi.
* Elle dönüştürme GUI'sinde küçük düzeltmeler.
* NVDA'yı başlatırken sentezleyici dil kontrolü eklendi. Bu nedenle, dilin desteklenmemesi durumunda bu eklentinin bir kısmı devre dışı bırakılacaktır.

## 0.1

* İlk sürüm. Bazı küçük hatalar bulabilirsiniz. Eğer öyleyse, lütfen bana bildirin.