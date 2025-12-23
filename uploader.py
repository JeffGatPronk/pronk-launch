import sys
from urllib.parse import urlparse, parse_qs
from tkinter import Tk, filedialog, messagebox

def main():
    if len(sys.argv) < 2:
        messagebox.showerror("Pronk Uploader", "No Work Order provided.")
        return

    url = sys.argv[1]
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    workorder = qs.get("wo", [""])[0]

    if not workorder:
        messagebox.showerror("Pronk Uploader", "Invalid Work Order ID.")
        return

    root = Tk()
    root.withdraw()

    pdf = filedialog.askopenfilename(
        title=f"Select PDF for Work Order {workorder}",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not pdf:
        return

    messagebox.showinfo(
        "Pronk Uploader",
        f"Selected:\n{pdf}\n\nWork Order:\n{workorder}"
    )

    # Placeholder for future:
    # upload_to_tms(pdf, workorder)

if __name__ == "__main__":
    main()
