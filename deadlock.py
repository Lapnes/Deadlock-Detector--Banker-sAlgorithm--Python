import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# --- Custom Widgets (Rounded look for modern GUI) ---

class RoundedButton(ttk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = ttk.Style()
        # Custom style configuration
        self.style.configure("Rounded.TButton", padding=10, relief="flat", background="#4CAF50", foreground="white", font=("Helvetica", 12, "bold"))
        self.configure(style="Rounded.TButton")

class RoundedEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = ttk.Style()
        # Custom style configuration
        self.style.configure("Rounded.TEntry", padding=10, relief="flat", background="white", foreground="black", font=("Helvetica", 12))
        self.configure(style="Rounded.TEntry")

# --- Main Application Class ---

class DeadlockDetection:
    def __init__(self, master):
        self.master = master
        self.master.title("Deadlock Detection and Prevention (Banker's Algorithm)")
        self.master.configure(bg="white")
        self.master.geometry("1400x850") # Window size adjusted

        # Main Frame setup
        self.main_frame = ttk.Frame(master, padding=20)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Title Label
        self.title_label = ttk.Label(self.main_frame, text="Deadlock Detection and Prevention (Banker's Algorithm)", font=("Helvetica", 18, "bold"), background="white")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Input Frame (Left Side)
        self.input_frame = ttk.Frame(self.main_frame, padding=10, style='White.TFrame')
        self.input_frame.grid(row=1, column=0, sticky="n")

        # Output Frame (Right Side - for Logging)
        self.output_frame = ttk.Frame(self.main_frame, padding=10, style='White.TFrame')
        self.output_frame.grid(row=1, column=1, rowspan=10, sticky="nwes")
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Setup Styles
        self.style = ttk.Style()
        self.style.configure('White.TFrame', background='white')

        # Variables for data and mode selection
        self.mode_var = tk.StringVar(value="max_need") # Default mode: Max Need
        self.allocation_matrix_entries = []
        self.secondary_matrix_entries = []
        self.available_vector_entries = []

        self.setup_initial_input()

        # Output Text Widget Setup (for step-by-step logging)
        self.log_label = ttk.Label(self.output_frame, text="Algoritma Banker's - Langkah-langkah Simulasi:", font=("Helvetica", 14, "bold"), background="white")
        self.log_label.pack(fill=tk.X, pady=(0, 10))

        self.log_text = tk.Text(self.output_frame, height=35, width=60, wrap=tk.WORD, font=("Consolas", 10), bg="#f5f5f5")
        self.log_text.pack(expand=True, fill=tk.BOTH)

    def setup_initial_input(self):
        """Creates the initial input fields for processes and resources count."""
        self.processes_label = ttk.Label(self.input_frame, text="Number of Processes (N):", background="white")
        self.processes_label.grid(row=0, column=0, sticky=tk.E, pady=5)
        self.processes_entry = RoundedEntry(self.input_frame, width=5)
        self.processes_entry.grid(row=0, column=1, padx=10, pady=5)

        self.resources_label = ttk.Label(self.input_frame, text="Number of Resources (M):", background="white")
        self.resources_label.grid(row=1, column=0, sticky=tk.E, pady=5)
        self.resources_entry = RoundedEntry(self.input_frame, width=5)
        self.resources_entry.grid(row=1, column=1, padx=10, pady=5)

        self.next_button = RoundedButton(self.input_frame, text="Next", command=self.next_step)
        self.next_button.grid(row=2, column=0, columnspan=2, pady=20)

    def next_step(self):
        """Validates N and M and proceeds to the matrix input step."""
        try:
            self.num_processes = int(self.processes_entry.get())
            self.num_resources = int(self.resources_entry.get())
            if self.num_processes <= 0 or self.num_resources <= 0:
                 messagebox.showerror("Invalid Input", "Processes and resources must be positive integers.")
                 return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for processes and resources.")
            return

        self.input_matrices()

    def input_matrices(self):
        """Creates dynamic matrix input fields and mode selection."""
        # Clear previous dynamic input section
        for widget in self.input_frame.winfo_children():
             if widget not in [self.processes_label, self.processes_entry, self.resources_label, self.resources_entry, self.next_button]:
                widget.destroy()

        # --- MODE SELECTION ---
        mode_frame = ttk.Frame(self.input_frame, padding=5, style='White.TFrame')
        mode_frame.grid(row=3, column=0, columnspan=2, pady=(10, 10), sticky="w")

        ttk.Label(mode_frame, text="Pilih Input Kedua:", background="white", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))

        rb1 = ttk.Radiobutton(mode_frame, text="Max Need Matrix", variable=self.mode_var, value="max_need", command=self.update_matrix_labels)
        rb1.pack(side=tk.LEFT, padx=5)

        rb2 = ttk.Radiobutton(mode_frame, text="Need Matrix", variable=self.mode_var, value="need", command=self.update_matrix_labels)
        rb2.pack(side=tk.LEFT, padx=5)
        # ----------------------

        # Input Allocation Matrix
        tk.Label(self.input_frame, text="Enter Allocation Matrix (Current Allocation)", font=("Helvetica", 11, "bold"), background="white").grid(row=4, column=0, columnspan=2, pady=(20, 10))
        self.allocation_matrix_entries = self.create_matrix_input(self.input_frame, self.num_processes, self.num_resources, 5)

        # Input Secondary Matrix (Max Need or Need)
        self.secondary_label = tk.Label(self.input_frame, text="Enter Max Need Matrix", font=("Helvetica", 11, "bold"), background="white")
        self.secondary_label.grid(row=self.num_processes + 5, column=0, columnspan=2, pady=(20, 10))
        self.secondary_matrix_entries = self.create_matrix_input(self.input_frame, self.num_processes, self.num_resources, self.num_processes + 6)

        # Input Available Vector
        tk.Label(self.input_frame, text="Enter Available Vector", font=("Helvetica", 11, "bold"), background="white").grid(row=(self.num_processes * 2) + 6, column=0, columnspan=2, pady=(20, 10))
        self.available_vector_entries = self.create_vector_input(self.input_frame, self.num_resources, (self.num_processes * 2) + 7)

        self.detect_button = RoundedButton(self.input_frame, text="Detect Deadlock (Banker's)", command=self.detect_deadlock)
        self.detect_button.grid(row=(self.num_processes * 2) + 8, column=0, columnspan=2, pady=20)

    def update_matrix_labels(self):
        """Updates the label for the secondary matrix based on the radio button selection."""
        if self.mode_var.get() == "max_need":
            self.secondary_label.config(text="Enter Max Need Matrix")
        else:
            self.secondary_label.config(text="Enter Need Matrix")

    def create_matrix_input(self, parent_frame, rows, cols, start_row):
        """Generates Entry widgets for a matrix."""
        matrix = []
        # Resource Labels (R1, R2, R3...)
        for j in range(cols):
            ttk.Label(parent_frame, text=f"R{j+1}", font=("Helvetica", 9), background="white").grid(row=start_row - 1, column=j+1, padx=5)

        for i in range(rows):
            row = []
            # Process Labels (P0, P1, P2...)
            ttk.Label(parent_frame, text=f"P{i}", font=("Helvetica", 9), background="white").grid(row=start_row + i, column=0, padx=5, sticky="e")
            for j in range(cols):
                entry = RoundedEntry(parent_frame, width=5)
                entry.grid(row=start_row + i, column=j+1, padx=5, pady=2)
                row.append(entry)
            matrix.append(row)
        return matrix

    def create_vector_input(self, parent_frame, size, start_row):
        """Generates Entry widgets for a vector."""
        vector = []
        # Resource Labels (R1, R2, R3...)
        for i in range(size):
            ttk.Label(parent_frame, text=f"R{i+1}", font=("Helvetica", 9), background="white").grid(row=start_row - 1, column=i+1, padx=5)

        for i in range(size):
            entry = RoundedEntry(parent_frame, width=5)
            entry.grid(row=start_row, column=i+1, padx=5, pady=2)
            vector.append(entry)
        return vector

    def get_matrix(self, matrix_entries):
        """Extracts integer values from matrix entry widgets."""
        result = []
        for row in matrix_entries:
            try:
                result.append([int(entry.get()) for entry in row])
            except ValueError:
                raise ValueError("Semua field matriks harus diisi dengan bilangan bulat (integer).")
        return result

    def get_vector(self, vector_entries):
        """Extracts integer values from vector entry widgets."""
        try:
            return [int(entry.get()) for entry in vector_entries]
        except ValueError:
            raise ValueError("Semua field vektor harus diisi dengan bilangan bulat (integer).")

    def log_message(self, message):
        """Appends a message to the log Text widget."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END) # Scroll to the bottom

    def calculate_need_matrix(self, allocation, secondary, mode):
        """Calculates the Need matrix based on the user's input mode."""

        if mode == "max_need":
            # Need = Max Need - Allocation
            need = secondary - allocation
            if np.any(need < 0):
                messagebox.showerror("Error Calculation", "Need calculation menghasilkan nilai negatif (Max Need < Allocation). Cek kembali input Anda.")
                return None
            return need

        elif mode == "need":
            # Need is the secondary matrix itself
            return secondary

    def detect_deadlock(self):
        """Main function to run the Banker's Algorithm and log the process."""
        self.log_text.delete(1.0, tk.END) # Clear previous log
        self.log_message("--- Memulai Algoritma Banker's ---")

        try:
            # 1. Get ALL inputs
            allocation = np.array(self.get_matrix(self.allocation_matrix_entries))
            secondary_matrix = np.array(self.get_matrix(self.secondary_matrix_entries))
            available = np.array(self.get_vector(self.available_vector_entries))
            mode = self.mode_var.get()

            # 2. Calculate the NEED matrix
            need = self.calculate_need_matrix(allocation, secondary_matrix, mode)
            if need is None:
                return # Error occurred during calculation

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        self.log_message(f"Mode Input: {'Max Need' if mode == 'max_need' else 'Need'}")
        self.log_message(f"Allocation Matrix:\n{allocation}")
        self.log_message(f"Need Matrix:\n{need}")
        self.log_message("-" * 30)

        # --- Banker's algorithm logic ---
        work = available.copy()
        finish = [False] * self.num_processes
        safe_sequence = []

        self.log_message(f"Initial Available (Work): {work.tolist()}")
        self.log_message("-" * 30)

        # Iterate at most N times (N=num_processes)
        for k in range(self.num_processes):
            process_found = False
            self.log_message(f"\nITERASI {k+1}: Mencari proses yang bisa dieksekusi...")

            for i in range(self.num_processes):
                if not finish[i]:
                    # Check if Need[i] <= Work
                    need_le_work = np.all(need[i] <= work)

                    self.log_message(f"  P{i}: Cek Need {need[i].tolist()} <= Work {work.tolist()} -> {need_le_work}")

                    if need_le_work:
                        # Process P_i can run and finish
                        work = work + allocation[i]
                        finish[i] = True
                        safe_sequence.append(i)
                        process_found = True

                        self.log_message(f"  ✅ P{i} selesai. Resource dikembalikan.")
                        self.log_message(f"     Work baru = {work.tolist()}")
                        break # Restart search from P0 for the next process

            if not process_found and not all(finish):
                # Cannot find any process that can execute
                self.log_message("\n--- HASIL AKHIR ---")
                self.log_message("❌ DEADLOCK TERDETEKSI!")
                self.log_message("Tidak ada proses yang tersisa yang dapat menyelesaikan eksekusinya.")
                messagebox.showerror("Result", "Deadlock Detected!")
                return

        self.log_message("\n--- HASIL AKHIR ---")
        if all(finish):
            final_sequence = [f"P{p}" for p in safe_sequence]
            self.log_message(f"✅ TIDAK ADA DEADLOCK TERDETEKSI. Sistem dalam SAFE STATE.")
            self.log_message(f"SAFE SEQUENCE (Urutan Aman): {final_sequence}")
            messagebox.showinfo("Result", f"No Deadlock Detected! Safe Sequence: {final_sequence}")
        else:
             # Should be unreachable if the deadlock detection logic is sound, but kept as a safeguard
             self.log_message("❌ DEADLOCK TERDETEKSI!")
             messagebox.showerror("Result", "Deadlock Detected!")

def main():
    root = tk.Tk()
    app = DeadlockDetection(root)
    root.mainloop()

if __name__ == "__main__":
    main()
