#!/usr/bin/env python3
# Matsuro Palette Türkçe Yama - Patcher v1.2
# Kullanım:
#   python apply_patch.py [SEÇENEK] [".../matsuro_Data/resources.assets"]
# Seçenekler:
#   --ascii      Sade harfler (ş->s, ğ->g ...). Her kurulumda çalışır. (VARSAYILAN)
#   --diacritic  Düzgün harfler. BepInEx + font ek-yaması gerekir (README).
#   --no-levels  Sahne başlıklarını (level*) atla, sadece metinleri yama.
#   --levels-only  Sadece sahne başlıklarını yama.
import json, sys, shutil
from pathlib import Path

VERSION = "1.2"

HERE = Path(__file__).parent
TR_JSON = HERE / "matsuro_tr_full.json"
TR_JSON_ASCII = HERE / "matsuro_tr_full_ascii.json"

# level dosyalarındaki sahne başlıkları (hepsi AYNI bayt boyunda, uzunluk öneki korunur)
# menü fontunda düzgün harf yok -> ASCII yazılır. her girdi: (dosya, [aranacak desenler], yeni)
LEVEL_JOBS = [
    ("level14", [b"\x0b\x00\x00\x00Option Room", b"\x0b\x00\x00\x00Ayar Odas\xc4\xb1"], b"\x0b\x00\x00\x00Ayar Odasi "),
    ("level27", [b"\x0a\x00\x00\x00Sound Room", b"\x0a\x00\x00\x00Ses Odas\xc4\xb1"], b"\x0a\x00\x00\x00Ses Odasi "),
    ("level10", [b"\x07\x00\x00\x00Chapter", b"\x07\x00\x00\x00B\xc3\xb6l\xc3\xbcm"], b"\x07\x00\x00\x00Bolum  "),
    ("level18", [b"\x07\x00\x00\x00Chapter", b"\x07\x00\x00\x00B\xc3\xb6l\xc3\xbcm"], b"\x07\x00\x00\x00Bolum  "),
    ("level31", [b"\x09\x00\x00\x00Chapter X", b"\x09\x00\x00\x00B\xc3\xb6l\xc3\xbcm X"], b"\x09\x00\x00\x00Bolum  X "),
    ("level5", [b"\x07\x00\x00\x00Gallery"], b"\x07\x00\x00\x00Galeri "),
    ("level6", [b"\x07\x00\x00\x00Gallery"], b"\x07\x00\x00\x00Galeri "),
]
LEVEL31_BARE = (b"\x07\x00\x00\x00Chapter", b"\x07\x00\x00\x00Bolum  ")

CANDIDATE_PATHS = [
    # GOG / Lutris (bu makine)
    Path("/home/zorti/Games/umu/umu-default/drive_c/GOG Games/Matsuro Palette/matsuro_Data/resources.assets"),
    # Steam Linux
    Path.home() / ".steam/steam/steamapps/common/Matsuro Palette/matsuro_Data/resources.assets",
    Path.home() / ".local/share/Steam/steamapps/common/Matsuro Palette/matsuro_Data/resources.assets",
    Path.home() / "Steam/steamapps/common/Matsuro Palette/matsuro_Data/resources.assets",
    # Lutris alt disk
    Path("/mnt/e393597c-9524-4abf-8c3c-4b98baccf2e2/oyunlar"),
    # Windows Steam varsayılanları (Windows'ta çalışırsa)
    Path("C:/Program Files (x86)/Steam/steamapps/common/Matsuro Palette/matsuro_Data/resources.assets"),
    Path("C:/Program Files/Steam/steamapps/common/Matsuro Palette/matsuro_Data/resources.assets"),
    Path("D:/Steam/steamapps/common/Matsuro Palette/matsuro_Data/resources.assets"),
    # GOG Windows
    Path("C:/GOG Games/Matsuro Palette/matsuro_Data/resources.assets"),
]

def find_game_file(cli_arg=None):
    if cli_arg:
        p = Path(cli_arg)
        if p.is_file():
            return p
        # klasör verildiyse resources.assets'i dene
        cand = p / "matsuro_Data" / "resources.assets"
        if cand.is_file():
            return cand
        cand2 = p / "resources.assets"
        if cand2.is_file():
            return cand2
        print(f"Verilen yol bulunamadı: {cli_arg}")
        sys.exit(1)
    for c in CANDIDATE_PATHS:
        if c.is_file() and c.name == "resources.assets":
            return c
    # geniş tara: home altında matsuro_Data ara (yavaş olabilir, max 3 derinlik)
    print("Otomatik oyun yolu bulunamadı.")
    print('Kullanım: python apply_patch.py "OYUN_KLASÖRÜ/matsuro_Data/resources.assets"')
    sys.exit(1)

def patch_levels(data_dir):
    """Sahne başlıklarını yama (idempotent: zaten yamalıysa atlar). True/False döndürür."""
    ok = True
    for fn, olds, new in LEVEL_JOBS:
        if isinstance(olds, (bytes, bytearray)):
            olds = [olds]
        for old in olds:
            assert len(old) == len(new), fn
        p = data_dir / fn
        if not p.is_file():
            print(f"  {fn}: dosya yok, atlandı")
            continue
        data = p.read_bytes()
        changed = False
        for old in olds:
            if old in data:
                if not changed:
                    bak = p.with_name(fn + ".YEDEK")
                    if not bak.is_file():
                        shutil.copy2(p, bak)
                    changed = True
                data = data.replace(old, new)
        if changed:
            p.write_bytes(data)
            print(f"  {fn}: başlık yamalandı")
        elif new in data:
            print(f"  {fn}: zaten yamalı")
        else:
            print(f"  {fn}: UYARI desen bulunamadı (sürüm farklı olabilir)")
            ok = False
        if fn == "level31":
            bo, bn = LEVEL31_BARE
            data = p.read_bytes()
            if bn in data and bo not in data:
                print("  level31-çıplak: zaten yamalı")
            elif bo in data:
                p.write_bytes(data.replace(bo, bn))
                print("  level31-çıplak: başlık yamalandı")
            else:
                print("  level31-çıplak: UYARI desen bulunamadı")
                ok = False
    return ok


def main():
    args = [a for a in sys.argv[1:] if a.startswith("--")]
    rest = [a for a in sys.argv[1:] if not a.startswith("--")]
    use_ascii = "--diacritic" not in args
    do_texts = "--levels-only" not in args
    do_levels = "--no-levels" not in args
    json_path = TR_JSON_ASCII if use_ascii else TR_JSON
    if not json_path.is_file():
        # tek dosyalık dağıtımlarda ascii yoksa diacritic'e düş
        json_path = TR_JSON if json_path == TR_JSON_ASCII else TR_JSON_ASCII
    print(f"Matsuro Palette TR yama {VERSION} ({'sade' if use_ascii else 'düzgün'} harfler)")

    try:
        import UnityPy
    except ImportError:
        if sys.platform.startswith("win"):
            print("UnityPy yok. Kur: py -m pip install UnityPy")
        else:
            print("UnityPy yok. Kur: pip install UnityPy")
        sys.exit(1)

    arg = rest[0] if rest else None
    target = find_game_file(arg)
    print(f"Hedef: {target}")

    if not json_path.is_file():
        print(f"Çeviri dosyası yok: {json_path}")
        sys.exit(1)

    tr_list = json.loads(json_path.read_text(encoding="utf-8"))
    tr_map = {d["path_id"]: d for d in tr_list}
    print(f"Çeviri kaydı: {len(tr_map)} TextAsset")

    # yedek
    backup = target.with_name("resources.assets.YEDEK")
    if not backup.is_file():
        shutil.copy2(target, backup)
        print(f"Yedek alındı: {backup}")
    else:
        print(f"Yedek zaten var: {backup}")

    if not do_texts:
        print("Metinler atlandı (--levels-only).")
        if do_levels:
            print("Sahne başlıkları:")
            patch_levels(target.parent)
        print("Bitti.")
        return

    env = UnityPy.load(str(target))
    applied, skipped, missing = 0, 0, []
    # path_id ile uygula
    objs_by_id = {}
    for o in env.objects:
        if o.type.name == "TextAsset":
            objs_by_id[o.path_id] = o

    for pid, entry in tr_map.items():
        o = objs_by_id.get(pid)
        # fallback: path_id yoksa isme göre ara (Steam sürüm farkı)
        if o is None:
            for oo in env.objects:
                if oo.type.name != "TextAsset":
                    continue
                try:
                    if oo.read().m_Name == entry["name"]:
                        # aynı isimde birden fazla var, ilk boş eşleşmeyi alma;
                        # İngilizce içeriğe benzeyeni tercih et (kısa heuristik)
                        o = oo
                        break
                except Exception:
                    continue
        if o is None:
            missing.append(pid)
            continue
        try:
            d = o.read()
            cur = d.m_Script.decode("utf-8", errors="ignore") if isinstance(d.m_Script, bytes) else str(d.m_Script)
            new = entry["text_tr"]
            if cur == new or cur.rstrip("\n") == new.rstrip("\n"):
                skipped += 1
                continue
            # güvenlik: satır sayısı aynı olmalı (sondaki boşluk farkını görmezden gel)
            if cur.rstrip("\n").count("\n") != new.rstrip("\n").count("\n"):
                print(f"UYARI {pid} {entry['name']}: satır sayısı farklı, atlanıyor")
                missing.append(pid)
                continue
            d.m_Script = new
            d.save()
            applied += 1
        except Exception as e:
            print(f"HATA {pid}: {e}")
            missing.append(pid)

    data = env.file.save()
    target.write_bytes(data)
    print(f"Yazıldı: {target} ({len(data)} bayt)")
    print(f"Uygulanan: {applied}, zaten Türkçe: {skipped}, eksik: {len(missing)}")
    if missing:
        print("Eksik path_id örnek:", missing[:10])

    # doğrulama
    env2 = UnityPy.load(str(target))
    bad = []
    for o in env2.objects:
        if o.type.name != "TextAsset":
            continue
        if o.path_id in tr_map:
            try:
                cur = o.read().m_Script
                cur = cur.decode("utf-8", errors="ignore") if isinstance(cur, bytes) else str(cur)
                want = tr_map[o.path_id]["text_tr"]
                if cur != want and cur.rstrip("\n") != want.rstrip("\n"):
                    bad.append(o.path_id)
            except Exception:
                bad.append(o.path_id)
    if bad:
        print(f"Doğrulama BAŞARISIZ: {bad[:10]}")
        sys.exit(2)
    if do_texts:
        print("Metin doğrulama OK.")

    if do_levels:
        print("Sahne başlıkları:")
        if not patch_levels(target.parent):
            print("UYARI: bazı başlıklar yamalanamadı (oyun sürümün farklı olabilir)")
    if not use_ascii:
        print("NOT: düzgün harfler için BepInEx ek-yaması gerekir (README).")
    print("Bitti. Oyunda dili Turkce seçip oyna.")

if __name__ == "__main__":
    main()
