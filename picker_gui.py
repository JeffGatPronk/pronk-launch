import sys
from tkinter import Tk, filedialog, messagebox

def main():
    workorder = sys.argv[1] if len(sys.argv) > 1 else "UNKNOWN"

    root = Tk()
    root.withdraw()
    pdf = filedialog.askopenfilename(
        title=f"Select PDF for Work Order {workorder}",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if pdf:
        messagebox.showinfo("Pronk Uploader", f"Selected:\n{pdf}\nWork Order: {workorder}")
    root.destroy()

if __name__ == "__main__":
    main()
