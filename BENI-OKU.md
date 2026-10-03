# Matsuro Palette — Türkçe Yama v1.2

STEAM + GOG uyumlu, 519 metin dosyası + 8 sahne başlığı. Çeviri: Zorti + OpenCode.

## En kolayı: TEK TIK

- **Windows:** `KUR-TEK-TIK.bat` dosyasına çift tıkla, oyun klasörünü seç, bekle.
  Python dahil her şeyi kendisi halleder, bir şey kurmana gerek yok.
- **Linux:** `python3 MatsuroTR_Yama.pyw` çalıştır (grafik ekran açılır, klasörü seç).

## Windows'ta kurulum (elle, alternatif)

1. **Python kur:** python.org → Downloads → Windows → en güncel 3.x'i indir, kurarken
   alttaki **"Add python.exe to PATH" tikini İŞARETLE**, Install Now de.
   (Microsoft Store'daki Python da olur ama site sürümü önerilir.)
2. **UnityPy kur:** Başlat menüsüne `cmd` yaz, Enter. Açılan siyah pencereye şunu
   yapıştırıp Enter'a bas:
   `py -m pip install UnityPy`
   `Successfully installed` yazması lazım.
3. **Yama klasörünü aç**, `MatsuroTR_Yama.pyw` dosyasına **çift tıkla**.
   Açılmazsa sağ tık > Birlikte aç > Python seç.
4. Uygulamada **Gözat** bas, oyun klasörünü seç:
   - Steam: `C:\Program Files (x86)\Steam\steamapps\common\matsuro`
     (D'ye kuruluysa `D:\Steam\steamapps\common\matsuro` — içinde `matsuro.exe` olmalı)
   - Korsan/portable: oyunu açtığın klasör (içinde `matsuro.exe` + `matsuro_Data` var)
5. **Yamayı Kur** bas, logda `Doğrulama OK` yazana kadar bekle (1-2 dk sürebilir).
6. Oyunu aç, dil **Turkce** seç. Oldu!

**Düzgün harfler istenirse** (ş ğ ı İ ç ö ü): uygulamada **Ek Yamayı Kur** bas,
sonra `fonts` klasöründeki `MPlus1p-Regular.ttf` dosyasına çift tıklayıp **Yükle** de.
Oyunda `ALT+F` ile eski/yeni fontu karşılaştır.

**Sorun çıkarsa:**
- `'py' tanınmıyor`: Python kurulurken PATH tiki işaretlenmemiş. Python'ı kaldırıp
  1. adımdaki tikle tekrar kur.
- `UnityPy yok` derse 2. adımı tekrarla.
- Antivirüs `winhttp.dll` için uyarırsa (sadece ek yamada): dosyaya izin ver,
  BepInEx oyun modlarının standart dosyasıdır.
- ` tkinter yok` hatası: python.org sürümünü kur (Store sürümünde bazen eksik olur).

## Hızlı kurulum (Linux — uygulama)

1. `pip install UnityPy` (`pip install --break-system-packages UnityPy` gerekebilir).
2. `MatsuroTR_Yama.pyw` dosyasını çalıştır, **Gözat** ile oyun klasörünü seç
   (bulunamazsa **Otomatik Bul**), **Yamayı Kur** bas.
3. Oyunda dili **Turkce** seç.

Prefix'in farklı (korsan/Lutris/Heroic) ise oyunu da prefix'i de Gözat ile elle seç,
uygulama gerisini halleder. Komut satırı istersen: `python apply_patch.py "oyun klasörü"` (ayrıntılar: `python apply_patch.py --help` gibi `--diacritic`, `--levels-only`, `--no-levels`).

Oyun dosyaların otomatik yedeklenir (`*.YEDEK`). Oyunda dili **Turkce** seç.

## Ek yama (düzgün harfler: ş ğ ı İ ç ö ü)

Base yaması sade harf yazar çünkü oyunun kendi fontunda bu harfler yok.
Düzgün harfler için:

- Windows: uygulamada **Ek Yamayı Kur** bas — BepInEx + fontu kurar.
  `fonts/MPlus1p-Regular.ttf` dosyasına **SAĞ TIKLA > Tüm kullanıcılar için yükle** de (yönetici onayı ister). Sadece "Yükle" dersen oyun fontu görmeyebilir!
- Linux: uygulamada **Ek Yamayı Kur** bas — her şeyi otomatik yapar.
  Sonra Steam'de oyuna sağ tık > Özellikler > Başlatma Seçenekleri:
  `WINEDLLOVERRIDES="winhttp=n,b" %command%`

Oyunda `ALT+F` ile eski/yeni fontu karşılaştırabilirsin.

## Wine / Lutris / Heroic / Bottles kullananlar (dosyayı bulamayanlar)

1. Uygulamada **Derin Arama** bas — oyunu diskte arar, bulunca kutuya yazar.
2. Olmazsa uygulamadaki **Derin Arama** düğmesine bas.
3. Klasik yerler: `~/.wine/drive_c/...`, `~/Games`, Lutris prefix içi `drive_c`,
   Bottles: `~/.var/app/com.usebottles.bottles/data/bottles`,
   Heroic: `~/.config/heroic/Prefixes`.

## Geri alma

- Metinler: `matsuro_Data/resources.assets.YEDEK` dosyasını `resources.assets` yap.
- Sahne başlıkları: `level*.YEDEK` dosyalarını geri adlandır.
- Ek yama: `BepInEx`, `winhttp.dll`, `doorstop_config.ini` sil.

## İçindekiler

- `apply_patch.py` — yama motoru (`--ascii` varsayılan, `--diacritic`, `--levels-only`, `--no-levels`)
- `matsuro_tr_full.json` — 519 düzgün harfli çeviri
- `matsuro_tr_full_ascii.json` — 519 sade harfli çeviri
- `fonts/MPlus1p-Regular.ttf` — oyundan çıkan, Türkçesi tam font
- `MatsuroTR_Yama.pyw` — grafik kurucu (klasör seçmeli, ek yama dahil)

## Notlar

- Bu paket oyun dosyası İÇERMEZ; yamayı kendi oyun kopyana uygular.
- Diğer diller (DE/FR/JA/ZH/RU/KO) aynen durur, sadece English slotu Türkçe olur.
- BepInEx ve XUnity.AutoTranslator bu pakette YOKTUR; ek-yama betikleri resmi sürümlerinden indirir.

---

## EN summary

Turkish patch for Matsuro Palette (Steam + GOG): 519 translated text assets + 8 scene headers.
Base patch uses ASCII-safe Turkish (works everywhere). The add-on (Ek Yamayı Kur button)
installs BepInEx + XUnity.AutoTranslator with a font override for proper ş/ğ/ı/İ/ç/ö/ü.
No game files included; the patcher modifies your own copy (auto-backup).

---
**NOT:** Bu yama yapay zekâ desteğiyle hazırlandı. Çevirideki hatalar
Zorti tarafından bildirilip yine yapay zekâ tarafından düzeltildi.
Hâlâ yazım/çeviri hatası olabilir; görürseniz lütfen bildirin.

