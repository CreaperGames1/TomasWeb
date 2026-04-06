"""
TomasekPlays v2.0
- Cool loading screen
- Green & Red theme
- Roblox stats, friends, leaderboard, overlay, badges, groups
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import requests
import threading
import time
import webbrowser
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

BG     = "#0a0f0a"
BG2    = "#0f1a0f"
BG3    = "#162016"
GREEN  = "#00ff5a"
GREEN2 = "#00c944"
RED    = "#ff2244"
RED2   = "#cc1133"
TEXT   = "#e8f5e8"
MUTED  = "#557755"
YELLOW = "#f5c842"
WHITE  = "#ffffff"

def api_get(url, json_body=None):
    try:
        r = requests.post(url, json=json_body, timeout=8) if json_body else requests.get(url, timeout=8)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def search_user(name):
    data = api_get(f"https://users.roblox.com/v1/users/search?keyword={name}&limit=10")
    return data.get("data", []) if data else []

def get_user(uid):
    return api_get(f"https://users.roblox.com/v1/users/{uid}")

def get_friends(uid):
    data = api_get(f"https://friends.roblox.com/v1/users/{uid}/friends")
    return data.get("data", []) if data else []

def get_presence(uids):
    data = api_get("https://presence.roblox.com/v1/presence/users", {"userIds": uids})
    if data and data.get("userPresences"):
        return {p["userId"]: p for p in data["userPresences"]}
    return {}

def get_badges(uid):
    data = api_get(f"https://badges.roblox.com/v1/users/{uid}/badges?limit=20")
    return data.get("data", []) if data else []

def get_groups(uid):
    data = api_get(f"https://groups.roblox.com/v1/users/{uid}/groups/roles")
    return data.get("data", []) if data else []

def presence_label(code):
    return {0: ("Offline", MUTED), 1: ("Na webu", YELLOW),
            2: ("Hraje", GREEN), 3: ("Ve studiu", GREEN2)}.get(code, ("Neznámý", MUTED))


class LoadingScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("")
        w, h = 500, 340
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.configure(fg_color=BG)
        self._build()
        self._anim_step = 0
        self._animate_logo()
        self.after(500, self._start_loading)

    def _build(self):
        border = ctk.CTkFrame(self, fg_color=GREEN, corner_radius=16)
        border.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.98, relheight=0.96)
        inner = ctk.CTkFrame(border, fg_color=BG, corner_radius=14)
        inner.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.992, relheight=0.988)

        self.logo_label = ctk.CTkLabel(inner, text="TomasekPlays",
                                        font=ctk.CTkFont("Courier New", 36, "bold"),
                                        text_color=GREEN)
        self.logo_label.place(relx=0.5, rely=0.28, anchor="center")

        ctk.CTkLabel(inner, text="Roblox Companion v2.0",
                     font=ctk.CTkFont(size=13), text_color=MUTED).place(relx=0.5, rely=0.42, anchor="center")

        ctk.CTkFrame(inner, height=2, fg_color=RED, corner_radius=2).place(
            relx=0.5, rely=0.52, anchor="center", relwidth=0.7)

        self.progress = ctk.CTkProgressBar(inner, width=320, height=10,
                                            progress_color=GREEN, fg_color=BG3, corner_radius=5)
        self.progress.place(relx=0.5, rely=0.67, anchor="center")
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(inner, text="Načítání...",
                                          font=ctk.CTkFont(size=11), text_color=MUTED)
        self.status_label.place(relx=0.5, rely=0.78, anchor="center")

        for i, (x, color) in enumerate([(0.15, GREEN), (0.5, RED), (0.85, GREEN)]):
            ctk.CTkLabel(inner, text="◆", font=ctk.CTkFont(size=10),
                         text_color=color).place(relx=x, rely=0.88, anchor="center")

    def _animate_logo(self):
        colors = [GREEN, GREEN2, WHITE, GREEN2, GREEN, RED, GREEN]
        self.logo_label.configure(text_color=colors[self._anim_step % len(colors)])
        self._anim_step += 1
        self.after(180, self._animate_logo)

    def _start_loading(self):
        steps = [(0.15, "Inicializace..."), (0.35, "Načítání modulů..."),
                 (0.55, "Připojování k Roblox API..."), (0.75, "Příprava rozhraní..."),
                 (1.0, "Hotovo! ✓")]
        self._run_steps(steps, 0)

    def _run_steps(self, steps, i):
        if i >= len(steps):
            self.after(400, self._finish)
            return
        val, text = steps[i]
        self.progress.set(val)
        self.status_label.configure(text=text)
        self.after(420, lambda: self._run_steps(steps, i + 1))

    def _finish(self):
        self.destroy()
        app = TomasekPlays()
        app.mainloop()


class TomasekPlays(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TomasekPlays v2.0")
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"1150x740+{(sw-1150)//2}+{(sh-740)//2}")
        self.minsize(950, 640)
        self.configure(fg_color=BG)
        self.overlay_window = None
        self._build_ui()

    def _build_ui(self):
        sidebar = ctk.CTkFrame(self, width=230, fg_color=BG2, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_frame = ctk.CTkFrame(sidebar, fg_color=BG3, corner_radius=12)
        logo_frame.pack(fill="x", padx=12, pady=(20, 8))
        ctk.CTkLabel(logo_frame, text="TomasekPlays",
                     font=ctk.CTkFont("Courier New", 16, "bold"), text_color=GREEN).pack(pady=(10, 2))
        ctk.CTkLabel(logo_frame, text="◆ Roblox Companion ◆",
                     font=ctk.CTkFont(size=10), text_color=RED).pack(pady=(0, 10))

        ctk.CTkFrame(sidebar, height=2, fg_color=GREEN, corner_radius=2).pack(fill="x", padx=12, pady=(4, 16))

        pages = [("🔍  Hledat hráče", "search"), ("👤  Profil hráče", "profile"),
                 ("🏆  Žebříček", "leaderboard"), ("🎮  Game Overlay", "overlay"),
                 ("🎖️  Odznaky", "badges"), ("👥  Skupiny", "groups"), ("ℹ️   O aplikaci", "about")]

        for label, key in pages:
            ctk.CTkButton(sidebar, text=label, anchor="w", font=ctk.CTkFont(size=13),
                          fg_color="transparent", hover_color=BG3, text_color=TEXT, corner_radius=8,
                          command=lambda k=key: self._show_page(k)).pack(fill="x", padx=10, pady=2)

        ctk.CTkFrame(sidebar, height=2, fg_color=RED, corner_radius=2).pack(fill="x", padx=12, pady=(12, 8))
        ctk.CTkLabel(sidebar, text="v2.0  •  TomasekPlays",
                     font=ctk.CTkFont(size=9), text_color=MUTED).pack(side="bottom", pady=12)

        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self.pages = {}
        self._build_search_page()
        self._build_profile_page()
        self._build_leaderboard_page()
        self._build_overlay_page()
        self._build_badges_page()
        self._build_groups_page()
        self._build_about_page()
        self._show_page("search")

    def _show_page(self, key):
        for f in self.pages.values(): f.pack_forget()
        self.pages[key].pack(fill="both", expand=True, padx=24, pady=24)

    def _header(self, parent, title, subtitle=""):
        ctk.CTkLabel(parent, text=title,
                     font=ctk.CTkFont("Courier New", 26, "bold"), text_color=GREEN).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(parent, text=subtitle, font=ctk.CTkFont(size=12),
                         text_color=MUTED).pack(anchor="w", pady=(2, 14))

    def _card(self, parent, **kw):
        return ctk.CTkFrame(parent, fg_color=BG2, corner_radius=12, **kw)

    # ── Search ────────────────────────────────────────────────────────────────
    def _build_search_page(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        self.pages["search"] = page
        self._header(page, "🔍 Hledat hráče", "Vyhledej jakéhokoli Roblox hráče")
        row = ctk.CTkFrame(page, fg_color="transparent")
        row.pack(fill="x", pady=(0, 14))
        self.search_entry = ctk.CTkEntry(row, placeholder_text="Zadej Roblox jméno...",
                                         font=ctk.CTkFont(size=14), height=44,
                                         fg_color=BG3, border_color=GREEN, text_color=TEXT, corner_radius=10)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self._do_search())
        ctk.CTkButton(row, text="Hledat", width=110, height=44,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=GREEN, hover_color=GREEN2, text_color=BG, corner_radius=10,
                      command=self._do_search).pack(side="left")
        self.search_results = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.search_results.pack(fill="both", expand=True)

    def _do_search(self):
        name = self.search_entry.get().strip()
        if not name: return
        for w in self.search_results.winfo_children(): w.destroy()
        ctk.CTkLabel(self.search_results, text="⏳ Hledám...", text_color=MUTED).pack(pady=20)
        threading.Thread(target=lambda: self.after(0, lambda: self._show_search(search_user(name))), daemon=True).start()

    def _show_search(self, results):
        for w in self.search_results.winfo_children(): w.destroy()
        if not results:
            ctk.CTkLabel(self.search_results, text="Žádný hráč nenalezen.", text_color=RED).pack(pady=20); return
        for user in results:
            card = self._card(self.search_results)
            card.pack(fill="x", pady=5)
            ctk.CTkFrame(card, height=2, fg_color=GREEN, corner_radius=0).pack(fill="x")
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=16, pady=12)
            info = ctk.CTkFrame(inner, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(info, text=user.get("name","?"),
                         font=ctk.CTkFont(size=15, weight="bold"), text_color=TEXT).pack(anchor="w")
            ctk.CTkLabel(info, text=f"ID: {user.get('id')}  •  {user.get('displayName','')}",
                         font=ctk.CTkFont(size=11), text_color=MUTED).pack(anchor="w")
            uid = user.get("id")
            ctk.CTkButton(inner, text="Zobrazit profil", width=120, height=32,
                          fg_color=BG3, hover_color=RED, text_color=GREEN,
                          font=ctk.CTkFont(size=12), corner_radius=8,
                          command=lambda u=uid: self._load_profile(u)).pack(side="right")

    # ── Profile ───────────────────────────────────────────────────────────────
    def _build_profile_page(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        self.pages["profile"] = page
        self._header(page, "👤 Profil hráče", "Detailní informace o hráči")
        row = ctk.CTkFrame(page, fg_color="transparent")
        row.pack(fill="x", pady=(0, 12))
        self.profile_entry = ctk.CTkEntry(row, placeholder_text="Zadej User ID...",
                                           height=42, fg_color=BG3, border_color=RED,
                                           text_color=TEXT, corner_radius=10)
        self.profile_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(row, text="Načíst", width=100, height=42,
                      fg_color=RED, hover_color=RED2, text_color=WHITE,
                      font=ctk.CTkFont(weight="bold"), corner_radius=10,
                      command=lambda: self._load_profile(self.profile_entry.get())).pack(side="left")
        self.profile_scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.profile_scroll.pack(fill="both", expand=True)

    def _load_profile(self, uid):
        try: uid = int(str(uid).strip())
        except: messagebox.showerror("Chyba", "Neplatné User ID"); return
        self._show_page("profile")
        for w in self.profile_scroll.winfo_children(): w.destroy()
        ctk.CTkLabel(self.profile_scroll, text="⏳ Načítám profil...", text_color=MUTED).pack(pady=20)
        threading.Thread(target=self._fetch_profile, args=(uid,), daemon=True).start()

    def _fetch_profile(self, uid):
        user = get_user(uid)
        friends = get_friends(uid)
        presence = get_presence([uid])
        self.after(0, lambda: self._show_profile(user, friends, presence, uid))

    def _show_profile(self, user, friends, presence, uid):
        for w in self.profile_scroll.winfo_children(): w.destroy()
        if not user:
            ctk.CTkLabel(self.profile_scroll, text="Hráč nenalezen.", text_color=RED).pack(); return

        p = presence.get(uid, {})
        status, scolor = presence_label(p.get("userPresenceType", 0))

        top = self._card(self.profile_scroll)
        top.pack(fill="x", pady=(0, 10))
        ctk.CTkFrame(top, height=3, fg_color=GREEN, corner_radius=0).pack(fill="x")
        inner = ctk.CTkFrame(top, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=16)
        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(left, text=user.get("displayName","?"),
                     font=ctk.CTkFont("Courier New", 24, "bold"), text_color=GREEN).pack(anchor="w")
        ctk.CTkLabel(left, text=f"@{user.get('name','?')}",
                     font=ctk.CTkFont(size=13), text_color=MUTED).pack(anchor="w")
        ctk.CTkLabel(left, text=f"● {status}",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=scolor).pack(anchor="w", pady=(6,0))

        right = ctk.CTkFrame(inner, fg_color=BG3, corner_radius=8)
        right.pack(side="right")
        ctk.CTkLabel(right, text=f"ID: {uid}", font=ctk.CTkFont(size=11), text_color=MUTED).pack(padx=14, pady=(8,2))
        ctk.CTkLabel(right, text=f"Připojil: {user.get('created','')[:10]}",
                     font=ctk.CTkFont(size=11), text_color=MUTED).pack(padx=14, pady=(0,8))

        stats = ctk.CTkFrame(self.profile_scroll, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 10))
        for label, val, color in [("Přátelé", len(friends), GREEN),
                                   ("Ověřený", "✓" if user.get("hasVerifiedBadge") else "✗",
                                    GREEN if user.get("hasVerifiedBadge") else RED),
                                   ("Od roku", user.get("created","")[:4], YELLOW)]:
            s = self._card(stats)
            s.pack(side="left", fill="x", expand=True, padx=4)
            ctk.CTkFrame(s, height=3, fg_color=color, corner_radius=0).pack(fill="x")
            ctk.CTkLabel(s, text=str(val), font=ctk.CTkFont("Courier New", 22, "bold"),
                         text_color=color).pack(pady=(12, 2))
            ctk.CTkLabel(s, text=label, font=ctk.CTkFont(size=11), text_color=MUTED).pack(pady=(0, 12))

        desc = user.get("description","").strip()
        if desc:
            d = self._card(self.profile_scroll)
            d.pack(fill="x", pady=(0, 10))
            ctk.CTkLabel(d, text="O hráči", font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=RED).pack(anchor="w", padx=16, pady=(12,4))
            ctk.CTkLabel(d, text=desc[:400], wraplength=620, justify="left",
                         font=ctk.CTkFont(size=12), text_color=TEXT).pack(anchor="w", padx=16, pady=(0,12))

        if friends:
            fc = self._card(self.profile_scroll)
            fc.pack(fill="x", pady=(0, 10))
            ctk.CTkLabel(fc, text=f"Přátelé ({len(friends)})",
                         font=ctk.CTkFont(size=13, weight="bold"), text_color=RED).pack(anchor="w", padx=16, pady=(12,8))
            fids = [f["id"] for f in friends[:20]]
            fpres = get_presence(fids) if fids else {}
            for f in friends[:15]:
                fp = fpres.get(f["id"], {})
                fs, fc2 = presence_label(fp.get("userPresenceType", 0))
                frow = ctk.CTkFrame(fc, fg_color=BG3, corner_radius=8)
                frow.pack(fill="x", padx=12, pady=3)
                ctk.CTkLabel(frow, text=f["name"], font=ctk.CTkFont(size=12), text_color=TEXT).pack(side="left", padx=12, pady=8)
                ctk.CTkLabel(frow, text=f"● {fs}", font=ctk.CTkFont(size=11), text_color=fc2).pack(side="right", padx=12)
            ctk.CTkFrame(fc, fg_color="transparent", height=8).pack()

        ctk.CTkButton(self.profile_scroll, text="🌐  Otevřít na Roblox.com",
                      fg_color=BG3, hover_color=GREEN, text_color=GREEN, corner_radius=10,
                      command=lambda: webbrowser.open(f"https://www.roblox.com/users/{uid}/profile")).pack(fill="x", pady=(0,8))

    # ── Leaderboard ───────────────────────────────────────────────────────────
    def _build_leaderboard_page(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        self.pages["leaderboard"] = page
        self._header(page, "🏆 Žebříček přátel", "Kdo z tvých přátel právě hraje?")
        row = ctk.CTkFrame(page, fg_color="transparent")
        row.pack(fill="x", pady=(0, 12))
        self.lb_entry = ctk.CTkEntry(row, placeholder_text="Tvoje User ID...",
                                     height=42, fg_color=BG3, border_color=GREEN,
                                     text_color=TEXT, corner_radius=10)
        self.lb_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkButton(row, text="Načíst", width=100, height=42,
                      fg_color=GREEN, hover_color=GREEN2, text_color=BG,
                      font=ctk.CTkFont(weight="bold"), corner_radius=10,
                      command=self._load_leaderboard).pack(side="left")
        self.lb_frame = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.lb_frame.pack(fill="both", expand=True)

    def _load_leaderboard(self):
        try: uid = int(self.lb_entry.get().strip())
        except: messagebox.showerror("Chyba", "Zadej platné User ID"); return
        for w in self.lb_frame.winfo_children(): w.destroy()
        ctk.CTkLabel(self.lb_frame, text="⏳ Načítám přátele...", text_color=MUTED).pack(pady=20)
        threading.Thread(target=self._fetch_lb, args=(uid,), daemon=True).start()

    def _fetch_lb(self, uid):
        friends = get_friends(uid)
        if not friends:
            self.after(0, lambda: ctk.CTkLabel(self.lb_frame, text="Žádní přátelé.", text_color=MUTED).pack()); return
        fids = [f["id"] for f in friends[:50]]
        presence = get_presence(fids)
        order = {2: 0, 1: 1, 3: 2, 0: 3}
        sorted_f = sorted(friends[:50], key=lambda f: order.get(presence.get(f["id"],{}).get("userPresenceType",0),3))
        self.after(0, lambda: self._show_lb(sorted_f, presence))

    def _show_lb(self, friends, presence):
        for w in self.lb_frame.winfo_children(): w.destroy()
        header = ctk.CTkFrame(self.lb_frame, fg_color=BG3, corner_radius=8)
        header.pack(fill="x", pady=(0,6))
        for txt, side in [("#","left"),("Jméno","left"),("Status","right"),("Hra","right")]:
            ctk.CTkLabel(header, text=txt, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=GREEN).pack(side=side, padx=14, pady=8)
        for i, f in enumerate(friends, 1):
            p = presence.get(f["id"], {})
            st, sc = presence_label(p.get("userPresenceType", 0))
            game = (p.get("lastLocation","") or "—")[:28]
            card = self._card(self.lb_frame)
            card.pack(fill="x", pady=3)
            medal = {1:"🥇", 2:"🥈", 3:"🥉"}.get(i, f"{i:2d}.")
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=14, pady=10)
            ctk.CTkLabel(inner, text=medal, width=32,
                         font=ctk.CTkFont("Courier New", 13, "bold"), text_color=YELLOW).pack(side="left")
            ctk.CTkLabel(inner, text=f["name"], font=ctk.CTkFont(size=13), text_color=TEXT).pack(side="left", padx=8)
            ctk.CTkLabel(inner, text=game, font=ctk.CTkFont(size=11), text_color=MUTED).pack(side="right", padx=8)
            ctk.CTkLabel(inner, text=f"● {st}", font=ctk.CTkFont(size=12), text_color=sc).pack(side="right")

    # ── Overlay ───────────────────────────────────────────────────────────────
    def _build_overlay_page(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        self.pages["overlay"] = page
        self._header(page, "🎮 Game Overlay", "Plovoucí okno nad hrou")
        info = self._card(page)
        info.pack(fill="x", pady=(0,16))
        ctk.CTkFrame(info, height=3, fg_color=RED, corner_radius=0).pack(fill="x")
        ctk.CTkLabel(info, text="Overlay se zobrazí nad tvou hrou.\nUkazuje čas, časovač sezení a rychlé poznámky.",
                     font=ctk.CTkFont(size=13), text_color=TEXT, justify="left").pack(padx=20, pady=16)
        ctk.CTkLabel(page, text="Průhlednost:", font=ctk.CTkFont(size=12), text_color=MUTED).pack(anchor="w")
        self.opacity_slider = ctk.CTkSlider(page, from_=0.3, to=1.0, progress_color=GREEN, button_color=RED)
        self.opacity_slider.set(0.88)
        self.opacity_slider.pack(fill="x", pady=(4, 16))
        self.overlay_btn = ctk.CTkButton(page, text="▶  Spustit Overlay", height=50,
                                          font=ctk.CTkFont(size=16, weight="bold"),
                                          fg_color=GREEN, hover_color=GREEN2, text_color=BG,
                                          corner_radius=12, command=self._toggle_overlay)
        self.overlay_btn.pack(fill="x")

    def _toggle_overlay(self):
        if self.overlay_window and self.overlay_window.winfo_exists():
            self.overlay_window.destroy()
            self.overlay_window = None
            self.overlay_btn.configure(text="▶  Spustit Overlay", fg_color=GREEN)
        else:
            self._launch_overlay()
            self.overlay_btn.configure(text="■  Zavřít Overlay", fg_color=RED)

    def _launch_overlay(self):
        ow = ctk.CTkToplevel(self)
        ow.title("TomasekPlays")
        ow.geometry("300x220+10+10")
        ow.attributes("-topmost", True)
        ow.attributes("-alpha", self.opacity_slider.get())
        ow.configure(fg_color=BG2)
        self.overlay_window = ow
        h = ctk.CTkFrame(ow, fg_color=BG3, corner_radius=0)
        h.pack(fill="x")
        ctk.CTkFrame(h, height=3, fg_color=GREEN, corner_radius=0).pack(fill="x")
        ctk.CTkLabel(h, text="◆ TomasekPlays",
                     font=ctk.CTkFont("Courier New", 12, "bold"), text_color=GREEN).pack(pady=6)
        self._ov_clock = ctk.CTkLabel(ow, text="", font=ctk.CTkFont("Courier New", 30, "bold"), text_color=GREEN)
        self._ov_clock.pack(pady=(10, 0))
        self._ov_date = ctk.CTkLabel(ow, text="", font=ctk.CTkFont(size=11), text_color=MUTED)
        self._ov_date.pack()
        self._ov_session_start = time.time()
        self._ov_timer = ctk.CTkLabel(ow, text="Sezení: 00:00", font=ctk.CTkFont(size=12), text_color=RED)
        self._ov_timer.pack()
        ctk.CTkEntry(ow, placeholder_text="Rychlá poznámka...",
                     fg_color=BG3, text_color=TEXT, border_color=GREEN, corner_radius=8).pack(fill="x", padx=10, pady=(8,10))
        self._update_overlay()

    def _update_overlay(self):
        if not self.overlay_window or not self.overlay_window.winfo_exists(): return
        now = datetime.now()
        self._ov_clock.configure(text=now.strftime("%H:%M:%S"))
        self._ov_date.configure(text=now.strftime("%d. %m. %Y"))
        elapsed = int(time.time() - self._ov_session_start)
        m, s = divmod(elapsed, 60)
        self._ov_timer.configure(text=f"Sezení: {m:02d}:{s:02d}")
        self.overlay_window.after(1000, self._update_overlay)

    # ── Badges ────────────────────────────────────────────────────────────────
    def _build_badges_page(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        self.pages["badges"] = page
        self._header(page, "🎖️ Odznaky hráče", "Zobraz odznaky libovolného hráče")
        row = ctk.CTkFrame(page, fg_color="transparent")
        row.pack(fill="x", pady=(0,12))
        self.badge_entry = ctk.CTkEntry(row, placeholder_text="User ID hráče...",
                                        height=42, fg_color=BG3, border_color=YELLOW,
                                        text_color=TEXT, corner_radius=10)
        self.badge_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkButton(row, text="Načíst", width=100, height=42,
                      fg_color=YELLOW, hover_color="#c9a000", text_color=BG,
                      font=ctk.CTkFont(weight="bold"), corner_radius=10,
                      command=self._load_badges).pack(side="left")
        self.badge_frame = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.badge_frame.pack(fill="both", expand=True)

    def _load_badges(self):
        try: uid = int(self.badge_entry.get().strip())
        except: messagebox.showerror("Chyba", "Zadej platné User ID"); return
        for w in self.badge_frame.winfo_children(): w.destroy()
        ctk.CTkLabel(self.badge_frame, text="⏳ Načítám odznaky...", text_color=MUTED).pack(pady=20)
        threading.Thread(target=lambda: self.after(0, lambda: self._show_badges(get_badges(uid))), daemon=True).start()

    def _show_badges(self, badges):
        for w in self.badge_frame.winfo_children(): w.destroy()
        if not badges:
            ctk.CTkLabel(self.badge_frame, text="Žádné odznaky.", text_color=MUTED).pack(pady=20); return
        ctk.CTkLabel(self.badge_frame, text=f"Nalezeno {len(badges)} odznaků:",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=YELLOW).pack(anchor="w", pady=(0,8))
        for b in badges:
            card = self._card(self.badge_frame)
            card.pack(fill="x", pady=4)
            ctk.CTkFrame(card, height=2, fg_color=YELLOW, corner_radius=0).pack(fill="x")
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=16, pady=10)
            ctk.CTkLabel(inner, text="🎖️", font=ctk.CTkFont(size=20)).pack(side="left", padx=(0,10))
            info = ctk.CTkFrame(inner, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(info, text=b.get("name","?"),
                         font=ctk.CTkFont(size=13, weight="bold"), text_color=YELLOW).pack(anchor="w")
            desc = b.get("description","")
            if desc:
                ctk.CTkLabel(info, text=desc[:80], font=ctk.CTkFont(size=11), text_color=MUTED).pack(anchor="w")

    # ── Groups ────────────────────────────────────────────────────────────────
    def _build_groups_page(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        self.pages["groups"] = page
        self._header(page, "👥 Skupiny hráče", "Zobraz skupiny libovolného hráče")
        row = ctk.CTkFrame(page, fg_color="transparent")
        row.pack(fill="x", pady=(0,12))
        self.group_entry = ctk.CTkEntry(row, placeholder_text="User ID hráče...",
                                        height=42, fg_color=BG3, border_color=RED,
                                        text_color=TEXT, corner_radius=10)
        self.group_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkButton(row, text="Načíst", width=100, height=42,
                      fg_color=RED, hover_color=RED2, text_color=WHITE,
                      font=ctk.CTkFont(weight="bold"), corner_radius=10,
                      command=self._load_groups).pack(side="left")
        self.group_frame = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.group_frame.pack(fill="both", expand=True)

    def _load_groups(self):
        try: uid = int(self.group_entry.get().strip())
        except: messagebox.showerror("Chyba", "Zadej platné User ID"); return
        for w in self.group_frame.winfo_children(): w.destroy()
        ctk.CTkLabel(self.group_frame, text="⏳ Načítám skupiny...", text_color=MUTED).pack(pady=20)
        threading.Thread(target=lambda: self.after(0, lambda: self._show_groups(get_groups(uid))), daemon=True).start()

    def _show_groups(self, groups):
        for w in self.group_frame.winfo_children(): w.destroy()
        if not groups:
            ctk.CTkLabel(self.group_frame, text="Hráč není v žádné skupině.", text_color=MUTED).pack(pady=20); return
        ctk.CTkLabel(self.group_frame, text=f"Nalezeno {len(groups)} skupin:",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=RED).pack(anchor="w", pady=(0,8))
        for g in groups:
            grp = g.get("group", {})
            role = g.get("role", {})
            card = self._card(self.group_frame)
            card.pack(fill="x", pady=4)
            ctk.CTkFrame(card, height=2, fg_color=RED, corner_radius=0).pack(fill="x")
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=16, pady=10)
            ctk.CTkLabel(inner, text="👥", font=ctk.CTkFont(size=20)).pack(side="left", padx=(0,10))
            info = ctk.CTkFrame(inner, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(info, text=grp.get("name","?"),
                         font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT).pack(anchor="w")
            ctk.CTkLabel(info, text=f"Role: {role.get('name','?')}  •  ID: {grp.get('id','?')}",
                         font=ctk.CTkFont(size=11), text_color=MUTED).pack(anchor="w")
            gid = grp.get("id")
            ctk.CTkButton(inner, text="Otevřít", width=80, height=28,
                          fg_color=BG3, hover_color=RED, text_color=RED,
                          font=ctk.CTkFont(size=11), corner_radius=6,
                          command=lambda g=gid: webbrowser.open(f"https://www.roblox.com/groups/{g}")).pack(side="right")

    # ── About ─────────────────────────────────────────────────────────────────
    def _build_about_page(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        self.pages["about"] = page
        self._header(page, "ℹ️ O aplikaci", "")
        card = self._card(page)
        card.pack(fill="x")
        ctk.CTkFrame(card, height=3, fg_color=GREEN, corner_radius=0).pack(fill="x")
        ctk.CTkLabel(card, text="TomasekPlays",
                     font=ctk.CTkFont("Courier New", 28, "bold"), text_color=GREEN).pack(pady=(20,4))
        ctk.CTkLabel(card, text="◆ Roblox Companion App ◆",
                     font=ctk.CTkFont(size=13), text_color=RED).pack()
        ctk.CTkFrame(card, height=2, fg_color=BG3, corner_radius=0).pack(fill="x", padx=20, pady=16)
        for label, val in [("Verze","2.0.0"),("Vytvořeno pro","TomasekPlays"),
                           ("Postaveno na","Python + CustomTkinter"),("Data z","Roblox Public API")]:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=24, pady=5)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=12),
                         text_color=MUTED, width=130, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=val, font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=TEXT).pack(side="left")
        ctk.CTkFrame(card, fg_color="transparent", height=20).pack()


if __name__ == "__main__":
    loading = LoadingScreen()
    loading.mainloop()
