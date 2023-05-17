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

Bu eklentide sayıları kelimelere dönüştürmenin iki yolu bulunur:

* Gerçek zamanlı mod: NVDA konuştuğu ve herhangi bir yerinde sayı içeren bir metin olduğu sürece, dönüştürme sonucu görüntülenecek ve konuşma yoluyla iletilecektir. Bu, kullandığınız herhangi bir konuşma sentezleyicisi için geçerlidir.
* El ile giriş modu: aynı anda sayı veya metin yazabilir, bunu yapmak için bir iletişim kutusu aracılığıyla etkileşimde bulunabilirsiniz. İletişim kutusunda şunlar bulunur:
	* Sıralı hale dönüştürmek için bir onay kutusu.
	* Sıra kutusu işaretlenmemişse, dönüştürme modunu seçmek için bir açılan kutu görüntülenir. Dört dönüştürme modu vardır ve bunlar aşağıdaki gibidir:
		* Sıralı, örneğin: 1 = ilk.
		* Sıra numarası, örneğin: 1 = ilk (sıra seçeneğiyle aynı yöntemi uygular).
		* Yıl, örneğin: 1980 = bin dokuz yüz seksen
		* Para birimi, örneğin: iki euro, on beş sent
	* Girdinizi yazmak için bir giriş kutusu.
	* Dönüştür düğmesi. Bu düğmeye basarak, nihai sonucu içeren bir mesaj kutusu gösterilecektir.
	* İptal düğmesi: Dönüştürme iletişim kutusundan çıkar.

### Girdi hareketleri:

* Sayıları kelimelere dönüştür (veya gerçek zamanlı mod): (Diğer eklentilerle karışıklığı önlemek için şimdilik bir hareket atanmamış).
* Dönüştürme iletişim kutusunu aç (El ile giriş modu): alt+shift+NVDA+n.
* Yakında daha fazla özellik!

#### Önemli notlar:

* Kitaplık birçok dili desteklediğinden, dönüştürmenin konuşma sentezleyicinizin dilinde yapıldığını unutmayın. Bu, sentezleyicinizin dilini değiştirdiğinizde bile geçerli olacaktır.
* NVDA başlatılırken sentezleyici dili kontrol edilir. Kullanılan dil desteklenmiyorsa, size bildirilecektir.
* num2words kütüphanesi 27 adede kadar ardışık sayıyı dönüştürebilir. Metin 27 sayıdan uzunsa, bir bip sesi ve bir konuşma mesajı ile size bildirir.
* Şu anda, dönüştürülen bir sayının imleçle söylenmesi uygulanmamaktadır ve sonuç olarak dönüştürülen sayı hecelenecektir.
* NVDA'da kurulu bazı yerel Python kitaplıklarıyla çakışmalar olduğundan, ondalık sayılardan sözcüklere dönüştürme desteği uygulanmaktadır.

## Bu eklentiyi derleme:

Not: Bu eklenti bir alt modüle bağlıdır, yani:

1. bu depoya cd: `cd num2words_nvda`
2. Modül olarak ayarlanan num2words kitaplık deposunu kopyalamak için konsola "git submodule init" ve "git submodule update" yazın.
3. Hata yoksa `scons` komutu düzgün çalışmalıdır.

## İletişim:

Bu eklentinin geliştirilmesine yardımcı olmak istiyorsanız `angelitomateocedillo@gmail.com` adresine e-posta gönderebilir veya GitHub deposunda katkılarınızı yapabilirsiniz.

---

# Değişiklik günlüğü:

## 0.2

* Şimdi sayılardan kelimelere sonuç büyük harfle yazılır.
* 'da48a319179f19b900d5b01ed394b304e94d31cf' işlemek için num2words kitaplığı güncellendi.
* Elle dönüştürme GUI'sinde num2words kitaplığı tarafından desteklenen dönüştürme modları eklendi.
* Elle dönüştürme GUI'sinde küçük düzeltmeler.
* NVDA'yı başlatırken sentezleyici dil kontrolü eklendi. Bu nedenle, dilin desteklenmemesi durumunda bu eklentinin bir kısmı devre dışı bırakılacaktır.

## 0.1

* İlk sürüm. Bazı küçük hatalar bulabilirsiniz. Eğer öyleyse, lütfen bana bildirin.