#!/usr/bin/env python3
# Matsuro Palette TR - Kurucu Uygulama v1.2
# Calistir: python MatsuroTR_Yama.pyw   (Windows: cift tik)
import os
import sys
import threading
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    import apply_patch as patcher
except Exception as e:
    raise SystemExit(f"apply_patch.py bulunamadı: {e}")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Matsuro Palette - Türkçe Yama v1.2")
        self.geometry("560x460")
        self.resizable(False, False)

        f1 = ttk.LabelFrame(self, text="Oyun klasörü (matsuro.exe'nin olduğu klasör)")
        f1.pack(fill="x", padx=10, pady=8)
        self.entry = ttk.Entry(f1, width=52)
        self.entry.pack(side="left", padx=6, pady=6, expand=True, fill="x")
        ttk.Button(f1, text="Gözat...", command=self.browse).pack(side="left", padx=3)
        ttk.Button(f1, text="Otomatik Bul", command=self.autodetect).pack(side="left", padx=3)
        ttk.Button(f1, text="Derin Arama", command=self.deep_search).pack(side="left", padx=3)

        f1b = ttk.LabelFrame(self, text="Wine prefix (sadece ek yama + Steam dışı kurulumlarda gerekli)")
        f1b.pack(fill="x", padx=10, pady=4)
        self.entry_pfx = ttk.Entry(f1b, width=52)
        self.entry_pfx.pack(side="left", padx=6, pady=6, expand=True, fill="x")
        ttk.Button(f1b, text="Gözat...", command=self.browse_pfx).pack(side="left", padx=3)
        ttk.Button(f1b, text="Otomatik Bul", command=self.autodetect_pfx).pack(side="left", padx=3)

        f2 = ttk.LabelFrame(self, text="Seçenekler")
        f2.pack(fill="x", padx=10, pady=4)
        self.mode = tk.StringVar(value="ascii")
        ttk.Radiobutton(f2, text="Sade harfler (her yerde çalışır)", value="ascii",
                        variable=self.mode).pack(anchor="w", padx=6)
        ttk.Radiobutton(f2, text="Düzgün harfler ş ğ ı İ ç ö ü (BepInEx gerekli)",
                        value="diacritic", variable=self.mode).pack(anchor="w", padx=6)
        self.do_levels = tk.BooleanVar(value=True)
        ttk.Checkbutton(f2, text="Sahne başlıklarını da yama (Ayar Odası, Bölüm...)",
                        variable=self.do_levels).pack(anchor="w", padx=6)

        f3 = ttk.Frame(self)
        f3.pack(fill="x", padx=10, pady=6)
        self.btn_install = ttk.Button(f3, text="Yamayı Kur", command=self.start_patch)
        self.btn_install.pack(side="left", padx=2)
        self.btn_ek = ttk.Button(f3, text="Ek Yamayı Kur (BepInEx)", command=self.start_ek)
        self.btn_ek.pack(side="left", padx=2)
        self.progress = ttk.Progressbar(f3, mode="indeterminate", length=150)
        self.progress.pack(side="right", padx=4)

        self.log = tk.Text(self, height=14, width=66, state="disabled")
        self.log.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.autodetect(silent=True)

    def say(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def game_dir(self):
        return Path(self.entry.get().strip().strip('"').strip("'"))

    def browse(self):
        d = filedialog.askdirectory(title="Oyun klasörünü seç (matsuro.exe'nin olduğu klasör)")
        if d:
            self.entry.delete(0, "end")
            self.entry.insert(0, d)
            self.autodetect_pfx(silent=True)

    def browse_pfx(self):
        d = filedialog.askdirectory(title="Wine prefix klasörünü seç (drive_c içeren klasör)")
        if d:
            self.entry_pfx.delete(0, "end")
            self.entry_pfx.insert(0, d)

    def find_prefix_for_game(self, game):
        """Oyun klasöründen prefix adayları: Steam compatdata, Lutris/Heroic tahminleri."""
        out = []
        try:
            for part in game.parents:
                if part.name == "steamapps":
                    c = part / "compatdata" / "1321120" / "pfx"
                    if (c / "drive_c").is_dir():
                        out.append(c)
                    break
        except Exception:
            pass
        home = Path.home()
        guesses = [home / ".wine", home / "Games" / "umu" / "umu-default"]
        hp = home / ".config" / "heroic" / "Prefixes"
        if hp.is_dir():
            try:
                guesses.extend([p for p in hp.iterdir() if (p / "drive_c").is_dir()])
            except Exception:
                pass
        for g in guesses:
            try:
                if (g / "drive_c").is_dir() and g not in out:
                    out.append(g)
            except Exception:
                continue
        return out

    def autodetect_pfx(self, silent=False):
        try:
            cands = self.find_prefix_for_game(self.game_dir())
        except Exception:
            cands = []
        if cands:
            self.entry_pfx.delete(0, "end")
            self.entry_pfx.insert(0, str(cands[0]))
            if not silent:
                self.say(f"Prefix bulundu: {cands[0]}")
        elif not silent:
            self.say("Prefix bulunamadı, Gözat ile elle seç (drive_c içeren klasör).")

    def autodetect(self, silent=False):
        for c in patcher.CANDIDATE_PATHS:
            try:
                if c.is_file():
                    self.entry.delete(0, "end")
                    self.entry.insert(0, str(c.parent.parent))
                    if not silent:
                        self.say(f"Bulundu: {c.parent.parent}")
                    return
            except Exception:
                continue
        if not silent:
            self.say("Otomatik bulunamadı, Gözat ile seç.")

    def resolve_assets(self):
        g = self.game_dir()
        if not g.is_dir():
            messagebox.showerror("Hata", "Önce geçerli bir oyun klasörü seç.")
            return None
        for cand in (g / "matsuro_Data" / "resources.assets",
                     g / "resources.assets"):
            if cand.is_file():
                return cand
        messagebox.showerror("Hata", "Klasörde matsuro_Data/resources.assets yok.")
        return None

    def deep_search(self):
        import time
        self.say("Derin arama başladı (1 dk kadar sürebilir)...")

        def scan_root(root, maxdepth, deadline, hits):
            try:
                stack = [(str(root), 0)]
                while stack:
                    if time.time() > deadline:
                        return True
                    cur, depth = stack.pop()
                    try:
                        if os.path.basename(cur) == "matsuro_Data":
                            ra = os.path.join(cur, "resources.assets")
                            if os.path.isfile(ra) and ra not in hits:
                                hits.append(ra)
                    except Exception:
                        pass
                    if depth >= maxdepth:
                        continue
                    try:
                        with os.scandir(cur) as it:
                            for e in it:
                                try:
                                    if e.is_dir(follow_symlinks=False):
                                        if e.name in ("proc", "sys", "dev"):
                                            continue
                                        stack.append((e.path, depth + 1))
                                except Exception:
                                    continue
                    except Exception:
                        continue
            except Exception:
                pass
            return False

        def job():
            try:
                home = str(Path.home())
                roots = [(os.path.expanduser("~/.wine/drive_c"), 6),
                         (os.path.join(home, "Games"), 6),
                         (os.path.expanduser("~/.local/share/Steam"), 5),
                         (os.path.expanduser("~/Steam"), 4),
                         ("/mnt", 7), ("/media", 7)]
                deadline = time.time() + 90
                hits = []
                for r, d in roots:
                    if time.time() > deadline or not os.path.isdir(r):
                        continue
                    scan_root(r, d, deadline, hits)
                seen, uniq = set(), []
                for h in hits:
                    if h not in seen:
                        seen.add(h)
                        uniq.append(h)
                if not uniq:
                    self.say("Bulunamadı. Gözat ile elle seç.")
                    return
                for u in uniq:
                    self.say("Bulundu: " + u)
                game = str(Path(uniq[0]).parent.parent)
                self.entry.delete(0, "end")
                self.entry.insert(0, game)
                self.autodetect_pfx(silent=True)
            except Exception as e:
                self.say(f"Arama hatası: {e}")
        threading.Thread(target=job, daemon=True).start()

    def run_in_thread(self, fn):
        self.btn_install.configure(state="disabled")
        self.btn_ek.configure(state="disabled")
        self.progress.start(12)

        def wrap():
            try:
                fn()
            except SystemExit:
                pass
            except Exception:
                self.say("HATA:\n" + traceback.format_exc())
            finally:
                self.progress.stop()
                self.btn_install.configure(state="normal")
                self.btn_ek.configure(state="normal")
        threading.Thread(target=wrap, daemon=True).start()

    def start_patch(self):
        target = self.resolve_assets()
        if target is None:
            return

        def job():
            argv = []
            if self.mode.get() == "diacritic":
                argv.append("--diacritic")
            if not self.do_levels.get():
                argv.append("--no-levels")
            argv.append(str(target))
            self.say(f"$ apply_patch.py {' '.join(argv)}")
            old = sys.argv
            sys.argv = ["apply_patch.py"] + argv
            try:
                patcher.main()
            finally:
                sys.argv = old
            self.say("BİTTİ. Oyunda dil Turkce seç.")
        self.run_in_thread(job)

    def start_ek(self):
        target = self.resolve_assets()
        if target is None:
            return

        def job():
            import urllib.request
            import zipfile
            import tempfile
            game = target.parent.parent
            urls = {
                "bepinex.zip": "https://github.com/BepInEx/BepInEx/releases/download/v5.4.23.5/BepInEx_win_x64_5.4.23.5.zip",
                "autotrans.zip": "https://github.com/bbepis/XUnity.AutoTranslator/releases/download/v5.6.2/XUnity.AutoTranslator-BepInEx-5.6.2.zip",
            }
            tmpd = Path(tempfile.mkdtemp(prefix="matsuro_ek"))
            try:
                for name, url in urls.items():
                    self.say(f"İndiriliyor: {name}")
                    urllib.request.urlretrieve(url, tmpd / name)
                    with zipfile.ZipFile(tmpd / name) as z:
                        z.extractall(game)
                cfgdir = game / "BepInEx" / "config"
                cfgdir.mkdir(parents=True, exist_ok=True)
                (cfgdir / "AutoTranslatorConfig.ini").write_text(
                    "[Service]\nEndpoint=GoogleTranslate\n\n[General]\nLanguage=en\n"
                    "FromLanguage=en\n\n[Behaviour]\nMinDialogueChars=1\nOverrideFont=M+ 1p\n",
                    encoding="utf-8")
                self.say("BepInEx kuruldu, ayar yazıldı.")
            except Exception:
                self.say("İndirme/kurulum HATASI:\n" + traceback.format_exc())
                return
            # font: önce kutudaki prefix, yoksa otomatik bul; Windows'ta klasörü aç
            font_src = HERE / "fonts" / "MPlus1p-Regular.ttf"
            pfx_txt = self.entry_pfx.get().strip().strip('"').strip("'")
            if sys.platform.startswith("win"):
                os.startfile(font_src.parent)  # noqa
                self.say("fonts klasörü açıldı: MPlus1p-Regular.ttf dosyasına çift tıklayıp Yükle de.")
            else:
                pfx = Path(pfx_txt) if pfx_txt else None
                if pfx is None or not (pfx / "drive_c").is_dir():
                    cands = self.find_prefix_for_game(game)
                    pfx = cands[0] if cands else None
                fonts_dir = pfx / "drive_c" / "windows" / "Fonts" if pfx else None
                if fonts_dir and fonts_dir.is_dir():
                    import shutil
                    shutil.copy2(font_src, fonts_dir / "MPlus1p-Regular.ttf")
                    self.say(f"Font kuruldu: {fonts_dir}")
                    self.say('Steam ise başlatma seçeneği: WINEDLLOVERRIDES="winhttp=n,b" %command%')
                    self.say('Lutris ise: Runner options > DLL overrides > winhttp=n,b')
                else:
                    self.say("Prefix bulunamadı: MPlus1p-Regular.ttf dosyasını Proton/Wine prefixindeki drive_c/windows/Fonts içine elle kopyala.")
            self.say("Şimdi düzgün harfli metinler yazılıyor...")
            old = sys.argv
            sys.argv = ["apply_patch.py", "--diacritic", str(target)]
            try:
                patcher.main()
            finally:
                sys.argv = old
            self.say("EK YAMA BİTTİ. Oyunda ALT+F ile fontu karşılaştır.")
        self.run_in_thread(job)


if __name__ == "__main__":
    App().mainloop()
