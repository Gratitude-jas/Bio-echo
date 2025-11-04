# debug_null_bytes.py

file_path = "app/main.py"

# Step 1: Check for null bytes
with open(file_path, "rb") as f:
    content = f.read()
    has_nulls = b"\x00" in content
    print("Null bytes found:", has_nulls)

# Step 2: If found, strip them out
if has_nulls:
    clean = content.replace(b"\x00", b"")
    with open(file_path, "wb") as f:
        f.write(clean)
    print("Null bytes removed.")
else:
    print("File is already clean.")

# debug_model_file.py

file_path = "models/rf_model.pkl"

with open(file_path, "rb") as f:
    content = f.read()
    has_nulls = b"\x00" in content
    print("Null bytes found in model file:", has_nulls)