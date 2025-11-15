import os
import zlib
import json
import time
import sys

def read_text(path):
    with open(path, "rb") as f:
        return f.read()

def compress_bytes(data: bytes, level: int = 9) -> bytes:
    return zlib.compress(data, level)

def write_blackbox(input_path: str, out_dir: str = "out"):
    os.makedirs(out_dir, exist_ok=True)

    raw = read_text(input_path)
    compressed = compress_bytes(raw, level=9)

    ts = int(time.time())
    base = os.path.splitext(os.path.basename(input_path))[0]
    blob_name = f"{base}.{ts}.bbx"
    manifest_name = f"{base}.{ts}.manifest.json"

    blob_path = os.path.join(out_dir, blob_name)
    manifest_path = os.path.join(out_dir, manifest_name)

    # Write binary blob
    with open(blob_path, "wb") as bf:
        bf.write(compressed)

    manifest = {
        "version": 1,
        "created_at": ts,
        "input_file": os.path.abspath(input_path),
        "blob_file": os.path.abspath(blob_path),
        "codec": "zlib",
        "original_bytes": len(raw),
        "compressed_bytes": len(compressed),
        "compression_ratio": round(len(compressed) / max(len(raw), 1), 4),
        "preview_utf8": raw[:200].decode("utf-8", errors="replace")
    }

    with open(manifest_path, "w", encoding="utf-8") as mf:
        json.dump(manifest, mf, ensure_ascii=False, indent=2)

    print(f"✅ BlackBox created:")
    print(f"- Blob: {blob_path}")
    print(f"- Manifest: {manifest_path}")
    print(f"- Ratio: {manifest['compression_ratio']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python enhanced\\ingest_text.py <path-to-text-file>")
        sys.exit(1)
    write_blackbox(sys.argv[1])
