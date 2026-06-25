import tkinter as tk
from tkinter import messagebox
import pymem


# --- الإعدادات والمتغيرات العامة ---
PROCESS_NAME = "SONIC3K.EXE"
pm = None

# حالات الغش (True = فعال، False = معطل)
rings_cheat_active = False
lives_cheat_active = False

# العناوين الصحيحة التي تم اصطيادها وتأكيدها
ADDR_RINGS = 0x08FFFE20
ADDR_LIVES = 0x08FFFE12




# --- دوال الاتصال والتحكم بالذاكرة ---

def check_game_connection():
    """البحث المستمر عن اللعبة في الخلفية للربط التلقائي"""
    global pm
    if pm is None:
        try:
            pm = pymem.Pymem(PROCESS_NAME)
            lbl_status.config(text="STATUS: CONNECTED TO GAME", fg="#008000") # أخضر كلاسيكي
            btn_rings.config(state="normal")
            btn_lives.config(state="normal")
        except Exception:
            pm = None
            lbl_status.config(text="STATUS: WAITING FOR SONIC3K.EXE...", fg="#A04000") # بني/برتقالي داكن كلاسيكي
            disable_cheats()
            root.after(1000, check_game_connection)

def disable_cheats():
    """تعطيل الأزرار وإعادة تعيين الحالات لو اللعبة قفلت"""
    global rings_cheat_active, lives_cheat_active
    rings_cheat_active = False
    lives_cheat_active = False
    btn_rings.config(text="FREEZE RINGS (99)", bg="#F0F0F0", fg="#000000", relief="raised", state="disabled")
    btn_lives.config(text="FREEZE LIVES (99)", bg="#F0F0F0", fg="#000000", relief="raised", state="disabled")

# --- حلقات التثبيت المستمر (Freeze Loops) ---

def freeze_rings():
    """حلقة تثبيت الرينجز على 99"""
    global rings_cheat_active
    if rings_cheat_active and pm:
        try:
            pm.write_short(ADDR_RINGS, 99)
            root.after(15, freeze_rings)
        except Exception:
            handle_disconnection()

def freeze_lives():
    """حلقة تثبيت الـ Lives على 99"""
    global lives_cheat_active
    if lives_cheat_active and pm:
        try:
            pm.write_short(ADDR_LIVES, 99)
            root.after(50, freeze_lives)
        except Exception:
            handle_disconnection()

def handle_disconnection():
    """التعامل الذكي في حالة إغلاق اللعبة فجأة"""
    global pm
    pm = None
    disable_cheats()
    check_game_connection()

# --- دوال التفعيل (Toggle Functions) ---

def toggle_rings():
    global rings_cheat_active
    if not rings_cheat_active:
        rings_cheat_active = True
        btn_rings.config(text="RINGS: ACTIVE [99]", bg="#008000", fg="#FFFFFF", relief="sunken")
        freeze_rings()
    else:
        rings_cheat_active = False
        btn_rings.config(text="FREEZE RINGS (99)", bg="#F0F0F0", fg="#000000", relief="raised")

def toggle_lives():
    global lives_cheat_active
    if not lives_cheat_active:
        lives_cheat_active = True
        btn_lives.config(text="LIVES: ACTIVE [99]", bg="#000080", fg="#FFFFFF", relief="sunken")
        freeze_lives()
    else:
        lives_cheat_active = False
        btn_lives.config(text="FREEZE LIVES (99)", bg="#F0F0F0", fg="#000000", relief="raised")

def show_about():
    """نافذة معلومات البرنامج الكلاسيكية"""
    messagebox.showinfo(
        "About Tool",
        "Sonic 3 & Knuckles Collection PC Port Cheat Trainer\n"
        "Build Version: 1.0 (Alpha build)\n\n"
        "Noureldeen - Tool Programming\n"
        "All Rights Reserved."
    )

# --- إعداد نافذة الـ GUI وتصميمها الكلاسيكي الرمادي ---

root = tk.Tk()
root.title("Sonic 3 and Knuckles Collection - Trainer")
root.geometry("480x340")
root.resizable(False, False)
root.config(bg="#D4D0C8") # الرمادي الكلاسيكي الموحد للخلفية الكاملة


# --- 1. البانر العلوي الرمادي المحدد (Classic Grey Bordered Header) ---
header_frame = tk.Frame(root, bg="#D4D0C8", bd=2, relief="groove")
header_frame.pack(fill="x", padx=15, pady=15)

title_label = tk.Label(
    header_frame,
    text="SONIC 3 & KNUCKLES",
    font=("Arial Black", 20, "bold"),
    bg="#D4D0C8",
    fg="#000000"
)
title_label.pack(pady=5)

subtitle_label = tk.Label(
    header_frame,
    text="CHEAT TRAINER",
    font=("MS Sans Serif", 9, "bold"),
    bg="#D4D0C8",
    fg="#444444"
)
subtitle_label.pack(pady=2)

# --- 2. منطقة التحكم والحالة (Main Control Area) ---
main_frame = tk.Frame(root, bg="#D4D0C8")
main_frame.pack(fill="both", expand=True, padx=20)

# مؤشر الحالة (Status)
lbl_status = tk.Label(
    main_frame,
    text="STATUS: INITIALIZING...",
    font=("MS Sans Serif", 10, "bold"),
    bg="#D4D0C8",
    fg="#000000"
)
lbl_status.pack(pady=10)

# أزرار الغش الكلاسيكية (Cheat Buttons)
btn_rings = tk.Button(
    main_frame,
    text="FREEZE RINGS (99)",
    font=("Arial", 11, "bold"),
    bg="#F0F0F0",
    fg="#000000",
    bd=3,
    relief="raised",
    command=toggle_rings,
    state="disabled",
    width=25
)
btn_rings.pack(pady=8)

btn_lives = tk.Button(
    main_frame,
    text="FREEZE LIVES (99)",
    font=("Arial", 11, "bold"),
    bg="#F0F0F0",
    fg="#000000",
    bd=3,
    relief="raised",
    command=toggle_lives,
    state="disabled",
    width=25
)
btn_lives.pack(pady=8)

# --- 3. الشريط السفلي للأزرار والمعلومات (Footer Panel) ---
footer_frame = tk.Frame(root, bg="#D4D0C8", bd=1, relief="sunken")
footer_frame.pack(fill="x", side="bottom", ipady=5)

# زر الـ About
btn_about = tk.Button(
    footer_frame,
    text="About Tool...",
    font=("MS Sans Serif", 8),
    command=show_about,
    bd=2,
    relief="raised"
)
btn_about.pack(side="left", padx=10, pady=5)

# زر الخروج الكلاسيكي
btn_exit = tk.Button(
    footer_frame,
    text="Exit Tool",
    font=("MS Sans Serif", 8),
    command=root.quit,
    bd=2,
    relief="raised",
    width=10
)
btn_exit.pack(side="right", padx=10, pady=5)

# تسمية المبرمج القصيرة في الفوتر
lbl_credits = tk.Label(
    footer_frame,
    #text="Noureldeen Tool Programming",
    font=("MS Sans Serif", 8, "italic"),
    bg="#D4D0C8",
    fg="#555555"
)
lbl_credits.pack(side="right", padx=20, pady=5)

# --- بدء تشغيل محرك كشف اللعبة تلقائياً ---
root.after(100, check_game_connection)

root.mainloop()