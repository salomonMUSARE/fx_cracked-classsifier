import os
import shutil
import time
import re

# Configuration
EXT_PHASE1 = ['.ex4', '.ex5']
EXT_PHASE2 = ['.zip', '.rar']
UNI_DIR = 'uni'
DUP_DIR = 'dup'


def ensure_dirs():
    for d in (UNI_DIR, DUP_DIR):
        if not os.path.isdir(d):
            os.makedirs(d)


def normalize_name(filename):
    base = os.path.splitext(filename)[0]
    # strip trailing ' (' and beyond
    norm = re.sub(r"\s*\(.*$", '', base)
    return norm + os.path.splitext(filename)[1]


def group_files(files, size_sensitive=True):
    groups = {}
    for f in files:
        name = normalize_name(f)
        key = (name, os.path.getsize(f) if size_sensitive else None)
        groups.setdefault(key, []).append(f)
    # sort each group alphabetically
    for key in groups:
        groups[key].sort()
    return groups


def process_phase(extensions, size_sensitive):
    all_files = sorted([
        f for f in os.listdir('.')
        if os.path.isfile(f) and os.path.splitext(f)[1].lower() in extensions
    ])
    groups = group_files(all_files, size_sensitive)
    count_uni = count_dup = 0

    for (name, _), members in groups.items():
        # check if uni already has a file with normalized name
        uni_members = [u for u in os.listdir(UNI_DIR) if normalize_name(u) == name]
        if uni_members:
            # move all to dup
            for f in members:
                shutil.move(f, os.path.join(DUP_DIR, f))
                count_dup += 1
        else:
            # move first to uni, rest to dup
            first, *rest = members
            shutil.move(first, os.path.join(UNI_DIR, first))
            count_uni += 1
            for f in rest:
                shutil.move(f, os.path.join(DUP_DIR, f))
                count_dup += 1

    return count_uni, count_dup


def main():
    ensure_dirs()

    # Phase 1: .ex4 & .ex5
    uni1, dup1 = process_phase(EXT_PHASE1, size_sensitive=True)
    print(f"Done sorting all {', '.join(EXT_PHASE1)} files.")
    print(f"Phase 1: {uni1} files moved to {UNI_DIR}, {dup1} files moved to {DUP_DIR}.")
    time.sleep(5)

    # Phase 2: .zip & .rar
    uni2, dup2 = process_phase(EXT_PHASE2, size_sensitive=False)
    print(f"Done sorting all {', '.join(EXT_PHASE2)} files.")
    print(f"Phase 2: {uni2} files moved to {UNI_DIR}, {dup2} files moved to {DUP_DIR}.")

    # After completion, pause and create names.txt
    time.sleep(5)
    names_path = os.path.join('.', 'names.txt')
    with open(names_path, 'w') as f:
        for fname in sorted(os.listdir(UNI_DIR)):
            f.write(fname + '\n')
    print(f"names.txt created with {len(os.listdir(UNI_DIR))} entries.")


if __name__ == '__main__':
    main()
