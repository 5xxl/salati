import psutil
import time
import random
import customtkinter as ctk
import pygame
import json
import os
from threading import Thread
from plyer import *

PRAYER_TIMES_FILE = os.path.join(os.path.expanduser("~"), "prayer_times.json")

def load_prayer_times():
    if os.path.exists(PRAYER_TIMES_FILE):
        with open(PRAYER_TIMES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {
            "Fajr": "05:00 AM",
            "Dhuhr": "12:15 PM",
            "Asr": "03:30 PM",
            "Maghrib": "05:45 PM",
            "Isha": "07:15 PM"
        }

prayer_times = load_prayer_times()
isStart = False
excluded_apps = ["explorer.exe", "code.exe", "msedge.exe", "powershell.exe", "cmd.exe", "py.exe", "python.exe","discord.exe"]

phrases = [
    "ضاع قلبي، فوجدته في الصلاة.",
    "كفى بالمسلم أن يعلم أنّ الصلاة أول ما يحاسب عليه المرء يوم القيامة.",
    "الصلاة مبهجةٌ للنفس، مذهبة للكسل، منشطة للجوارح، ممدة للقوى، شارحة للصدر، مغذية للروح، منورة للقلب.",
    "ما دمت في الصلاة؛ فأنت تقرع باب الملك، ومن يقرع باب الملك يفتح له.",
    "المصلي في ضيافة الرحمن؛ فأحسن وقوفك على أعتابه ونزولك ببابه.",
    "ليس في الدنيا شيء أجلّ ولا أجمل من الصلاة.",
    "الصلاة حصن المسلم الحصين وملجؤه المتين، وهي غذاء للروح، وبلسم للجروح.",
    "الصلاة غوث للملهوف، وأمان للخائف، وسند للضعيف، وهي الملاذ القوي لكل مستضعف ومظلوم.",
    "ما رأيت شيئاً من العبادة ألذّ من الصلاة في جوف الليل.",
    "تفقد الحلاوة في ثلاثة أشياء، في الصلاة والقرآن والذكر، فإن وجدت ذلك فامضِ وأبشر، وإلا فاعلم أن بابك مغلق فعالج فتحه.",
    "الصلاة نور في الدنيا وضياء في الآخرة.",
    "الصلاة تقربك من الله، وتفتح لك أبواب الرحمة.",
    "إن الصلاة كانت على المؤمنين كتابًا موقوتًا.",
    "في الصلاة تجد الراحة والطمأنينة، وتزول الهموم.",
    "الصلاة تجدد الإيمان في القلب، وتنير درب الحياة.",
    "أقرب ما يكون العبد من ربه وهو ساجد.",
    "الصلاة صلة بين العبد وربه، لا تقدر بثمن.",
    "في الصلاة، تجد السكينة التي لا تجدها في أي مكان آخر.",
    "الصلاة شرف للمؤمن، ووسيلة للغفران.",
    "الصلاة حياة القلب، وقوة للروح."
]

def handle_prayer_task(wait_time):
    global isStart
    show_reminder(random.choice(phrases))
    play_sound()
    time.sleep(wait_time)
    close_all_apps()
    ensure_discord_closed()
    isStart = False

def save_prayer_times():
    with open(PRAYER_TIMES_FILE, "w", encoding="utf-8") as file:
        json.dump(prayer_times, file, ensure_ascii=False, indent=4)

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('./play.mp3')
    pygame.mixer.music.play()

def close_all_apps():
    def close_apps_thread():
        current_pid = psutil.Process().pid
        for process in psutil.process_iter(attrs=["pid", "name"]):
            try:
                process_name = process.info["name"].lower()
                process_pid = process.info["pid"]
                if process_pid != current_pid and process_name not in excluded_apps:
                    process.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    Thread(target=close_apps_thread, daemon=True).start()

def ensure_discord_closed():
    def close_discord_thread():
        for process in psutil.process_iter(attrs=["name"]):
            try:
                if process.info["name"].lower() == "discord.exe":
                    process.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    Thread(target=close_discord_thread, daemon=True).start()

def show_reminder(message):
    notification.notify(
        title="تذكير بالصلاة",
        message=message,
        app_name = "صلاتي",
        timeout=25,
    )

def update_prayer_times(prayer_window=None):
    global prayer_times
    prayer_times["Fajr"] = fajr_time_entry.get()
    prayer_times["Dhuhr"] = dhuhr_time_entry.get()
    prayer_times["Asr"] = asr_time_entry.get()
    prayer_times["Maghrib"] = maghrib_time_entry.get()
    prayer_times["Isha"] = isha_time_entry.get()
    save_prayer_times()
    if prayer_window:
        prayer_window.destroy()

current_prayer_window = None
def open_prayer_times_window():
    global current_prayer_window
    if current_prayer_window:
        current_prayer_window.destroy()

    current_prayer_window = ctk.CTkToplevel(root)
    current_prayer_window.title("تعيين مواعيد الصلاة")
    current_prayer_window.geometry("300x400")
    current_prayer_window.configure(fg_color="#2E3440")

    global fajr_time_entry, dhuhr_time_entry, asr_time_entry, maghrib_time_entry, isha_time_entry

    fajr_time_label = ctk.CTkLabel(current_prayer_window, text="الفجر:", font=("Arial", 12), text_color="white")
    fajr_time_label.pack()
    fajr_time_entry = ctk.CTkEntry(current_prayer_window, font=("Arial", 12))
    fajr_time_entry.insert(0, prayer_times["Fajr"])
    fajr_time_entry.pack(pady=5)

    dhuhr_time_label = ctk.CTkLabel(current_prayer_window, text="الظهر:", font=("Arial", 12), text_color="white")
    dhuhr_time_label.pack()
    dhuhr_time_entry = ctk.CTkEntry(current_prayer_window, font=("Arial", 12))
    dhuhr_time_entry.insert(0, prayer_times["Dhuhr"])
    dhuhr_time_entry.pack(pady=5)

    asr_time_label = ctk.CTkLabel(current_prayer_window, text="العصر:", font=("Arial", 12), text_color="white")
    asr_time_label.pack()
    asr_time_entry = ctk.CTkEntry(current_prayer_window, font=("Arial", 12))
    asr_time_entry.insert(0, prayer_times["Asr"])
    asr_time_entry.pack(pady=5)

    maghrib_time_label = ctk.CTkLabel(current_prayer_window, text="المغرب:", font=("Arial", 12), text_color="white")
    maghrib_time_label.pack()
    maghrib_time_entry = ctk.CTkEntry(current_prayer_window, font=("Arial", 12))
    maghrib_time_entry.insert(0, prayer_times["Maghrib"])
    maghrib_time_entry.pack(pady=5)

    isha_time_label = ctk.CTkLabel(current_prayer_window, text="العشاء:", font=("Arial", 12), text_color="white")
    isha_time_label.pack()
    isha_time_entry = ctk.CTkEntry(current_prayer_window, font=("Arial", 12))
    isha_time_entry.insert(0, prayer_times["Isha"])
    isha_time_entry.pack(pady=5)

    save_button = ctk.CTkButton(
        current_prayer_window, text="حفظ",
        command=lambda: update_prayer_times(current_prayer_window),
        font=("Arial", 12)
    )
    save_button.pack(pady=10)

def main_check():
    global isStart
    if isStart:
        return
    isStart = True

    current_time = time.strftime("%I:%M %p")
    if current_time in prayer_times.values():
        try:
            wait_time = int(wait_time_entry.get()) * 60
        except ValueError:
            return

        prayer_thread = Thread(target=handle_prayer_task, args=(wait_time,))
        prayer_thread.start()

    root.after(30000, main_check)

def on_start():
    main_check()

root = ctk.CTk()
root.title("صلاتي")
root.geometry("220x325")
root.configure(fg_color="#2E3440")
root.resizable(False, False)

set_prayer_times_button = ctk.CTkButton(root, text="تعيين مواعيد الصلاة", command=open_prayer_times_window, font=("Arial", 12))
set_prayer_times_button.pack(pady=20)

prayer_label = ctk.CTkLabel(root, text="الإعدادات:", font=("Arial", 16), text_color="white")
prayer_label.pack(pady=10)

wait_time_label = ctk.CTkLabel(root, text="الانتظار قبل القفل (بالدقائق):", font=("Arial", 12), text_color="white")
wait_time_label.pack(pady=10)

wait_time_entry = ctk.CTkEntry(root, font=("Arial", 12))
wait_time_entry.insert(0, "10")
wait_time_entry.pack(pady=5)

lock_apps_var = ctk.BooleanVar(value=True)
lock_apps_checkbox = ctk.CTkCheckBox(root, text="تفعيل قفل التطبيقات أثناء الصلاة", variable=lock_apps_var, font=("Arial", 12), text_color="white")
lock_apps_checkbox.pack(pady=10)

start_button = ctk.CTkButton(root, text="بدء", command=on_start, font=("Arial", 12))
start_button.pack(pady=20)

root.mainloop()