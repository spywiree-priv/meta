import hashlib, zipfile, tarfile, os


def make_zip(path: str, src: str, dst: str):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as f:
        f.write(src, dst)


def make_targz(path: str, src: str, dst: str):
    with tarfile.open(path, "w:gz") as f:
        f.add(src, dst)


def hash_file(path: str):
    with open(path, "rb", buffering=0) as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def main():
    for file in os.listdir("build"):
        is_exe = file.endswith(".exe")

        src = os.path.join("build", file)
        dst = file.split("-")[0]
        if is_exe:
            dst += ".exe"

        arcpath = os.path.join("build", file.removesuffix(".exe"))
        if not is_exe:
            arcpath += ".tar.gz"
            make_targz(arcpath, src, dst)
        else:
            arcpath += ".zip"
            make_zip(arcpath, src, dst)

        os.remove(src)

        with open(arcpath + ".sha256", mode="w", encoding="utf-8") as f:
            f.write(hash_file(arcpath) + "\n")


if __name__ == "__main__":
    main()
