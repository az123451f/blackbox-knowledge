import os, json, time, sys
import hashlib, zlib

def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()

def compress(data: bytes, level=9) -> bytes:
    return zlib.compress(data, level)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def ingest(path, out_dir="out"):
    os.makedirs(out_dir, exist_ok=True)
    raw = read_bytes(path)
    compressed = compress(raw)

    ts = int(time.time())
    base = os.path.splitext(os.path.basename(path))[0]
    blob = f"{base}.{ts}.bbx"
    manifest = f"{base}.{ts}.manifest.json"

    blob_path = os.path.join(out_dir, blob)
    manifest_path = os.path.join(out_dir, manifest)

    with open(blob_path, "wb") as f:
        f.write(compressed)

    meta = {
        "version": 1,
        "created_at": ts,
        "input_file": os.path.abspath(path),
        "blob_file": os.path.abspath(blob_path),
        "manifest_file": os.path.abspath(manifest_path),
        "codec": "zlib",
        "original_bytes": len(raw),
        "compressed_bytes": len(compressed),
        "compression_ratio": round(len(compressed) / max(len(raw), 1), 4),
        "sha256_raw": sha256(raw),
        "sha256_blob": sha256(compressed),
        "preview_utf8": raw[:200].decode("utf-8", errors="replace")
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    update_index(meta, os.path.join(out_dir, "index.json"))
    print(f"✅ Ingested: {path}")

def update_index(entry, index_path):
    index = []
    if os.path.exists(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                index = json.load(f)
        except:
            index = []
    index.append(entry)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python enhanced/ingest.py <file>")
        sys.exit(1)
    ingest(sys.argv[1])
