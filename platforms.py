import json
from pathlib import Path

PLT_JSON = "plt.json"

def load_platforms():
    if not Path(PLT_JSON).exists():
        raise FileNotFoundError(f"{PLT_JSON} not found. Please provide the file.")
    with open(PLT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        platforms = []
        for p in data:
            name = p.get("name", "").strip().lower()
            platforms.append({
                "name": name,
                "url": p.get("url"),
                "validation": p.get("validation", {}),
            })
        if not platforms:
            raise Exception("No valid platforms found in plt.json.")
        return platforms

def get_platform_names(platforms):
    return [p["name"] for p in platforms]

def select_platforms(platforms, chosen_names=None):
    if not chosen_names or chosen_names == ["all"]:
        return platforms
    chosen = []
    names = [n.strip().lower() for n in chosen_names]
    for p in platforms:
        if p["name"].lower() in names:
            chosen.append(p)
    if not chosen:
        raise ValueError(f"No matching platform(s) found for: {', '.join(chosen_names)}")
    return chosen

def add_platform_cli():
    import argparse
    parser = argparse.ArgumentParser(description='IGT Toolkit')
    parser.add_argument('--add-platform', type=str, help='Platform name to add')
    parser.add_argument('--url', type=str, help='URL template, e.g., https://platform.com/{}')
    parser.add_argument('--validation', type=str, default="", help='Text that indicates user not found (optional)')
    args, extra = parser.parse_known_args()

    if args.add_platform and args.url:
        platform_entry = {
            "name": args.add_platform.strip().lower(),
            "url": args.url.strip(),
        }
        if args.validation:
            platform_entry["validation"] = {"text_absent": args.validation.strip()}
        # Load existing plt.json or init new
        if Path(PLT_JSON).exists():
            with open(PLT_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        # Check for duplicates
        for p in data:
            if p["name"] == platform_entry["name"]:
                print(f"[!] Platform '{p['name']}' already exists. Updating entry.")
                p.update(platform_entry)
                break
        else:
            data.append(platform_entry)
        with open(PLT_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[+] Platform '{args.add_platform}' added/updated successfully!")
        exit(0)
