import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

# ── Data file ────────────────────────────────────────────────────────────────
DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#0f0f0f"
PANEL     = "#1a1a1a"
CARD      = "#222222"
CARD_DONE = "#181818"
ACCENT    = "#e8c547"       # warm gold
ACCENT2   = "#e05a4e"       # coral red
GREEN     = "#4ecb71"
FG        = "#f0ede6"
FG_DIM    = "#888880"
FG_DONE   = "#4a4a44"
BORDER    = "#333330"
FONT_H    = ("Georgia", 22, "bold")
FONT_SUB  = ("Georgia", 11, "italic")
FONT_BODY = ("Courier New", 12)
FONT_SMALL= ("Courier New", 10)
FONT_BTN  = ("Courier New", 11, "bold")
FONT_TAG  = ("Courier New", 9)

PRIORITIES = {"High": ACCENT2, "Medium": ACCENT, "Low": GREEN}

# ── App ───────────────────────────────────────────────────────────────────────
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✦ TASK FORGE")
        self.root.geometry("780x680")
        self.root.minsize(680, 500)
        self.root.configure(bg=BG)

        self.tasks = load_tasks()
        self.filter_var = tk.StringVar(value="All")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh())

        self._build_ui()
        self.refresh()

    # ── UI construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        # ─ Header ─
        hdr = tk.Frame(self.root, bg=BG, pady=18)
        hdr.pack(fill="x", padx=28)

        tk.Label(hdr, text="✦ TASK FORGE", font=FONT_H,
                 bg=BG, fg=ACCENT).pack(side="left")
        tk.Label(hdr, text="  your work, forged in order",
                 font=FONT_SUB, bg=BG, fg=FG_DIM).pack(side="left", padx=6, pady=4)

        # ─ Toolbar ─
        bar = tk.Frame(self.root, bg=PANEL, pady=10, padx=18)
        bar.pack(fill="x", padx=0)

        # Search
        tk.Label(bar, text="⌕", font=("Courier New", 14), bg=PANEL, fg=FG_DIM).pack(side="left")
        self.search_entry = tk.Entry(bar, textvariable=self.search_var,
                                     font=FONT_BODY, bg=CARD, fg=FG,
                                     insertbackground=ACCENT, relief="flat",
                                     bd=0, width=22)
        self.search_entry.pack(side="left", ipady=5, padx=(4,16))
        self.search_entry.insert(0, "Search tasks…")
        self.search_entry.bind("<FocusIn>",  self._clear_placeholder)
        self.search_entry.bind("<FocusOut>", self._restore_placeholder)

        # Filter tabs
        for label in ("All", "Active", "Done"):
            tk.Button(bar, text=label, font=FONT_BTN,
                      bg=PANEL, fg=FG_DIM, activebackground=ACCENT,
                      activeforeground=BG, relief="flat", bd=0, padx=10, pady=4,
                      cursor="hand2",
                      command=lambda l=label: self._set_filter(l)
                      ).pack(side="left", padx=2)

        # Add button
        tk.Button(bar, text="+ ADD TASK", font=FONT_BTN,
                  bg=ACCENT, fg=BG, activebackground="#f5d76e",
                  activeforeground=BG, relief="flat", bd=0,
                  padx=14, pady=5, cursor="hand2",
                  command=self.add_task).pack(side="right", padx=4)

        # ─ Stats bar ─
        self.stats_frame = tk.Frame(self.root, bg=BG, pady=6)
        self.stats_frame.pack(fill="x", padx=28)

        # ─ Task list ─
        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview,
                                 bg=PANEL, troughcolor=BG, bd=0, width=8)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.task_frame = tk.Frame(canvas, bg=BG)
        self.canvas_window = canvas.create_window((0, 0), window=self.task_frame, anchor="nw")

        self.task_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
            lambda e: canvas.itemconfig(self.canvas_window, width=e.width))
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # ─ Bottom bar ─
        bot = tk.Frame(self.root, bg=PANEL, pady=8)
        bot.pack(fill="x")
        tk.Button(bot, text="⌫  CLEAR DONE", font=FONT_BTN,
                  bg=PANEL, fg=ACCENT2, activebackground=ACCENT2,
                  activeforeground=BG, relief="flat", bd=0,
                  padx=12, pady=4, cursor="hand2",
                  command=self.clear_done).pack(side="left", padx=18)
        tk.Label(bot, text="click task to edit  •  ✓ to complete  •  ✕ to delete",
                 font=FONT_TAG, bg=PANEL, fg=FG_DIM).pack(side="right", padx=18)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _clear_placeholder(self, e):
        if self.search_entry.get() == "Search tasks…":
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg=FG)

    def _restore_placeholder(self, e):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search tasks…")
            self.search_entry.config(fg=FG_DIM)

    def _set_filter(self, val):
        self.filter_var.set(val)
        self.refresh()

    def _filtered_tasks(self):
        q = self.search_var.get().lower()
        if q == "search tasks…": q = ""
        f = self.filter_var.get()
        out = []
        for i, t in enumerate(self.tasks):
            if f == "Active" and t.get("done"): continue
            if f == "Done"   and not t.get("done"): continue
            if q and q not in t["title"].lower() and q not in t.get("note","").lower(): continue
            out.append((i, t))
        return out

    # ── Stats ─────────────────────────────────────────────────────────────────
    def _update_stats(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()
        total  = len(self.tasks)
        done   = sum(1 for t in self.tasks if t.get("done"))
        active = total - done
        pct    = int(done/total*100) if total else 0

        for label, val, color in [
            (f"{total}",  "total",  FG_DIM),
            (f"{active}", "active", ACCENT),
            (f"{done}",   "done",   GREEN),
            (f"{pct}%",   "complete", FG_DIM),
        ]:
            f = tk.Frame(self.stats_frame, bg=BG)
            f.pack(side="left", padx=(0, 24))
            tk.Label(f, text=label, font=("Courier New", 16, "bold"),
                     bg=BG, fg=color).pack(side="left")
            tk.Label(f, text=f" {val}", font=FONT_SMALL,
                     bg=BG, fg=FG_DIM).pack(side="left", pady=2)

        # Progress bar
        pf = tk.Frame(self.stats_frame, bg=BG)
        pf.pack(side="right", padx=4, pady=2)
        bar_w = 160
        tk.Label(pf, text="progress", font=FONT_TAG, bg=BG, fg=FG_DIM).pack(anchor="e")
        pb_bg = tk.Frame(pf, bg=BORDER, width=bar_w, height=6)
        pb_bg.pack()
        pb_bg.pack_propagate(False)
        filled = max(2, int(bar_w * pct / 100)) if pct else 0
        tk.Frame(pb_bg, bg=GREEN, width=filled, height=6).place(x=0, y=0)

    # ── Task cards ────────────────────────────────────────────────────────────
    def refresh(self):
        for w in self.task_frame.winfo_children():
            w.destroy()
        self._update_stats()

        items = self._filtered_tasks()
        if not items:
            msg = "No tasks yet — click + ADD TASK to begin!" if not self.tasks else "No tasks match this filter."
            tk.Label(self.task_frame, text=msg, font=FONT_BODY,
                     bg=BG, fg=FG_DIM, pady=40).pack()
            return

        for idx, (real_idx, task) in enumerate(items):
            self._task_card(real_idx, task, idx)

    def _task_card(self, real_idx, task, row):
        done = task.get("done", False)
        pri  = task.get("priority", "Medium")
        pri_color = PRIORITIES.get(pri, ACCENT)

        card = tk.Frame(self.task_frame, bg=CARD_DONE if done else CARD,
                        pady=10, padx=14, cursor="hand2")
        card.pack(fill="x", padx=0, pady=3)

        # Left accent strip
        tk.Frame(card, bg=FG_DONE if done else pri_color, width=4).pack(side="left", fill="y", padx=(0,10))

        # Check button
        chk_sym = "✓" if done else "○"
        chk_col = GREEN if done else FG_DIM
        tk.Button(card, text=chk_sym, font=("Courier New", 14, "bold"),
                  bg=CARD_DONE if done else CARD, fg=chk_col,
                  activebackground=GREEN, activeforeground=BG,
                  relief="flat", bd=0, cursor="hand2", width=2,
                  command=lambda i=real_idx: self.toggle_done(i)).pack(side="left", padx=(0,8))

        # Text block
        txt = tk.Frame(card, bg=CARD_DONE if done else CARD)
        txt.pack(side="left", fill="both", expand=True)

        title_fg = FG_DONE if done else FG
        title_font = ("Courier New", 12, "overstrike") if done else ("Courier New", 12, "bold")
        tk.Label(txt, text=task["title"], font=title_font,
                 bg=CARD_DONE if done else CARD, fg=title_fg,
                 anchor="w").pack(fill="x")

        if task.get("note"):
            tk.Label(txt, text=task["note"], font=FONT_SMALL,
                     bg=CARD_DONE if done else CARD, fg=FG_DONE,
                     anchor="w").pack(fill="x")

        # Meta row
        meta = tk.Frame(txt, bg=CARD_DONE if done else CARD)
        meta.pack(fill="x", pady=(3,0))

        tk.Label(meta, text=f"▲ {pri}", font=FONT_TAG,
                 bg=CARD_DONE if done else CARD,
                 fg=FG_DONE if done else pri_color).pack(side="left", padx=(0,12))

        if task.get("due"):
            tk.Label(meta, text=f"⏰ {task['due']}", font=FONT_TAG,
                     bg=CARD_DONE if done else CARD, fg=FG_DIM).pack(side="left", padx=(0,12))

        tk.Label(meta, text=f"added {task.get('created','—')}", font=FONT_TAG,
                 bg=CARD_DONE if done else CARD, fg=FG_DONE).pack(side="left")

        # Right buttons
        btn_frame = tk.Frame(card, bg=CARD_DONE if done else CARD)
        btn_frame.pack(side="right", padx=(8,0))

        tk.Button(btn_frame, text="✎", font=("Courier New", 13),
                  bg=CARD_DONE if done else CARD, fg=ACCENT,
                  activebackground=ACCENT, activeforeground=BG,
                  relief="flat", bd=0, cursor="hand2", padx=6,
                  command=lambda i=real_idx: self.edit_task(i)).pack(side="left")

        tk.Button(btn_frame, text="✕", font=("Courier New", 13),
                  bg=CARD_DONE if done else CARD, fg=ACCENT2,
                  activebackground=ACCENT2, activeforeground=BG,
                  relief="flat", bd=0, cursor="hand2", padx=6,
                  command=lambda i=real_idx: self.delete_task(i)).pack(side="left")

    # ── Task dialog ───────────────────────────────────────────────────────────
    def _task_dialog(self, title="New Task", task=None):
        dlg = tk.Toplevel(self.root)
        dlg.title(title)
        dlg.geometry("460x360")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.grab_set()

        result = {}

        def label(parent, text):
            tk.Label(parent, text=text, font=FONT_SMALL,
                     bg=BG, fg=FG_DIM).pack(anchor="w", padx=24, pady=(10,2))

        def entry(parent, default=""):
            e = tk.Entry(parent, font=FONT_BODY, bg=CARD, fg=FG,
                         insertbackground=ACCENT, relief="flat", bd=0)
            e.pack(fill="x", padx=24, ipady=6)
            e.insert(0, default)
            return e

        tk.Label(dlg, text=title, font=("Courier New", 14, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=(18,0))

        label(dlg, "TASK TITLE *")
        title_e = entry(dlg, task["title"] if task else "")

        label(dlg, "NOTE / DESCRIPTION")
        note_e = entry(dlg, task.get("note","") if task else "")

        label(dlg, "DUE DATE  (e.g. 2025-12-31)")
        due_e = entry(dlg, task.get("due","") if task else "")

        label(dlg, "PRIORITY")
        pri_var = tk.StringVar(value=task.get("priority","Medium") if task else "Medium")
        pf = tk.Frame(dlg, bg=BG)
        pf.pack(anchor="w", padx=24, pady=4)
        for p in ("High", "Medium", "Low"):
            tk.Radiobutton(pf, text=p, variable=pri_var, value=p,
                           font=FONT_SMALL, bg=BG, fg=PRIORITIES[p],
                           selectcolor=CARD, activebackground=BG,
                           activeforeground=PRIORITIES[p]).pack(side="left", padx=8)

        def save():
            t = title_e.get().strip()
            if not t:
                messagebox.showwarning("Required", "Task title cannot be empty.", parent=dlg)
                return
            result["title"]    = t
            result["note"]     = note_e.get().strip()
            result["due"]      = due_e.get().strip()
            result["priority"] = pri_var.get()
            dlg.destroy()

        tk.Button(dlg, text="SAVE TASK", font=FONT_BTN,
                  bg=ACCENT, fg=BG, activebackground="#f5d76e",
                  activeforeground=BG, relief="flat", bd=0,
                  padx=20, pady=8, cursor="hand2",
                  command=save).pack(pady=16)

        dlg.wait_window()
        return result if result else None

    # ── Actions ───────────────────────────────────────────────────────────────
    def add_task(self):
        data = self._task_dialog("✦ ADD NEW TASK")
        if data:
            data["done"]    = False
            data["created"] = datetime.now().strftime("%b %d")
            self.tasks.append(data)
            save_tasks(self.tasks)
            self.refresh()

    def edit_task(self, idx):
        data = self._task_dialog("✎ EDIT TASK", task=self.tasks[idx])
        if data:
            self.tasks[idx].update(data)
            save_tasks(self.tasks)
            self.refresh()

    def toggle_done(self, idx):
        self.tasks[idx]["done"] = not self.tasks[idx].get("done", False)
        save_tasks(self.tasks)
        self.refresh()

    def delete_task(self, idx):
        name = self.tasks[idx]["title"]
        if messagebox.askyesno("Delete Task",
                               f"Delete '{name}'?\nThis cannot be undone.",
                               parent=self.root):
            self.tasks.pop(idx)
            save_tasks(self.tasks)
            self.refresh()

    def clear_done(self):
        done_count = sum(1 for t in self.tasks if t.get("done"))
        if not done_count:
            messagebox.showinfo("Nothing to clear", "No completed tasks to remove.", parent=self.root)
            return
        if messagebox.askyesno("Clear Done",
                               f"Remove all {done_count} completed task(s)?",
                               parent=self.root):
            self.tasks = [t for t in self.tasks if not t.get("done")]
            save_tasks(self.tasks)
            self.refresh()

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = TodoApp(root)
    root.mainloop()
