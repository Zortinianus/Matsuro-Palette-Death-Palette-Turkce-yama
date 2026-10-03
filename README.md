# Matsuro Palette — Türkçe Yama

> Steam + GOG uyumlu fan çevirisi. Python tabanlı kurucu + BepInEx ek-yamasıyla düzgün Türkçe harfler.

STEAM + GOG uyumlu, 519 metin dosyası + 8 sahne başlığı. Çeviri: Zorti + OpenCode.

## Kurulum (Windows + Linux, tek yöntem)

1. **Python 3.10+** kur ([python.org](https://www.python.org/downloads/) — kurarken
   **"Add python.exe to PATH"** tikini işaretle; Linux'ta genelde hazır gelir).
2. UnityPy kur:
   - Windows: Başlat > `cmd` > `py -m pip install UnityPy`
   - Linux: `pip install --break-system-packages UnityPy`
3. `MatsuroTR_Yama.pyw` dosyasını çalıştır (Windows: çift tık; Linux: `python3 MatsuroTR_Yama.pyw`).
   Açılmazsa: `sudo apt install python3-tk` (Linux) veya sağ tık > Birlikte aç > Python (Windows).
4. Uygulamada **Gözat** ile oyun klasörünü seç (içinde `matsuro.exe` olmalı;
   bulunamazsa **Otomatik Bul** / **Derin Arama**), **Yamayı Kur** bas.
5. Logda **Doğrulama OK** yazana kadar bekle (1-2 dk), oyunda dil **Turkce** seç.

Korsan / Lutris / Heroic / Wine: oyunu da prefix'i de Gözat ile elle seç,
uygulama gerisini halleder. Komut satırı istersen:
`python apply_patch.py "oyun klasörü"` (seçenekler: `--diacritic`, `--levels-only`, `--no-levels`).

Oyun dosyaların otomatik yedeklenir (`*.YEDEK`).

## Ek yama (düzgün harfler: ş ğ ı İ ç ö ü)

Base yama sade harf yazar çünkü oyunun kendi fontunda bu harfler yok.
Düzgün harfler için uygulamada **Ek Yamayı Kur** bas:

- `fonts/MPlus1p-Regular.ttf` dosyasını sisteme kur:
  - Windows: dosyaya **SAĞ TIKLA > Tüm kullanıcılar için yükle** (sadece "Yükle" yetmez!).
  - Linux: Proton prefixindeki `drive_c/windows/Fonts` içine kopyala (uygulama dener).
- Linux + Steam'de ek olarak oyuna sağ tık > Özellikler > Başlatma Seçenekleri:
  `WINEDLLOVERRIDES="winhttp=n,b" %command%`

Oyunda `ALT+F` ile eski/yeni fontu karşılaştırabilirsin.

## Geri alma

- Metinler: `matsuro_Data/resources.assets.YEDEK` dosyasını `resources.assets` yap.
- Sahne başlıkları: `level*.YEDEK` dosyalarını geri adlandır.
- Ek yama: `BepInEx`, `winhttp.dll`, `doorstop_config.ini` sil.

## İçindekiler

- `MatsuroTR_Yama.pyw` — grafik kurucu (klasör seçmeli, derin aramalı, ek yamalı)
- `apply_patch.py` — komut satırı yama motoru
- `matsuro_tr_full.json` — 519 düzgün harfli çeviri
- `matsuro_tr_full_ascii.json` — 519 sade harfli çeviri
- `fonts/` — Türkçesi tam yazı tipi
- `BENI-OKU.md` / `BILGI-OKU.txt` — Windows Not Defteri uyumlu belgeler

## Notlar

- Bu paket oyun dosyası İÇERMEZ; yamayı kendi oyun kopyana uygular.
- Diğer diller (DE/FR/JA/ZH/RU/KO) aynen durur, sadece English yuvası Türkçe olur.
- BepInEx ve XUnity.AutoTranslator bu pakette YOKTUR; ek-yama düğmesi resmi
  sürümlerinden indirir (lisansları için kendi sayfalarına bak).

**NOT:** Bu yama yapay zekâ desteğiyle hazırlandı. Çevirideki hatalar
Zorti tarafından bildirilip yine yapay zekâ tarafından düzeltildi.
Hâlâ yazım/çeviri hatası olabilir; görürseniz lütfen bildirin.

---

## EN summary

Turkish patch for Matsuro Palette (Steam + GOG): 519 translated text assets + 8 scene headers.
Needs Python 3.10+ and UnityPy: run `MatsuroTR_Yama.pyw`, pick the game folder, install.
Base patch uses ASCII-safe Turkish (works everywhere); the in-app add-on installs BepInEx +
a font override for proper Turkish glyphs (ş/ğ/ı/İ/ç/ö/ü). No game files included;
the patcher modifies your own copy (auto-backup).
