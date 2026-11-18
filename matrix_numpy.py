"""
matrix_numpy.py
3x3 Matrix Operations GUI using NumPy
Operations: Addition, Subtraction, Multiplication, Transpose, Determinant, Inverse
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np

def get_matrix(entries):
    """Read 9 Entry widgets -> 3x3 numpy array (floats)."""
    vals = []
    for e in entries:
        try:
            vals.append(float(e.get()))
        except ValueError:
            raise ValueError("Please enter valid numeric values in all 18 fields.")
    return np.array(vals, dtype=float).reshape(3, 3)

def show_matrix(mat, out_entries, title):
    """Display a 3x3 matrix in the output entries."""
    flat = mat.flatten()
    for i in range(9):
        out_entries[i].delete(0, tk.END)
        out_entries[i].insert(0, f"{flat[i]:.4f}")
    result_title.set(title)

# ---------- Operations ----------
def op_add():
    try:
        A = get_matrix(entriesA); B = get_matrix(entriesB)
        show_matrix(A + B, entriesR, "Result: A + B")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def op_sub():
    try:
        A = get_matrix(entriesA); B = get_matrix(entriesB)
        show_matrix(A - B, entriesR, "Result: A - B")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def op_mul():
    try:
        A = get_matrix(entriesA); B = get_matrix(entriesB)
        show_matrix(A @ B, entriesR, "Result: A × B")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def op_transpose():
    try:
        A = get_matrix(entriesA)
        show_matrix(A.T, entriesR, "Result: Aᵀ")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def op_determinant():
    try:
        A = get_matrix(entriesA)
        det = np.linalg.det(A)
        result_title.set(f"det(A) = {det:.6f}")
        for e in entriesR:
            e.delete(0, tk.END); e.insert(0, "—")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def op_inverse():
    try:
        A = get_matrix(entriesA)
        inv = np.linalg.inv(A)
        show_matrix(inv, entriesR, "Result: A⁻¹")
    except np.linalg.LinAlgError:
        messagebox.showerror("Error", "Matrix is singular — inverse does not exist.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_all():
    for e in entriesA + entriesB + entriesR:
        e.delete(0, tk.END)
    result_title.set("Result")

# ---------- GUI ----------
root = tk.Tk()
root.title("3×3 Matrix Operations — NumPy Version")
root.geometry("780x420")
root.configure(bg="#f0f4f8")

def make_grid(parent, label_text, row0, col0, color):
    tk.Label(parent, text=label_text, font=("Arial", 13, "bold"),
             bg="#f0f4f8", fg=color).grid(row=row0, column=col0, columnspan=3, pady=(8, 4))
    cells = []
    for r in range(3):
        for c in range(3):
            e = tk.Entry(parent, width=8, justify="center",
                         font=("Consolas", 12), bd=2, relief="solid")
            e.grid(row=row0 + 1 + r, column=col0 + c, padx=3, pady=3)
            cells.append(e)
    return cells

entriesA = make_grid(root, "Matrix A", 0, 0, "#1e3a8a")
entriesB = make_grid(root, "Matrix B", 0, 4, "#1e3a8a")
entriesR = make_grid(root, "Result",  0, 8, "#b91c1c")

result_title = tk.StringVar(value="Result")
tk.Label(root, textvariable=result_title, font=("Arial", 12, "italic"),
         bg="#f0f4f8", fg="#b91c1c").grid(row=5, column=0, columnspan=11, pady=8)

# Buttons
btns = [
    ("A + B", op_add), ("A − B", op_sub), ("A × B", op_mul),
    ("Transpose A", op_transpose), ("det(A)", op_determinant),
    ("Inverse A", op_inverse), ("Clear", clear_all),
]
frm = tk.Frame(root, bg="#f0f4f8")
frm.grid(row=6, column=0, columnspan=11, pady=10)
for i, (txt, cmd) in enumerate(btns):
    tk.Button(frm, text=txt, command=cmd, width=12, font=("Arial", 10, "bold"),
              bg="#2563eb", fg="white", activebackground="#1d4ed8"
              ).grid(row=0, column=i, padx=4)

root.mainloop()