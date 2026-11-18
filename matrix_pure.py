"""
matrix_pure.py
3x3 Matrix Operations GUI using pure Python (no external libraries)
Operations: Addition, Subtraction, Multiplication, Transpose, Determinant, Inverse
"""

import tkinter as tk
from tkinter import messagebox

def get_matrix(entries):
    """Read 9 Entry widgets -> 3x3 list of lists (floats)."""
    vals = []
    for e in entries:
        try:
            vals.append(float(e.get()))
        except ValueError:
            raise ValueError("Please enter valid numeric values in all 18 fields.")
    return [vals[0:3], vals[3:6], vals[6:9]]

def show_matrix(mat, out_entries, title):
    """Display 3x3 matrix (list of lists) in output entries."""
    k = 0
    for r in range(3):
        for c in range(3):
            out_entries[k].delete(0, tk.END)
            out_entries[k].insert(0, f"{mat[r][c]:.4f}")
            k += 1
    result_title.set(title)

# ---------- Pure-Python matrix helpers ----------
def m_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(3)] for i in range(3)]

def m_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(3)] for i in range(3)]

def m_mul(A, B):
    C = [[0.0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            C[i][j] = sum(A[i][k]*B[k][j] for k in range(3))
    return C

def m_transpose(A):
    return [[A[j][i] for j in range(3)] for i in range(3)]

def m_det(A):
    return (A[0][0]*(A[1][1]*A[2][2] - A[1][2]*A[2][1])
          - A[0][1]*(A[1][0]*A[2][2] - A[1][2]*A[2][0])
          + A[0][2]*(A[1][0]*A[2][1] - A[1][1]*A[2][0]))

def m_inverse(A):
    d = m_det(A)
    if abs(d) < 1e-12:
        raise ZeroDivisionError("Matrix is singular — inverse does not exist.")
    # Cofactor matrix
    cof = [[0.0]*3 for _ in range(3)]
    cof[0][0] =  (A[1][1]*A[2][2] - A[1][2]*A[2][1])
    cof[0][1] = -(A[1][0]*A[2][2] - A[1][2]*A[2][0])
    cof[0][2] =  (A[1][0]*A[2][1] - A[1][1]*A[2][0])
    cof[1][0] = -(A[0][1]*A[2][2] - A[0][2]*A[2][1])
    cof[1][1] =  (A[0][0]*A[2][2] - A[0][2]*A[2][0])
    cof[1][2] = -(A[0][0]*A[2][1] - A[0][1]*A[2][0])
    cof[2][0] =  (A[0][1]*A[1][2] - A[0][2]*A[1][1])
    cof[2][1] = -(A[0][0]*A[1][2] - A[0][2]*A[1][0])
    cof[2][2] =  (A[0][0]*A[1][1] - A[0][1]*A[1][0])
    # Adjugate = transpose(cofactor)
    adj = m_transpose(cof)
    # Inverse = adj / det
    return [[adj[i][j]/d for j in range(3)] for i in range(3)]

# ---------- Button handlers ----------
def op_add():
    try:
        show_matrix(m_add(get_matrix(entriesA), get_matrix(entriesB)), entriesR, "Result: A + B")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def op_sub():
    try:
        show_matrix(m_sub(get_matrix(entriesA), get_matrix(entriesB)), entriesR, "Result: A - B")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def op_mul():
    try:
        show_matrix(m_mul(get_matrix(entriesA), get_matrix(entriesB)), entriesR, "Result: A × B")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def op_transpose():
    try:
        show_matrix(m_transpose(get_matrix(entriesA)), entriesR, "Result: Aᵀ")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def op_determinant():
    try:
        det = m_det(get_matrix(entriesA))
        result_title.set(f"det(A) = {det:.6f}")
        for e in entriesR:
            e.delete(0, tk.END); e.insert(0, "—")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def op_inverse():
    try:
        show_matrix(m_inverse(get_matrix(entriesA)), entriesR, "Result: A⁻¹")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_all():
    for e in entriesA + entriesB + entriesR:
        e.delete(0, tk.END)
    result_title.set("Result")

# ---------- GUI (identical layout) ----------
root = tk.Tk()
root.title("3×3 Matrix Operations — Pure Python Version")
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

btns = [
    ("A + B", op_add), ("A − B", op_sub), ("A × B", op_mul),
    ("Transpose A", op_transpose), ("det(A)", op_determinant),
    ("Inverse A", op_inverse), ("Clear", clear_all),
]
frm = tk.Frame(root, bg="#f0f4f8")
frm.grid(row=6, column=0, columnspan=11, pady=10)
for i, (txt, cmd) in enumerate(btns):
    tk.Button(frm, text=txt, command=cmd, width=12, font=("Arial", 10, "bold"),
              bg="#16a34a", fg="white", activebackground="#15803d"
              ).grid(row=0, column=i, padx=4)

root.mainloop()