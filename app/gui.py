import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from app.config import SessionConfig
from app.session import ProctorSession
from app.students import STUDENTS_ORDER, is_valid_student
from app.subjects import SUBJECTS_ORDER, minutes_for_subject
from app.used_pairs import UsedPairsStore


MATRICULE_PREFIX = "C-2026-"
MATRICULE_DIGITS = 6


class ProctorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Plateforme Anti-Triche - Examen Pratique")
        self.root.geometry("680x460")

        self.used_store = UsedPairsStore(Path("data") / "used_student_subjects.json")
        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(frame, text="Demarrage de session", font=("Segoe UI", 14, "bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.matricule_digits_var = tk.StringVar()
        self.student_name_var = tk.StringVar()
        self.subject_var = tk.StringVar()
        self.duration_label_var = tk.StringVar(value="Duree: (choisissez une matiere)")

        ttk.Label(frame, text="Matricule etudiant").grid(row=1, column=0, sticky="w", pady=4)

        matricule_frame = ttk.Frame(frame)
        matricule_frame.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(matricule_frame, text=MATRICULE_PREFIX).pack(side=tk.LEFT)

        matricule_entry = ttk.Entry(
            matricule_frame,
            textvariable=self.matricule_digits_var,
            width=12,
        )
        matricule_entry.pack(side=tk.LEFT)

        ttk.Label(matricule_frame, text="  Exemple: 000011").pack(side=tk.LEFT)

        ttk.Label(frame, text="Nom et prenom etudiant").grid(row=2, column=0, sticky="w", pady=4)
        self.student_combo = ttk.Combobox(
            frame,
            textvariable=self.student_name_var,
            values=STUDENTS_ORDER,
            state="readonly",
            width=44,
        )
        self.student_combo.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Matiere").grid(row=3, column=0, sticky="w", pady=4)
        self.subject_combo = ttk.Combobox(
            frame,
            textvariable=self.subject_var,
            values=[],
            state="disabled",
            width=44,
        )
        self.subject_combo.grid(row=3, column=1, sticky="ew", pady=4)
        self.subject_combo.bind("<<ComboboxSelected>>", lambda _e: self._on_subject_changed())

        ttk.Label(frame, textvariable=self.duration_label_var).grid(row=4, column=0, columnspan=2, sticky="w", pady=6)
        frame.columnconfigure(1, weight=1)

        self.status_var = tk.StringVar(value="Saisissez le matricule puis choisissez votre nom.")
        ttk.Label(frame, textvariable=self.status_var, foreground="#0b62d6").grid(
            row=5, column=0, columnspan=2, sticky="w", pady=(14, 8)
        )

        self.start_btn = ttk.Button(frame, text="Demarrer la surveillance", command=self._start_session)
        self.start_btn.grid(row=6, column=0, sticky="w", pady=8)

        ttk.Label(
            frame,
            text="Astuce: pendant la surveillance, appuyez sur 'q' dans la fenetre camera pour arreter.",
            foreground="#666666",
        ).grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.matricule_digits_var.trace_add("write", lambda *_args: self._refresh_subject_choices())
        self.student_name_var.trace_add("write", lambda *_args: self._refresh_subject_choices())
        self._refresh_subject_choices()

    def _student_id(self) -> str:
        digits = self.matricule_digits_var.get().strip()
        return f"{MATRICULE_PREFIX}{digits}"

    def _is_valid_matricule_digits(self) -> bool:
        digits = self.matricule_digits_var.get().strip()
        return len(digits) == MATRICULE_DIGITS and digits.isdigit()

    def _is_valid_student_identity(self) -> bool:
        if not self._is_valid_matricule_digits():
            return False
        student_id = self._student_id()
        student_name = self.student_name_var.get().strip()
        return is_valid_student(student_id, student_name)

    def _refresh_subject_choices(self) -> None:
        previous = self.subject_var.get().strip()

        if not self._is_valid_matricule_digits():
            self.subject_combo["values"] = []
            self.subject_combo.configure(state="disabled")
            self.subject_var.set("")
            self.status_var.set("Saisissez exactement les 6 chiffres du matricule.")
            self._on_subject_changed()
            return

        student_name = self.student_name_var.get().strip()
        if not student_name:
            self.subject_combo["values"] = []
            self.subject_combo.configure(state="disabled")
            self.subject_var.set("")
            self.status_var.set("Choisissez votre nom et prenom dans la liste.")
            self._on_subject_changed()
            return

        if not self._is_valid_student_identity():
            self.subject_combo["values"] = []
            self.subject_combo.configure(state="disabled")
            self.subject_var.set("")
            self.status_var.set("Matricule incorrect pour ce nom. Verifiez les 6 chiffres.")
            self._on_subject_changed()
            return

        student_id = self._student_id()
        used_subjects = self.used_store.used_subjects_for_student(student_id)
        available = [s for s in SUBJECTS_ORDER if s not in used_subjects]

        self.subject_combo["values"] = available
        self.subject_combo.configure(state="readonly" if available else "disabled")

        if previous and previous in available:
            self.subject_var.set(previous)
        else:
            self.subject_var.set("")

        if not available:
            self.status_var.set("Aucune matiere disponible: toutes les matieres ont deja ete utilisees pour ce matricule.")
        else:
            self.status_var.set("Identite valide. Choisissez une matiere.")

        self._on_subject_changed()

    def _on_subject_changed(self) -> None:
        subject = self.subject_var.get().strip()
        if not subject:
            self.duration_label_var.set("Duree: (choisissez une matiere)")
            return
        try:
            minutes = minutes_for_subject(subject)
        except KeyError:
            self.duration_label_var.set("Duree: (matiere inconnue)")
            return
        hours = minutes / 60.0
        if hours.is_integer():
            self.duration_label_var.set(f"Duree: {int(hours)}h ({minutes} minutes)")
        else:
            self.duration_label_var.set(f"Duree: {hours:.1f}h ({minutes} minutes)")

    def _start_session(self) -> None:
        student_id = self._student_id()
        student_name = self.student_name_var.get().strip()
        subject = self.subject_var.get().strip()

        if not self._is_valid_matricule_digits():
            messagebox.showerror(
                "Validation",
                "Le matricule doit contenir exactement 6 chiffres. Exemple: C-2026-000011",
            )
            return

        if not student_name:
            messagebox.showerror("Validation", "Veuillez choisir votre nom et prenom.")
            return

        if not self._is_valid_student_identity():
            messagebox.showerror(
                "Validation",
                "Matricule incorrect pour cet etudiant. Veuillez saisir le bon matricule.",
            )
            return

        if not subject:
            messagebox.showerror("Validation", "Veuillez choisir une matiere.")
            return

        try:
            duration = minutes_for_subject(subject)
        except KeyError as err:
            messagebox.showerror("Validation", str(err))
            return

        config = SessionConfig(
            student_id=student_id,
            subject=subject,
            duration_minutes=duration,
        )
        self.start_btn.configure(state=tk.DISABLED)
        self.status_var.set("Session en cours...")

        threading.Thread(target=self._run_session, args=(config, student_id, subject), daemon=True).start()

    def _run_session(self, config: SessionConfig, student_id: str, subject: str) -> None:
        try:
            session = ProctorSession(config)
            session.run()
            self.used_store.add_pair(student_id, subject)
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Session terminee",
                    f"Resume cree dans:\n{session.session_dir}",
                ),
            )
            self.root.after(0, lambda: self.status_var.set("Session terminee."))
        except Exception as err:
            self.root.after(0, lambda: messagebox.showerror("Erreur", str(err)))
            self.root.after(0, lambda: self.status_var.set("Erreur au lancement."))
        finally:
            self.root.after(0, lambda: self.start_btn.configure(state=tk.NORMAL))
            self.root.after(0, self._refresh_subject_choices)


def launch_gui() -> None:
    root = tk.Tk()
    app = ProctorApp(root)
    _ = app
    root.mainloop()
