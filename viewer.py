import json, os, zlib
from tkinter import Tk, Listbox, Label, Text, Scrollbar, END, BOTH, RIGHT, Y

OUT_DIR = "out"

def list_manifests():
    return [f for f in os.listdir(OUT_DIR) if f.endswith(".manifest.json")]

def load_manifest(path):
    with open(os.path.join(OUT_DIR, path), "r", encoding="utf-8") as f:
        return json.load(f)

def decompress_blob(blob_path):
    with open(blob_path, "rb") as f:
        return zlib.decompress(f.read())

def show_manifest(event):
    selection = event.widget.curselection()
    if not selection: return
    index = selection[0]
    filename = event.widget.get(index)
    manifest = load_manifest(filename)

    blob_path = manifest["blob_file"]
    preview.delete(1.0, END)
    preview.insert(END, f"📄 Manifest: {filename}\n")
    preview.insert(END, f"📦 Blob: {blob_path}\n")
    preview.insert(END, f"📉 Ratio: {manifest['compression_ratio']}\n")
    preview.insert(END, f"📄 Preview (from manifest):\n\n{manifest['preview_utf8']}\n\n")

    try:
        decompressed = decompress_blob(blob_path)
        text = decompressed[:500].decode("utf-8", errors="replace")
        preview.insert(END, f"🧠 Decompressed preview:\n\n{text}")
    except Exception as e:
        preview.insert(END, f"❌ Error decompressing blob:\n{e}")

def run_viewer():
    root = Tk()
    root.title("🧠 BlackBox Vault Viewer")

    Label(root, text="📁 Vault Entries").pack()
    listbox = Listbox(root, height=10)
    listbox.pack(fill=BOTH, expand=False)
    listbox.bind("<<ListboxSelect>>", show_manifest)

    for f in list_manifests():
        listbox.insert(END, f)

    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

    global preview
    preview = Text(root, height=20, yscrollcommand=scrollbar.set)
    preview.pack(fill=BOTH, expand=True)
    scrollbar.config(command=preview.yview)

    root.mainloop()

if __name__ == "__main__":
    run_viewer()
def update_index(manifest: dict, index_path: str = "out/index.json"):
    index = []
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            try:
                index = json.load(f)
            except:
                index = []

    index.append({
        "created_at": manifest["created_at"],
        "input_file": manifest["input_file"],
        "blob_file": manifest["blob_file"],
        "manifest_file": manifest["blob_file"].replace(".bbx", ".manifest.json"),
        "codec": manifest["codec"],
        "compression_ratio": manifest["compression_ratio"]
    })

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
