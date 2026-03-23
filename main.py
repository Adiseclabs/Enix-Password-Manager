"""
Enix Password Manager v1.0.0
Developed by Enix Software India - https://www.enixsoftwareindia.com/
@Aditya Bhosale  |  Internal Use Only
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, base64, hashlib, secrets, string, re
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# ──────────────────────────────────────────────
#  EMBEDDED LOGOS
# ──────────────────────────────────────────────
_LOGO_B64 = "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"
_LOGO_SM  = "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"
_ICON_B64 = "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"
_ICO_B64  = "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"


# ──────────────────────────────────────────────
#  CONSTANTS
# ──────────────────────────────────────────────
APP_NAME  = "Enix Password Manager"
VERSION   = "1.0.0"
DEVELOPER = "Aditya Bhosale"
WEBSITE   = "https://www.enixsoftwareindia.com/"
APP_DIR     = os.path.join(os.path.expanduser("~"), ".enix_pm")
CONFIG_FILE = os.path.join(APP_DIR, "config.json")
DATA_FILE   = os.path.join(APP_DIR, "vault.enix")
os.makedirs(APP_DIR, exist_ok=True)

# ──────────────────────────────────────────────
#  THEME
# ──────────────────────────────────────────────
C = {
    "bg":       "#0D0F14",
    "surface":  "#161A23",
    "surface2": "#1E2433",
    "border":   "#2A3148",
    "accent":   "#4F8EF7",
    "accent2":  "#7C5CFC",
    "success":  "#29D17C",
    "warning":  "#F5A623",
    "danger":   "#F75F5F",
    "text":     "#E8EAF0",
    "text2":    "#8892A4",
    "text3":    "#4A5568",
    "white":    "#FFFFFF",
    "gold":     "#F5C842",
}
FONT_HEAD   = ("Segoe UI", 13, "bold")
FONT_LABEL  = ("Segoe UI", 10)
FONT_MONO   = ("Consolas", 11)
FONT_SMALL  = ("Segoe UI", 9)
FONT_BUTTON = ("Segoe UI", 10, "bold")


# ══════════════════════════════════════════════
#  CRYPTO ENGINE
# ══════════════════════════════════════════════
class CryptoEngine:
    ITERATIONS = 390_000

    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                         salt=salt, iterations=CryptoEngine.ITERATIONS)
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    @staticmethod
    def hash_master(password: str, salt: bytes) -> str:
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, CryptoEngine.ITERATIONS)
        return base64.b64encode(dk).decode()

    @staticmethod
    def encrypt(data: str, key: bytes) -> str:
        return Fernet(key).encrypt(data.encode()).decode()

    @staticmethod
    def decrypt(token: str, key: bytes) -> str:
        return Fernet(key).decrypt(token.encode()).decode()

    @staticmethod
    def gen_password(length=20, upper=True, lower=True, digits=True, symbols=True) -> str:
        SYM  = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        pool, req = "", []
        if upper:   pool += string.ascii_uppercase; req.append(secrets.choice(string.ascii_uppercase))
        if lower:   pool += string.ascii_lowercase; req.append(secrets.choice(string.ascii_lowercase))
        if digits:  pool += string.digits;          req.append(secrets.choice(string.digits))
        if symbols: pool += SYM;                    req.append(secrets.choice(SYM))
        if not pool: pool = string.ascii_letters + string.digits
        rest = [secrets.choice(pool) for _ in range(max(0, length - len(req)))]
        pwd  = req + rest
        secrets.SystemRandom().shuffle(pwd)
        return "".join(pwd)


# ══════════════════════════════════════════════
#  VAULT
# ══════════════════════════════════════════════
class Vault:
    def __init__(self):
        self.key:     bytes | None = None
        self.entries: list         = []
        self._salt:   bytes | None = None

    def is_configured(self): return os.path.exists(CONFIG_FILE)

    def setup(self, master: str):
        salt  = os.urandom(32)
        hash_ = CryptoEngine.hash_master(master, salt)
        with open(CONFIG_FILE, "w") as f:
            json.dump({"salt": base64.b64encode(salt).decode(),
                       "hash": hash_, "created": datetime.now().isoformat()}, f)
        self._salt = salt
        self.key   = CryptoEngine._derive_key(master, salt)
        self.entries = []
        self._save()

    def unlock(self, master: str) -> bool:
        with open(CONFIG_FILE) as f: cfg = json.load(f)
        salt = base64.b64decode(cfg["salt"])
        if CryptoEngine.hash_master(master, salt) != cfg["hash"]: return False
        self._salt = salt
        self.key   = CryptoEngine._derive_key(master, salt)
        self._load()
        return True

    def lock(self): self.key = None; self.entries = []

    def add(self, entry: dict):
        entry["id"] = secrets.token_hex(8)
        entry["created"] = entry["updated"] = datetime.now().isoformat()
        self.entries.append(entry); self._save()

    def update(self, eid: str, data: dict):
        for e in self.entries:
            if e["id"] == eid:
                e.update(data); e["updated"] = datetime.now().isoformat()
        self._save()

    def delete(self, eid: str):
        self.entries = [e for e in self.entries if e["id"] != eid]; self._save()

    def search(self, q: str) -> list:
        q = q.lower()
        return [e for e in self.entries if
                q in e.get("title","").lower() or q in e.get("username","").lower() or
                q in e.get("url","").lower()   or q in e.get("category","").lower()]

    def _save(self):
        if self.key is None: return
        with open(DATA_FILE, "w") as f:
            f.write(CryptoEngine.encrypt(json.dumps(self.entries), self.key))

    def _load(self):
        if not os.path.exists(DATA_FILE): self.entries = []; return
        try:
            with open(DATA_FILE) as f:
                self.entries = json.loads(CryptoEngine.decrypt(f.read(), self.key))
        except Exception: self.entries = []


# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════
class IconButton(tk.Button):
    _ST = {
        "primary": ("#4F8EF7","#FFFFFF","#3A7AE8"),
        "success": ("#29D17C","#FFFFFF","#22B86A"),
        "danger":  ("#F75F5F","#FFFFFF","#E04A4A"),
        "ghost":   ("#1E2433","#8892A4","#2A3148"),
        "gold":    ("#F5C842","#0D0F14","#DDB52E"),
    }
    def __init__(self, parent, text, command=None, style="primary", **kw):
        bg, fg, abg = self._ST.get(style, self._ST["primary"])
        super().__init__(parent, text=text, command=command, font=FONT_BUTTON,
                         bg=bg, fg=fg, activebackground=abg, activeforeground=fg,
                         relief="flat", bd=0, cursor="hand2", padx=14, pady=7, **kw)
        self._bg, self._abg = bg, abg
        self.bind("<Enter>", lambda e: self.config(bg=self._abg))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg))


class StrengthBar(tk.Frame):
    _COLORS = ["#F75F5F","#F75F5F","#F5A623","#F5A623","#29D17C"]
    _LABELS = ["","Very Weak","Weak","Fair","Strong","Very Strong"]
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=C["surface"], **kw)
        self._bars = []
        for _ in range(5):
            b = tk.Frame(self, width=28, height=6, bg=C["border"])
            b.pack(side="left", padx=2); b.pack_propagate(False)
            self._bars.append(b)
        self._lbl = tk.Label(self, text="", font=FONT_SMALL, fg=C["text2"], bg=C["surface"])
        self._lbl.pack(side="left", padx=6)

    def update_strength(self, pwd: str):
        s = sum([len(pwd)>=8, len(pwd)>=14,
                 bool(re.search(r"[A-Z]",pwd)), bool(re.search(r"\d",pwd)),
                 bool(re.search(r"[^A-Za-z0-9]",pwd))])
        for i, b in enumerate(self._bars):
            b.config(bg=self._COLORS[s-1] if s>0 and i<s else C["border"])
        self._lbl.config(text=self._LABELS[s] if s else "",
                         fg=self._COLORS[s-1] if s else C["text2"])


def _load_img(b64_str, size=None):
    try:
        from PIL import Image as _I, ImageTk as _IT
        import io as _io
        img = _I.open(_io.BytesIO(base64.b64decode(b64_str)))
        if size: img = img.resize(size, _I.LANCZOS)
        return _IT.PhotoImage(img)
    except Exception:
        return None


def _set_win_icon(win):
    try:
        import tempfile
        p = os.path.join(tempfile.gettempdir(), "enix_app.ico")
        if not os.path.exists(p):
            with open(p, "wb") as f: f.write(base64.b64decode(_ICO_B64))
        win.iconbitmap(default=p)
    except Exception:
        pass


# ══════════════════════════════════════════════
#  MASTER PASSWORD SCREEN
# ══════════════════════════════════════════════
class MasterScreen(tk.Toplevel):
    def __init__(self, vault, on_success, mode="unlock"):
        super().__init__()
        self.vault = vault; self.on_success = on_success; self.mode = mode
        self.title(APP_NAME); self.resizable(False, False); self.configure(bg=C["bg"])
        h = 620 if mode == "setup" else 480
        self.geometry(f"460x{h}+{(self.winfo_screenwidth()-460)//2}+{(self.winfo_screenheight()-h)//2}")
        _set_win_icon(self)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self._build(); self.grab_set()

    def _build(self):
        hdr = tk.Frame(self, bg=C["surface"], height=180)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        lf = tk.Frame(hdr, bg=C["surface"])
        lf.place(relx=0.5, rely=0.5, anchor="center")
        img = _load_img(_LOGO_B64)
        if img:
            self._logo = img
            tk.Label(lf, image=img, bg=C["surface"]).pack(pady=(0,4))
        else:
            tk.Label(lf, text="ENIX", font=("Segoe UI",20,"bold"), fg=C["accent"], bg=C["surface"]).pack()
        tk.Label(lf, text="Password Manager", font=("Segoe UI",10), fg=C["text2"], bg=C["surface"]).pack()

        body = tk.Frame(self, bg=C["bg"]); body.pack(fill="both", expand=True, padx=40, pady=20)
        tk.Label(body,
                 text="Create Master Password" if self.mode=="setup" else "Unlock Your Vault",
                 font=FONT_HEAD, fg=C["text"], bg=C["bg"]).pack(pady=(0,4))
        hint = ("Choose a strong master password.\nThis encrypts your entire vault."
                if self.mode=="setup" else "Enter your master password to access the vault.")
        tk.Label(body, text=hint, font=FONT_SMALL, fg=C["text2"],
                 bg=C["bg"], justify="center").pack(pady=(0,18))

        tk.Label(body, text="Master Password", font=FONT_LABEL,
                 fg=C["text2"], bg=C["bg"], anchor="w").pack(fill="x")
        ef = tk.Frame(body, bg=C["surface2"], highlightthickness=1,
                      highlightbackground=C["border"], highlightcolor=C["accent"])
        ef.pack(fill="x", pady=4)
        self.pwd_var = tk.StringVar()
        self.pwd_e = tk.Entry(ef, show="*", font=FONT_MONO, bg=C["surface2"],
                              fg=C["text"], insertbackground=C["accent"],
                              relief="flat", bd=8, textvariable=self.pwd_var)
        self.pwd_e.pack(side="left", fill="x", expand=True)
        self._show = False
        self._eye = tk.Button(ef, text="👁", font=("Segoe UI",10), bg=C["surface2"],
                              fg=C["text2"], relief="flat", bd=0, cursor="hand2",
                              command=self._toggle)
        self._eye.pack(side="right", padx=6)

        if self.mode == "setup":
            self.pwd_var.trace_add("write", lambda *_: self._sb.update_strength(self.pwd_var.get()))
            self._sb = StrengthBar(body); self._sb.pack(pady=(0,8))
            tk.Label(body, text="Confirm Password", font=FONT_LABEL,
                     fg=C["text2"], bg=C["bg"], anchor="w").pack(fill="x")
            cf = tk.Frame(body, bg=C["surface2"], highlightthickness=1,
                          highlightbackground=C["border"], highlightcolor=C["accent"])
            cf.pack(fill="x", pady=4)
            self.confirm_var = tk.StringVar()
            tk.Entry(cf, show="*", font=FONT_MONO, bg=C["surface2"], fg=C["text"],
                     insertbackground=C["accent"], relief="flat", bd=8,
                     textvariable=self.confirm_var).pack(fill="x")

        self.status = tk.Label(body, text="", font=FONT_SMALL, fg=C["danger"], bg=C["bg"])
        self.status.pack(pady=4)
        btn_txt = "Create Vault" if self.mode=="setup" else "Unlock  →"
        IconButton(body, btn_txt, command=self._submit, style="primary").pack(fill="x", pady=8, ipady=4)
        self.pwd_e.bind("<Return>", lambda e: self._submit())
        self.pwd_e.focus()

    def _toggle(self):
        self._show = not self._show
        self.pwd_e.config(show="" if self._show else "*")
        self._eye.config(text="🙈" if self._show else "👁")

    def _submit(self):
        pwd = self.pwd_var.get()
        if not pwd: self.status.config(text="Password cannot be empty."); return
        if self.mode == "setup":
            if len(pwd) < 8: self.status.config(text="Need at least 8 characters."); return
            if pwd != self.confirm_var.get(): self.status.config(text="Passwords do not match."); return
            self.vault.setup(pwd)
            messagebox.showinfo("Vault Created", "Your vault has been created!", parent=self)
        else:
            if not self.vault.unlock(pwd):
                self.status.config(text="Incorrect master password."); return
        self.destroy(); self.on_success()


# ══════════════════════════════════════════════
#  ADD / EDIT ENTRY DIALOG
# ══════════════════════════════════════════════
class EntryDialog(tk.Toplevel):
    CATS = ["Login","Email","Banking","Social","Work","Shopping","API Key","Note","Other"]

    def __init__(self, parent, vault, entry=None, on_save=None):
        super().__init__(parent)
        self.vault = vault; self.entry = entry; self.on_save = on_save
        self.title("Edit Entry" if entry else "Add New Entry")
        self.resizable(False, False); self.configure(bg=C["bg"])
        self.geometry(f"520x680+{(self.winfo_screenwidth()-520)//2}+{(self.winfo_screenheight()-680)//2}")
        self.grab_set(); self._build()

    def _field(self, parent, lbl, mono=True):
        f = tk.Frame(parent, bg=C["bg"]); f.pack(fill="x", pady=5)
        tk.Label(f, text=lbl, font=FONT_LABEL, fg=C["text2"], bg=C["bg"], anchor="w").pack(fill="x")
        wrap = tk.Frame(f, bg=C["surface2"], highlightthickness=1,
                        highlightbackground=C["border"], highlightcolor=C["accent"])
        wrap.pack(fill="x")
        var = tk.StringVar()
        ent = tk.Entry(wrap, textvariable=var,
                       font=FONT_MONO if mono else FONT_LABEL,
                       bg=C["surface2"], fg=C["text"],
                       insertbackground=C["accent"], relief="flat", bd=8)
        ent.pack(side="left", fill="x", expand=True)
        return var, ent, wrap

    def _build(self):
        hdr = tk.Frame(self, bg=C["surface"], height=56); hdr.pack(fill="x"); hdr.pack_propagate(False)
        icon = "✏️" if self.entry else "➕"
        tk.Label(hdr, text=f"  {icon}  {'Edit Entry' if self.entry else 'Add New Entry'}",
                 font=FONT_HEAD, fg=C["text"], bg=C["surface"]).pack(side="left", padx=16)

        body = tk.Frame(self, bg=C["bg"]); body.pack(fill="both", expand=True, padx=32, pady=16)
        self.title_var, _, _ = self._field(body, "Title / Site Name *", mono=False)
        self.user_var, _, _  = self._field(body, "Username / Email")

        # password
        pf = tk.Frame(body, bg=C["bg"]); pf.pack(fill="x", pady=5)
        tk.Label(pf, text="Password *", font=FONT_LABEL, fg=C["text2"],
                 bg=C["bg"], anchor="w").pack(fill="x")
        pw_wrap = tk.Frame(pf, bg=C["surface2"], highlightthickness=1,
                           highlightbackground=C["border"], highlightcolor=C["accent"])
        pw_wrap.pack(fill="x")
        self.pass_var = tk.StringVar(); self._show_pwd = False
        self.pass_e = tk.Entry(pw_wrap, textvariable=self.pass_var, show="*",
                               font=FONT_MONO, bg=C["surface2"], fg=C["text"],
                               insertbackground=C["accent"], relief="flat", bd=8)
        self.pass_e.pack(side="left", fill="x", expand=True)
        self._eye2 = tk.Button(pw_wrap, text="👁", font=("Segoe UI",10), bg=C["surface2"],
                               fg=C["text2"], relief="flat", bd=0, cursor="hand2",
                               command=self._toggle_pwd)
        self._eye2.pack(side="right", padx=4)
        tk.Button(pw_wrap, text="⚡ Generate", font=FONT_SMALL, bg=C["accent2"],
                  fg=C["white"], relief="flat", bd=0, cursor="hand2", padx=8, pady=2,
                  command=lambda: GenDialog(self, callback=lambda p: self.pass_var.set(p))
                  ).pack(side="right", padx=4)
        self._sb = StrengthBar(body); self._sb.pack(anchor="w")
        self.pass_var.trace_add("write", lambda *_: self._sb.update_strength(self.pass_var.get()))

        self.url_var, _, _   = self._field(body, "Website URL", mono=False)

        cf = tk.Frame(body, bg=C["bg"]); cf.pack(fill="x", pady=5)
        tk.Label(cf, text="Category", font=FONT_LABEL, fg=C["text2"],
                 bg=C["bg"], anchor="w").pack(fill="x")
        self.cat_var = tk.StringVar(value="Login")
        style = ttk.Style(); style.theme_use("clam")
        style.configure("Dark.TCombobox", fieldbackground=C["surface2"],
                        background=C["surface2"], foreground=C["text"],
                        arrowcolor=C["accent"], selectbackground=C["surface2"],
                        selectforeground=C["text"])
        ttk.Combobox(cf, textvariable=self.cat_var, values=self.CATS,
                     state="readonly", style="Dark.TCombobox",
                     font=FONT_LABEL).pack(fill="x")

        nf = tk.Frame(body, bg=C["bg"]); nf.pack(fill="x", pady=5)
        tk.Label(nf, text="Notes", font=FONT_LABEL, fg=C["text2"],
                 bg=C["bg"], anchor="w").pack(fill="x")
        self.notes_text = tk.Text(nf, height=3, font=FONT_LABEL,
                                  bg=C["surface2"], fg=C["text"],
                                  insertbackground=C["accent"], relief="flat", bd=8,
                                  highlightthickness=1, highlightbackground=C["border"],
                                  highlightcolor=C["accent"])
        self.notes_text.pack(fill="x")

        if self.entry:
            self.title_var.set(self.entry.get("title",""))
            self.user_var.set(self.entry.get("username",""))
            self.pass_var.set(self.entry.get("password",""))
            self.url_var.set(self.entry.get("url",""))
            self.cat_var.set(self.entry.get("category","Login"))
            self.notes_text.insert("1.0", self.entry.get("notes",""))

        bf = tk.Frame(body, bg=C["bg"]); bf.pack(fill="x", pady=12)
        IconButton(bf, "Cancel", command=self.destroy, style="ghost").pack(side="left")
        IconButton(bf, "Save Entry  ✓", command=self._save, style="success").pack(side="right")

    def _toggle_pwd(self):
        self._show_pwd = not self._show_pwd
        self.pass_e.config(show="" if self._show_pwd else "*")
        self._eye2.config(text="🙈" if self._show_pwd else "👁")

    def _save(self):
        t = self.title_var.get().strip(); p = self.pass_var.get()
        if not t or not p:
            messagebox.showwarning("Missing Fields", "Title and Password are required.", parent=self); return
        data = dict(title=t, username=self.user_var.get().strip(), password=p,
                    url=self.url_var.get().strip(), category=self.cat_var.get(),
                    notes=self.notes_text.get("1.0","end-1c"))
        if self.entry: self.vault.update(self.entry["id"], data)
        else:          self.vault.add(data)
        if self.on_save: self.on_save()
        self.destroy()


# ══════════════════════════════════════════════
#  PASSWORD GENERATOR DIALOG
# ══════════════════════════════════════════════
class GenDialog(tk.Toplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.title("Password Generator"); self.resizable(False, False); self.configure(bg=C["bg"])
        self.geometry(f"440x400+{(self.winfo_screenwidth()-440)//2}+{(self.winfo_screenheight()-400)//2}")
        self.grab_set(); self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=C["surface"], height=50); hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="  ⚡  Password Generator", font=FONT_HEAD,
                 fg=C["text"], bg=C["surface"]).pack(side="left", padx=16)
        body = tk.Frame(self, bg=C["bg"]); body.pack(fill="both", expand=True, padx=28, pady=16)

        lf = tk.Frame(body, bg=C["bg"]); lf.pack(fill="x", pady=8)
        tk.Label(lf, text="Length", font=FONT_LABEL, fg=C["text2"], bg=C["bg"]).pack(side="left")
        self.len_var = tk.IntVar(value=20)
        self._ll = tk.Label(lf, text="20", font=FONT_MONO, fg=C["accent"], bg=C["bg"], width=3)
        self._ll.pack(side="right")
        def on_len(v):
            self._ll.config(text=str(int(float(v)))); self._generate()
        tk.Scale(lf, from_=8, to=64, orient="horizontal", variable=self.len_var,
                 showvalue=False, bg=C["bg"], fg=C["text2"], troughcolor=C["border"],
                 activebackground=C["accent"], highlightthickness=0,
                 command=on_len).pack(fill="x", expand=True, padx=8)

        self.upper_v  = tk.BooleanVar(value=True)
        self.lower_v  = tk.BooleanVar(value=True)
        self.digit_v  = tk.BooleanVar(value=True)
        self.symbol_v = tk.BooleanVar(value=True)
        for var, txt in [(self.upper_v,"Uppercase  A-Z"),(self.lower_v,"Lowercase  a-z"),
                         (self.digit_v,"Numbers  0-9"),(self.symbol_v,"Symbols  !@#...")]:
            r = tk.Frame(body, bg=C["bg"]); r.pack(fill="x", pady=2)
            tk.Checkbutton(r, variable=var, text=txt, font=FONT_LABEL,
                           fg=C["text"], bg=C["bg"], selectcolor=C["surface2"],
                           activebackground=C["bg"], activeforeground=C["text"],
                           cursor="hand2", command=self._generate).pack(side="left")

        pf = tk.Frame(body, bg=C["surface2"], highlightthickness=1,
                      highlightbackground=C["border"]); pf.pack(fill="x", pady=12)
        self._prev = tk.Label(pf, text="", font=FONT_MONO, fg=C["success"],
                              bg=C["surface2"], pady=10, padx=12, wraplength=360)
        self._prev.pack()
        self._sb = StrengthBar(body); self._sb.pack(anchor="w")

        bf = tk.Frame(body, bg=C["bg"]); bf.pack(fill="x", pady=4)
        IconButton(bf, "🔄 Regenerate", command=self._generate, style="ghost").pack(side="left")
        if self.callback:
            IconButton(bf, "Use This Password", command=self._use, style="success").pack(side="right")
        else:
            IconButton(bf, "📋 Copy", command=self._copy, style="primary").pack(side="right")
        self._generate()

    def _generate(self):
        self._pwd = CryptoEngine.gen_password(self.len_var.get(),
            self.upper_v.get(), self.lower_v.get(), self.digit_v.get(), self.symbol_v.get())
        self._prev.config(text=self._pwd); self._sb.update_strength(self._pwd)

    def _copy(self):
        self.clipboard_clear(); self.clipboard_append(self._pwd)
        messagebox.showinfo("Copied", "Password copied!", parent=self)

    def _use(self):
        if self.callback: self.callback(self._pwd)
        self.destroy()


# ══════════════════════════════════════════════
#  ABOUT DIALOG
# ══════════════════════════════════════════════
class AboutDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(f"About {APP_NAME}"); self.resizable(False, False); self.configure(bg=C["bg"])
        self.geometry(f"520x720+{(self.winfo_screenwidth()-520)//2}+{(self.winfo_screenheight()-720)//2}")
        self.grab_set(); self._build()

    def _build(self):
        hero = tk.Frame(self, bg=C["surface"], height=140); hero.pack(fill="x"); hero.pack_propagate(False)
        hf = tk.Frame(hero, bg=C["surface"]); hf.place(relx=0.5, rely=0.5, anchor="center")
        img = _load_img(_LOGO_B64)
        if img:
            self._logo = img; tk.Label(hf, image=img, bg=C["surface"]).pack(pady=(0,4))
        else:
            tk.Label(hf, text="ENIX", font=("Segoe UI",20,"bold"), fg=C["accent"], bg=C["surface"]).pack()
        tk.Label(hf, text=f"Password Manager  v{VERSION}", font=("Segoe UI",9),
                 fg=C["text2"], bg=C["surface"]).pack()

        outer = tk.Frame(self, bg=C["bg"]); outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        sb_scroll = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb_scroll.set)
        sb_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        body = tk.Frame(canvas, bg=C["bg"])
        body_window = canvas.create_window((0,0), window=body, anchor="nw")
        def _on_resize(e): canvas.itemconfig(body_window, width=e.width)
        canvas.bind("<Configure>", _on_resize)
        def _update_scroll(e): canvas.configure(scrollregion=canvas.bbox("all"))
        body.bind("<Configure>", _update_scroll)
        def _on_mousewheel(e): canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        inner = tk.Frame(body, bg=C["bg"]); inner.pack(fill="both", expand=True, padx=36, pady=20)

        def section(title, items):
            tk.Label(inner, text=title, font=("Segoe UI",11,"bold"),
                     fg=C["accent"], bg=C["bg"], anchor="w").pack(fill="x", pady=(12,4))
            tk.Frame(inner, bg=C["border"], height=1).pack(fill="x", pady=(0,8))
            for icon, text in items:
                r = tk.Frame(inner, bg=C["bg"]); r.pack(fill="x", pady=3)
                tk.Label(r, text=icon, font=("Segoe UI",12), bg=C["bg"],
                         fg=C["accent2"]).pack(side="left", padx=(0,8))
                tk.Label(r, text=text, font=FONT_LABEL, fg=C["text"], bg=C["bg"],
                         anchor="w", wraplength=400, justify="left").pack(side="left")

        section("Security Architecture", [
            ("🛡️","AES-256 encryption via Fernet"),
            ("🔑","Master password never stored — only a PBKDF2-SHA256 hash"),
            ("🧂","32-byte random salt per vault"),
            (f"🔁",f"{CryptoEngine.ITERATIONS:,} PBKDF2 iterations"),
            ("💾","100% local — data never leaves your device"),
            ("🔄","Encrypted export/import with separate backup password"),
        ])
        section("Features", [
            ("🛡️","AES-256 encryption (Fernet) — military-grade vault protection"),
            ("🔐","Master password authentication — vault locked until verified"),
            ("🔑","PBKDF2-SHA256 key derivation — brute-force resistant hashing"),
            ("🧂","Random cryptographic salt per vault — defeats rainbow-table attacks"),
            ("⚡","Secure password generator — customisable length & character sets"),
            ("💪","Real-time password strength meter — visual entropy feedback"),
            ("💾","Encrypted local storage — data never leaves your device"),
            ("👁","Password visibility toggle — reveal/hide with one click"),
            ("🔄","Encrypted backup export/import (.enixbackup) — separate backup password"),
            ("📋","Copy to clipboard — instant one-click credential copying"),
            ("🔍","Credential search & category filter — find anything instantly"),
            ("🎨","Modern dark UI — polished, distraction-free interface"),
        ])
        section("About", [
            ("🏢","Developed by Enix Software India"),
            ("🌐",WEBSITE),
            ("⚠️","Authorized Use Only"),
            ("©","2025 Enix Software India. All rights reserved."),
        ])
        IconButton(inner, "Close", command=self.destroy, style="ghost").pack(pady=10)


# ══════════════════════════════════════════════
#  EXPORT / IMPORT DIALOG
# ══════════════════════════════════════════════
class ExportImportDialog(tk.Toplevel):
    def __init__(self, parent, vault, on_done=None):
        super().__init__(parent)
        self.vault = vault; self.on_done = on_done; self._import_path = None
        self.title("Export / Import Vault"); self.resizable(False, False); self.configure(bg=C["bg"])
        self.geometry(f"500x640+{(self.winfo_screenwidth()-500)//2}+{(self.winfo_screenheight()-640)//2}")
        self.grab_set(); self._build()

    def _pwd_row(self, parent, lbl_text):
        tk.Label(parent, text=lbl_text, font=FONT_LABEL,
                 fg=C["text2"], bg=C["surface"], anchor="w").pack(fill="x")
        wrap = tk.Frame(parent, bg=C["surface2"], highlightthickness=1,
                        highlightbackground=C["border"], highlightcolor=C["accent"])
        wrap.pack(fill="x", pady=4)
        var = tk.StringVar()
        ent = tk.Entry(wrap, textvariable=var, show="*", font=FONT_MONO,
                       bg=C["surface2"], fg=C["text"],
                       insertbackground=C["accent"], relief="flat", bd=8)
        ent.pack(side="left", fill="x", expand=True)
        shown = [False]
        eye = tk.Button(wrap, text="👁", font=("Segoe UI",10), bg=C["surface2"],
                        fg=C["text2"], relief="flat", bd=0, cursor="hand2")
        def toggle():
            shown[0] = not shown[0]
            ent.config(show="" if shown[0] else "*")
            eye.config(text="🙈" if shown[0] else "👁")
        eye.config(command=toggle); eye.pack(side="right", padx=6)
        return var

    def _build(self):
        tk.Frame(self, bg=C["surface"], height=56).pack(fill="x")
        hdr = self.winfo_children()[-1]; hdr.pack_propagate(False)
        tk.Label(hdr, text="  🔄  Export / Import Vault", font=FONT_HEAD,
                 fg=C["text"], bg=C["surface"]).pack(side="left", padx=16)

        # scrollable area
        outer = tk.Frame(self, bg=C["bg"]); outer.pack(fill="both", expand=True)
        cv = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        sv = tk.Scrollbar(outer, orient="vertical", command=cv.yview)
        cv.configure(yscrollcommand=sv.set)
        sv.pack(side="right", fill="y"); cv.pack(fill="both", expand=True)
        body = tk.Frame(cv, bg=C["bg"])
        bw = cv.create_window((0,0), window=body, anchor="nw")
        body.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.bind("<Configure>", lambda e: cv.itemconfig(bw, width=e.width))
        cv.bind("<MouseWheel>", lambda e: cv.yview_scroll(int(-1*(e.delta/120)),"units"))

        pad = tk.Frame(body, bg=C["bg"]); pad.pack(fill="x", padx=24)

        def sec_hdr(txt, col):
            r = tk.Frame(pad, bg=C["bg"]); r.pack(fill="x", pady=(16,6))
            tk.Label(r, text=txt, font=("Segoe UI",10,"bold"), fg=col, bg=C["bg"]).pack(side="left")
            tk.Frame(r, bg=C["border"], height=1).pack(side="left", fill="x", expand=True, padx=10, pady=5)

        # ── EXPORT ──
        sec_hdr("📤  EXPORT", C["accent"])
        tk.Label(pad,
                 text="Save an encrypted backup of your vault protected\nby a separate export password.",
                 font=FONT_SMALL, fg=C["text2"], bg=C["bg"],
                 justify="left", anchor="w").pack(fill="x", pady=(0,8))
        ec = tk.Frame(pad, bg=C["surface"], highlightthickness=1,
                      highlightbackground=C["border"]); ec.pack(fill="x")
        ei = tk.Frame(ec, bg=C["surface"]); ei.pack(fill="x", padx=16, pady=14)
        self._exp_pwd = self._pwd_row(ei, "Export Password")
        self._exp_st = tk.Label(ei, text="", font=FONT_SMALL, fg=C["danger"], bg=C["surface"])
        self._exp_st.pack(anchor="w", pady=(2,0))
        IconButton(ei, "📤  Export Vault", command=self._do_export,
                   style="primary").pack(fill="x", pady=(10,0), ipady=3)

        # ── IMPORT ──
        sec_hdr("📥  IMPORT", C["success"])
        tk.Label(pad,
                 text="Restore from an .enixbackup file. Use Merge to keep\nexisting entries, or Replace to overwrite all.",
                 font=FONT_SMALL, fg=C["text2"], bg=C["bg"],
                 justify="left", anchor="w").pack(fill="x", pady=(0,8))
        ic = tk.Frame(pad, bg=C["surface"], highlightthickness=1,
                      highlightbackground=C["border"]); ic.pack(fill="x")
        ii = tk.Frame(ic, bg=C["surface"]); ii.pack(fill="x", padx=16, pady=14)
        self._imp_pwd = self._pwd_row(ii, "Import Password")

        fr = tk.Frame(ii, bg=C["surface"]); fr.pack(fill="x", pady=6)
        self._file_lbl = tk.Label(fr, text="No file selected", font=FONT_SMALL,
                                  fg=C["text3"], bg=C["surface"], anchor="w")
        self._file_lbl.pack(side="left", fill="x", expand=True)
        IconButton(fr, "📁 Browse", command=self._browse, style="ghost").pack(side="right")

        self._mode = tk.StringVar(value="merge")
        mr = tk.Frame(ii, bg=C["surface"]); mr.pack(fill="x", pady=4)
        for val, lbl, desc in [("merge","Merge","keep existing"),
                               ("replace","Replace","overwrite all")]:
            rf = tk.Frame(mr, bg=C["surface"]); rf.pack(side="left", padx=(0,20))
            tk.Radiobutton(rf, text=lbl, variable=self._mode, value=val,
                           font=("Segoe UI",10,"bold"), fg=C["text"], bg=C["surface"],
                           selectcolor=C["surface2"], activebackground=C["surface"],
                           activeforeground=C["text"], cursor="hand2").pack(side="left")
            tk.Label(rf, text=desc, font=FONT_SMALL, fg=C["text3"],
                     bg=C["surface"]).pack(side="left", padx=(3,0))

        self._imp_st = tk.Label(ii, text="", font=FONT_SMALL, fg=C["danger"], bg=C["surface"])
        self._imp_st.pack(anchor="w", pady=(4,0))
        IconButton(ii, "📥  Import Vault", command=self._do_import,
                   style="success").pack(fill="x", pady=(10,0), ipady=3)

        tk.Frame(pad, bg=C["border"], height=1).pack(fill="x", pady=14)
        IconButton(pad, "Close", command=self.destroy, style="ghost").pack(pady=(0,16))

    def _browse(self):
        p = filedialog.askopenfilename(title="Select Backup",
                                       filetypes=[("Enix Backup","*.enixbackup"),("All Files","*.*")],
                                       parent=self)
        if p:
            self._import_path = p
            self._file_lbl.config(text=os.path.basename(p), fg=C["success"])
            self._imp_st.config(text="")

    def _do_export(self):
        pwd = self._exp_pwd.get().strip()
        if not pwd: self._exp_st.config(text="Enter an export password.", fg=C["warning"]); return
        if len(pwd) < 4: self._exp_st.config(text="Password must be 4+ characters.", fg=C["warning"]); return
        path = filedialog.asksaveasfilename(
            title="Save Backup", defaultextension=".enixbackup",
            filetypes=[("Enix Backup","*.enixbackup")],
            initialfile=f"enix_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}", parent=self)
        if not path: return
        try:
            salt = os.urandom(32)
            key  = CryptoEngine._derive_key(pwd, salt)
            payload = {"version":"1.0","app":"EnixPasswordManager",
                       "exported":datetime.now().isoformat(),
                       "count":len(self.vault.entries),"entries":self.vault.entries}
            bundle = {"salt": base64.b64encode(salt).decode(),
                      "data": CryptoEngine.encrypt(json.dumps(payload), key)}
            with open(path,"w") as f: json.dump(bundle, f)
            n = len(self.vault.entries)
            self._exp_st.config(text=f"Exported {n} entries successfully!", fg=C["success"])
            messagebox.showinfo("Export Complete",
                f"{n} password{'s' if n!=1 else ''} exported.\n\nFile: {os.path.basename(path)}\n\nKeep this file and its password safe.",
                parent=self)
        except Exception as ex:
            self._exp_st.config(text=f"Export failed: {ex}", fg=C["danger"])

    def _do_import(self):
        if not self._import_path:
            self._imp_st.config(text="Select a .enixbackup file first.", fg=C["warning"]); return
        pwd = self._imp_pwd.get().strip()
        if not pwd: self._imp_st.config(text="Enter the import password.", fg=C["warning"]); return
        try:
            with open(self._import_path) as f: bundle = json.load(f)
            salt    = base64.b64decode(bundle["salt"])
            key     = CryptoEngine._derive_key(pwd, salt)
            payload = json.loads(CryptoEngine.decrypt(bundle["data"], key))
            if payload.get("app") != "EnixPasswordManager":
                raise ValueError("Not a valid Enix backup file.")
            entries = payload.get("entries", [])
            mode    = self._mode.get()
            if mode == "replace":
                if not messagebox.askyesno("Replace Vault",
                    f"Delete all {len(self.vault.entries)} existing entries\nand replace with {len(entries)} imported?\n\nThis cannot be undone.",
                    parent=self): return
                self.vault.entries = []
            existing = {(e.get("title","").lower(), e.get("username","").lower())
                        for e in self.vault.entries}
            added = skipped = 0
            for e in entries:
                k = (e.get("title","").lower(), e.get("username","").lower())
                if mode == "merge" and k in existing: skipped += 1; continue
                e["id"] = secrets.token_hex(8); self.vault.entries.append(e); added += 1
            self.vault._save()
            msg = f"Added {added} entries"
            if skipped: msg += f" ({skipped} duplicates skipped)"
            self._imp_st.config(text=msg, fg=C["success"])
            messagebox.showinfo("Import Complete",
                f"Import complete!\nAdded: {added} entries" +
                (f"\nSkipped: {skipped} duplicates" if skipped else ""), parent=self)
            if self.on_done: self.on_done()
        except Exception as ex:
            err = str(ex)
            self._imp_st.config(
                text="Wrong password or corrupted file." if "InvalidToken" in err else f"Error: {err}",
                fg=C["danger"])


# ══════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════
class EnixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.vault = Vault()
        self._active_cat  = "all"
        self._selected_id = None
        self.withdraw()
        self.title(APP_NAME); self.configure(bg=C["bg"])
        self.minsize(920, 620)
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"1060x680+{(sw-1060)//2}+{(sh-680)//2}")
        _set_win_icon(self)
        self._build_ui()
        self.after(100, self._start)

    def _build_ui(self):
        self._build_sidebar()
        self._build_main()
        self._build_statusbar()

    # ── SIDEBAR ──────────────────────────────
    def _build_sidebar(self):
        sb = tk.Frame(self, bg=C["surface"], width=230)
        sb.pack(side="left", fill="y"); sb.pack_propagate(False)

        lf = tk.Frame(sb, bg=C["surface"], height=72)
        lf.pack(fill="x"); lf.pack_propagate(False)
        img = _load_img(_LOGO_SM)
        self._egg_clicks = [0]
        if img:
            self._sb_logo = img
            logo_lbl = tk.Label(lf, image=img, bg=C["surface"], cursor="hand2")
            logo_lbl.place(relx=0.5, rely=0.5, anchor="center")
        else:
            logo_lbl = tk.Label(lf, text="ENIX", font=("Segoe UI",16,"bold"),
                     fg=C["accent"], bg=C["surface"], cursor="hand2")
            logo_lbl.place(relx=0.5, rely=0.5, anchor="center")

        def _logo_click(event=None):
            self._egg_clicks[0] += 1
            if self._egg_clicks[0] >= 4:
                self._egg_clicks[0] = 0
                self._show_easter_egg()
        logo_lbl.bind("<Button-1>", _logo_click)
        tk.Frame(sb, bg=C["border"], height=1).pack(fill="x")

        sf = tk.Frame(sb, bg=C["surface"], pady=10, padx=12); sf.pack(fill="x")
        wrap = tk.Frame(sf, bg=C["surface2"], highlightthickness=1,
                        highlightbackground=C["border"], highlightcolor=C["accent"])
        wrap.pack(fill="x")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        tk.Label(wrap, text="🔍", font=("Segoe UI",10),
                 bg=C["surface2"], fg=C["text2"]).pack(side="left", padx=6)
        tk.Entry(wrap, textvariable=self.search_var, font=FONT_LABEL,
                 bg=C["surface2"], fg=C["text"],
                 insertbackground=C["accent"], relief="flat", bd=6).pack(side="left", fill="x", expand=True)

        tk.Frame(sb, bg=C["border"], height=1).pack(fill="x")
        self.cat_btns = {}
        cats = [("🔵 All Items","all"),("🔑 Login","Login"),("📧 Email","Email"),
                ("🏦 Banking","Banking"),("💬 Social","Social"),("💼 Work","Work"),
                ("🛒 Shopping","Shopping"),("🔧 API Key","API Key"),
                ("📝 Note","Note"),("📁 Other","Other")]
        for lbl, key in cats:
            b = tk.Button(sb, text=f"  {lbl}", font=FONT_LABEL, anchor="w",
                          bg=C["surface"], fg=C["text2"], relief="flat", bd=0,
                          cursor="hand2", padx=8, pady=6,
                          activebackground=C["surface2"], activeforeground=C["text"],
                          command=lambda k=key: self._filter_cat(k))
            b.pack(fill="x"); self.cat_btns[key] = b
        self._filter_cat("all")

        tk.Frame(sb, bg=C["border"], height=1).pack(fill="x", pady=4)
        IconButton(sb, "  ➕  Add Password", command=self._add_entry,
                   style="primary").pack(fill="x", padx=12, pady=4, ipady=2)
        IconButton(sb, "  ⚡  Generator",
                   command=lambda: GenDialog(self),
                   style="ghost").pack(fill="x", padx=12, pady=2, ipady=2)
        IconButton(sb, "  🔄  Export / Import",
                   command=lambda: ExportImportDialog(self, self.vault, on_done=self.refresh),
                   style="ghost").pack(fill="x", padx=12, pady=2, ipady=2)
        IconButton(sb, "  🔒  Lock Vault",
                   command=self._lock,
                   style="ghost").pack(fill="x", padx=12, pady=2, ipady=2)
        IconButton(sb, "  ℹ️   About",
                   command=lambda: AboutDialog(self),
                   style="ghost").pack(fill="x", padx=12, pady=2, ipady=2)

        self.count_lbl = tk.Label(sb, text="0 items", font=FONT_SMALL,
                                  fg=C["text3"], bg=C["surface"])
        self.count_lbl.pack(side="bottom", pady=10)

    # ── MAIN PANE ────────────────────────────
    def _build_main(self):
        self.main = tk.Frame(self, bg=C["bg"]); self.main.pack(side="left", fill="both", expand=True)

        topbar = tk.Frame(self.main, bg=C["surface"], height=52)
        topbar.pack(fill="x"); topbar.pack_propagate(False)
        self.topbar_title = tk.Label(topbar, text="All Passwords",
                                     font=FONT_HEAD, fg=C["text"], bg=C["surface"])
        self.topbar_title.pack(side="left", padx=20)
        self.topbar_count = tk.Label(topbar, text="", font=FONT_SMALL,
                                     fg=C["text2"], bg=C["surface"])
        self.topbar_count.pack(side="left")
        IconButton(topbar, "➕ Add", command=self._add_entry,
                   style="primary").pack(side="right", padx=12, pady=10)

        pane = tk.PanedWindow(self.main, orient="horizontal",
                              bg=C["bg"], bd=0, sashwidth=5, sashrelief="flat")
        pane.pack(fill="both", expand=True)

        lf = tk.Frame(pane, bg=C["bg"]); pane.add(lf, minsize=280)
        self.list_canvas = tk.Canvas(lf, bg=C["bg"], highlightthickness=0, bd=0)
        lsb = tk.Scrollbar(lf, orient="vertical", command=self.list_canvas.yview)
        self.list_canvas.configure(yscrollcommand=lsb.set)
        lsb.pack(side="right", fill="y"); self.list_canvas.pack(fill="both", expand=True)
        self.list_inner = tk.Frame(self.list_canvas, bg=C["bg"])
        self._list_win = self.list_canvas.create_window((0,0), window=self.list_inner, anchor="nw")
        self.list_inner.bind("<Configure>",
            lambda e: self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all")))
        self.list_canvas.bind("<Configure>",
            lambda e: self.list_canvas.itemconfig(self._list_win, width=e.width))

        # Bind mousewheel only when pointer is over the list canvas (not globally)
        def _list_scroll(e): self.list_canvas.yview_scroll(int(-1*(e.delta/120)),"units")
        self.list_canvas.bind("<Enter>", lambda e: self.list_canvas.bind_all("<MouseWheel>", _list_scroll))
        self.list_canvas.bind("<Leave>", lambda e: self.list_canvas.unbind_all("<MouseWheel>"))

        self.detail_frame = tk.Frame(pane, bg=C["surface"])
        pane.add(self.detail_frame, minsize=340)
        self._show_empty_detail()

    def _build_statusbar(self):
        sb = tk.Frame(self, bg=C["surface"], height=30)
        sb.pack(side="bottom", fill="x")
        sb.pack_propagate(False)
        tk.Frame(sb, bg=C["border"], height=1).pack(fill="x", side="top")

        # Left: app info + clickable website
        left = tk.Frame(sb, bg=C["surface"])
        left.pack(side="left", fill="y")

        self.status_lbl = tk.Label(left,
            text=f"  {APP_NAME} v{VERSION}  |  {DEVELOPER}",
            font=FONT_SMALL, fg=C["text3"], bg=C["surface"], anchor="w")
        self.status_lbl.pack(side="left", padx=(0, 4))

        sep = tk.Label(left, text="|", font=FONT_SMALL,
                       fg=C["text3"], bg=C["surface"])
        sep.pack(side="left")

        # Clickable website link
        link = tk.Label(left, text=f"  www.enixsoftwareindia.com  ",
                        font=("Segoe UI", 9, "underline"),
                        fg=C["accent"], bg=C["surface"],
                        cursor="hand2", anchor="w")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: self._open_website())
        link.bind("<Enter>", lambda e: link.config(fg=C["accent2"]))
        link.bind("<Leave>", lambda e: link.config(fg=C["accent"]))

        # Right: encrypted badge
        tk.Label(sb, text="🔒 Encrypted", font=FONT_SMALL,
                 fg=C["success"], bg=C["surface"]).pack(side="right", padx=12)

    def _open_website(self):
        import webbrowser
        webbrowser.open(WEBSITE)

    # ── FLOW ─────────────────────────────────
    def _start(self):
        if not self.vault.is_configured():
            MasterScreen(self.vault, self._on_unlocked, mode="setup")
        else:
            MasterScreen(self.vault, self._on_unlocked, mode="unlock")

    def _on_unlocked(self): self.deiconify(); self.refresh()
    def _lock(self): self.vault.lock(); self.withdraw(); self._start()

    def _show_easter_egg(self):
        """Hidden Easter egg — shown after clicking the logo 4 times."""
        egg = tk.Toplevel(self)
        egg.title("🔐 Enix Secret")
        egg.resizable(False, False)
        egg.configure(bg=C["bg"])
        egg.geometry(f"480x520+{(egg.winfo_screenwidth()-480)//2}+{(egg.winfo_screenheight()-520)//2}")
        egg.grab_set()

        # Header
        hdr = tk.Frame(egg, bg=C["surface"], height=110); hdr.pack(fill="x"); hdr.pack_propagate(False)
        hf = tk.Frame(hdr, bg=C["surface"]); hf.place(relx=0.5, rely=0.5, anchor="center")
        img = _load_img(_LOGO_B64)
        if img:
            self._egg_logo = img
            tk.Label(hf, image=img, bg=C["surface"]).pack(pady=(0,4))
        tk.Label(hf, text="🔓  You found the secret!", font=("Segoe UI",11,"bold"),
                 fg=C["accent"], bg=C["surface"]).pack()

        body = tk.Frame(egg, bg=C["bg"]); body.pack(fill="both", expand=True, padx=30, pady=16)

        # Credits
        tk.Label(body, text="Developed by", font=("Segoe UI",10),
                 fg=C["text2"], bg=C["bg"]).pack()
        tk.Label(body, text="Enix Software India", font=("Segoe UI",15,"bold"),
                 fg=C["accent"], bg=C["bg"]).pack(pady=(0,2))
        tk.Label(body, text="Aditya Bhosale", font=("Segoe UI",12),
                 fg=C["text"], bg=C["bg"]).pack()

        tk.Frame(body, bg=C["border"], height=1).pack(fill="x", pady=14)

        # Security quotes
        tk.Label(body, text="💬  Words to live by", font=("Segoe UI",10,"bold"),
                 fg=C["accent2"], bg=C["bg"]).pack(pady=(0,8))

        quotes = [
            ("\"Security is not a product, but a process.\"", "— Bruce Schneier"),
            ("\"The only truly secure system is one that is\npowered off, cast in a block of concrete and\nsealed in a lead-lined room.\"", "— Gene Spafford"),
            ("\"Encryption works. Properly implemented strong\ncrypto systems are one of the few things you can rely on.\"", "— Edward Snowden"),
        ]
        for q, attr in quotes:
            qf = tk.Frame(body, bg=C["surface"], padx=14, pady=10)
            qf.pack(fill="x", pady=5)
            tk.Label(qf, text=q, font=("Segoe UI",9,"italic"),
                     fg=C["text"], bg=C["surface"], wraplength=390, justify="left").pack(anchor="w")
            tk.Label(qf, text=attr, font=("Segoe UI",8),
                     fg=C["text2"], bg=C["surface"], anchor="e").pack(fill="x")

        IconButton(body, "Close", command=egg.destroy, style="ghost").pack(pady=12)


    def refresh(self, query="", category=None):
        cat = category if category is not None else self._active_cat
        items = self.vault.search(query) if query else list(self.vault.entries)
        if cat != "all": items = [e for e in items if e.get("category") == cat]
        for w in self.list_inner.winfo_children(): w.destroy()
        if not items:
            f = tk.Frame(self.list_inner, bg=C["bg"]); f.pack(fill="x", padx=20, pady=40)
            tk.Label(f, text="🔍", font=("Segoe UI",32), bg=C["bg"]).pack()
            tk.Label(f, text="No entries found", font=FONT_HEAD,
                     fg=C["text2"], bg=C["bg"]).pack(pady=4)
            tk.Label(f, text='Click "Add Password" to get started.',
                     font=FONT_LABEL, fg=C["text3"], bg=C["bg"]).pack()
        else:
            for e in items: self._entry_card(e)
        total = len(self.vault.entries)
        self.count_lbl.config(text=f"{total} item{'s' if total!=1 else ''}")
        self.topbar_count.config(text=f"  ({len(items)} shown)")

    def _entry_card(self, entry: dict):
        ICONS = {"Login":"🔑","Email":"📧","Banking":"🏦","Social":"💬",
                 "Work":"💼","Shopping":"🛒","API Key":"🔧","Note":"📝","Other":"📁"}
        icon = ICONS.get(entry.get("category",""), "🔑")
        eid  = entry["id"]
        sel  = eid == self._selected_id
        bg_c = C["surface2"] if sel else C["surface"]
        hl_c = C["accent"]   if sel else C["border"]

        card = tk.Frame(self.list_inner, bg=bg_c,
                        highlightthickness=1, highlightbackground=hl_c,
                        cursor="hand2")
        card._entry_id = eid
        card.pack(fill="x", padx=12, pady=4)

        inner = tk.Frame(card, bg=bg_c, cursor="hand2")
        inner.pack(fill="x", padx=12, pady=10)

        left = tk.Frame(inner, bg=bg_c, cursor="hand2")
        left.pack(side="left", fill="x", expand=True)
        title_lbl = tk.Label(left, text=f"{icon}  {entry.get('title','Untitled')}",
                             font=("Segoe UI",11,"bold"), fg=C["text"], bg=bg_c,
                             anchor="w", cursor="hand2")
        title_lbl.pack(fill="x")
        user_lbl = tk.Label(left, text=entry.get("username","—"),
                            font=FONT_SMALL, fg=C["text2"], bg=bg_c,
                            anchor="w", cursor="hand2")
        user_lbl.pack(fill="x")

        right = tk.Frame(inner, bg=bg_c, cursor="hand2")
        right.pack(side="right")
        cat_lbl = tk.Label(right, text=entry.get("category",""), font=("Segoe UI",8),
                           fg=C["accent2"], bg=C["surface2"], padx=6, pady=2,
                           cursor="hand2")
        cat_lbl.pack()

        all_w = [card, inner, left, right, title_lbl, user_lbl, cat_lbl]

        def _set_bg(bg, hl):
            card.config(bg=bg, highlightbackground=hl)
            for w in (inner, left, right, title_lbl, user_lbl):
                try: w.config(bg=bg)
                except Exception: pass

        def on_enter(e):   _set_bg(C["surface2"], C["accent"])
        def on_leave(e):
            s = eid == self._selected_id
            _set_bg(C["surface2"] if s else C["surface"],
                    C["accent"]   if s else C["border"])
        def on_click(e):   self._show_detail(eid)

        for w in all_w:
            w.bind("<Enter>",    lambda e, f=on_enter: f(e))
            w.bind("<Leave>",    lambda e, f=on_leave: f(e))
            w.bind("<Button-1>", lambda e, f=on_click: f(e))

    def _update_card_highlights(self):
        """Update card highlight colours without rebuilding the list."""
        for card in self.list_inner.winfo_children():
            eid = getattr(card, "_entry_id", None)
            if eid is None: continue
            sel = eid == self._selected_id
            bg  = C["surface2"] if sel else C["surface"]
            hl  = C["accent"]   if sel else C["border"]
            card.config(bg=bg, highlightbackground=hl)
            for ch in card.winfo_children():
                try: ch.config(bg=bg)
                except Exception: pass
                for cch in ch.winfo_children():
                    try: cch.config(bg=bg)
                    except Exception: pass

    # ── DETAIL PANEL ─────────────────────────
    def _show_empty_detail(self):
        for w in self.detail_frame.winfo_children(): w.destroy()
        f = tk.Frame(self.detail_frame, bg=C["surface"])
        f.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(f, text="🔐", font=("Segoe UI",40), bg=C["surface"]).pack()
        tk.Label(f, text="Select an entry to view details",
                 font=FONT_LABEL, fg=C["text3"], bg=C["surface"]).pack(pady=6)

    def _show_detail(self, eid: str):
        entry = next((e for e in self.vault.entries if e["id"] == eid), None)
        if not entry: return
        self._selected_id = eid
        self._update_card_highlights()

        # ── Destroy old detail widgets ────────
        for w in self.detail_frame.winfo_children():
            w.destroy()

        ICONS = {"Login":"🔑","Email":"📧","Banking":"🏦","Social":"💬",
                 "Work":"💼","Shopping":"🛒","API Key":"🔧","Note":"📝","Other":"📁"}
        icon = ICONS.get(entry.get("category",""), "🔑")
        BG   = C["bg"]
        S2   = C["surface2"]
        S    = C["surface"]

        # ════════════════════════════════════════
        #  TOP HEADER BAR
        # ════════════════════════════════════════
        hdr = tk.Frame(self.detail_frame, bg=S2, height=64)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)
        tk.Label(hdr, text=f"{icon}  {entry.get('title','Untitled')}",
                 font=("Segoe UI",13,"bold"), fg=C["text"], bg=S2,
                 anchor="w").place(x=16, y=10)
        tk.Label(hdr, text=f"  {entry.get('category','')}  ",
                 font=("Segoe UI",8,"bold"), fg=C["accent2"],
                 bg=C["surface"]).place(x=16, y=40)

        # ════════════════════════════════════════
        #  BOTTOM ACTION BAR
        # ════════════════════════════════════════
        bot = tk.Frame(self.detail_frame, bg=S, height=56)
        bot.pack(fill="x", side="bottom")
        bot.pack_propagate(False)
        tk.Frame(bot, bg=C["border"], height=1).pack(fill="x", side="top")
        bb = tk.Frame(bot, bg=S); bb.pack(fill="both", expand=True, padx=14, pady=8)
        IconButton(bb, "🗑  Delete", style="danger",
                   command=lambda: self._delete_entry(eid)).pack(side="right", padx=4)
        IconButton(bb, "✏️  Edit", style="ghost",
                   command=lambda: self._edit_entry(eid)).pack(side="right", padx=4)

        # ════════════════════════════════════════
        #  SCROLLABLE CONTENT (Text widget trick)
        #  Use a plain Frame inside a Text widget
        #  so no Canvas+binding conflicts at all
        # ════════════════════════════════════════
        container = tk.Frame(self.detail_frame, bg=BG)
        container.pack(fill="both", expand=True, side="top")

        txt = tk.Text(container, bg=BG, bd=0, highlightthickness=0,
                      relief="flat", cursor="arrow", state="normal",
                      wrap="none")
        vsb = tk.Scrollbar(container, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)

        # Inner frame embedded inside Text widget
        inner = tk.Frame(txt, bg=BG)
        txt.window_create("end", window=inner)
        txt.config(state="disabled")  # prevent typing

        # Mousewheel scrolls the Text widget naturally — no extra binding needed

        # ════════════════════════════════════════
        #  FIELD BUILDER  (inside inner frame)
        # ════════════════════════════════════════
        def field(label_text, value, secret=False, revealed=True):
            """Build one labelled field row inside inner."""
            if not value:
                return
            row = tk.Frame(inner, bg=BG)
            row.pack(fill="x", padx=16, pady=(10, 2))

            # Label
            tk.Label(row, text=label_text,
                     font=("Segoe UI", 8, "bold"),
                     fg=C["text3"], bg=BG, anchor="w").pack(fill="x")

            # Value box
            box = tk.Frame(row, bg=S2,
                           highlightthickness=1, highlightbackground=C["border"])
            box.pack(fill="x", pady=(3, 0))

            shown = [revealed]
            display = value if (not secret or revealed) else "●" * min(len(value), 32)
            var = tk.StringVar(value=display)

            val_lbl = tk.Label(box, textvariable=var,
                               font=FONT_MONO if secret else FONT_LABEL,
                               fg=C["text"], bg=S2,
                               anchor="w", padx=10, pady=8,
                               wraplength=220, justify="left")
            val_lbl.pack(side="left", fill="x", expand=True)

            btn_area = tk.Frame(box, bg=S2)
            btn_area.pack(side="right", padx=4, pady=4)

            # Copy button
            def copy_it(v=value, lbl=label_text):
                self.clipboard_clear()
                self.clipboard_append(v)
                self._flash_status(f"Copied  {lbl}")
                cp.config(bg=C["success"], fg=C["white"])
                self.after(800, lambda: cp.config(bg=S2, fg=C["text2"]))

            cp = tk.Button(btn_area, text="📋",
                           font=("Segoe UI", 12), bg=S2, fg=C["text2"],
                           activebackground=C["border"], activeforeground=C["text"],
                           relief="flat", bd=0, padx=4, pady=2,
                           cursor="hand2", command=copy_it)
            cp.pack(side="left")

            # Eye toggle (secret fields only)
            if secret:
                def toggle_eye(v=value):
                    shown[0] = not shown[0]
                    var.set(v if shown[0] else "●" * min(len(v), 32))
                    eye.config(text="🙈" if shown[0] else "👁")

                eye = tk.Button(btn_area,
                                text="🙈" if revealed else "👁",
                                font=("Segoe UI", 12), bg=S2, fg=C["text2"],
                                activebackground=C["border"], activeforeground=C["text"],
                                relief="flat", bd=0, padx=4, pady=2,
                                cursor="hand2", command=toggle_eye)
                eye.pack(side="left", padx=(2, 0))

        # ── Spacer ────────────────────────────
        tk.Frame(inner, bg=BG, height=8).pack()

        # ── Fields ────────────────────────────
        field("USERNAME / EMAIL", entry.get("username", ""))
        field("PASSWORD",         entry.get("password", ""), secret=True, revealed=True)
        field("WEBSITE URL",      entry.get("url", ""))
        field("NOTES",            entry.get("notes", ""))

        # ── Divider ───────────────────────────
        tk.Frame(inner, bg=C["border"], height=1).pack(fill="x", padx=16, pady=(14, 6))

        # ── Password strength ─────────────────
        sr = tk.Frame(inner, bg=BG); sr.pack(fill="x", padx=16, pady=4)
        tk.Label(sr, text="PASSWORD STRENGTH",
                 font=("Segoe UI", 8, "bold"),
                 fg=C["text3"], bg=BG, anchor="w").pack(fill="x")
        sb2 = StrengthBar(sr); sb2.bg = BG
        sb2.configure(bg=BG)
        sb2.pack(anchor="w", pady=4)
        sb2.update_strength(entry.get("password", ""))

        # ── Dates ─────────────────────────────
        tk.Frame(inner, bg=C["border"], height=1).pack(fill="x", padx=16, pady=(10, 6))
        dr = tk.Frame(inner, bg=BG); dr.pack(fill="x", padx=16, pady=(0, 16))
        tk.Label(dr, text=f"Created   {entry.get('created','')[:10]}",
                 font=FONT_SMALL, fg=C["text3"], bg=BG, anchor="w").pack(fill="x")
        tk.Label(dr, text=f"Updated   {entry.get('updated','')[:10]}",
                 font=FONT_SMALL, fg=C["text3"], bg=BG, anchor="w").pack(fill="x")

    # ── CRUD ─────────────────────────────────
    def _add_entry(self):
        EntryDialog(self, self.vault, on_save=self.refresh)

    def _edit_entry(self, eid: str):
        e = next((x for x in self.vault.entries if x["id"] == eid), None)
        if e: EntryDialog(self, self.vault, entry=e,
                          on_save=lambda: (self.refresh(), self._show_detail(eid)))

    def _delete_entry(self, eid: str):
        if messagebox.askyesno("Delete Entry",
                               "Delete this entry?\nThis cannot be undone.", parent=self):
            self.vault.delete(eid)
            self._selected_id = None
            self._show_empty_detail()
            self.refresh()
            self._flash_status("Entry deleted.")

    # ── SEARCH / FILTER ──────────────────────
    def _on_search(self, *_):
        self.refresh(query=self.search_var.get(), category=self._active_cat)

    def _filter_cat(self, cat: str):
        self._active_cat = cat
        names = {"all":"All Passwords","Login":"Logins","Email":"Emails",
                 "Banking":"Banking","Social":"Social","Work":"Work",
                 "Shopping":"Shopping","API Key":"API Keys","Note":"Notes","Other":"Other"}
        for k, b in self.cat_btns.items():
            b.config(bg=C["surface2"] if k==cat else C["surface"],
                     fg=C["accent"]   if k==cat else C["text2"],
                     font=("Segoe UI",10,"bold") if k==cat else FONT_LABEL)
        if hasattr(self, "topbar_title"): self.topbar_title.config(text=names.get(cat,cat))
        if hasattr(self, "list_inner"):   self.refresh(query=self.search_var.get(), category=cat)

    # ── STATUS BAR ───────────────────────────
    def _flash_status(self, msg: str):
        self.status_lbl.config(text=f"  ✅  {msg}", fg=C["success"])
        self.after(3000, lambda: self.status_lbl.config(
            text=f"  {APP_NAME} v{VERSION}  |  {DEVELOPER}",
            fg=C["text3"]))


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════
if __name__ == "__main__":
    app = EnixApp()
    app.mainloop()
