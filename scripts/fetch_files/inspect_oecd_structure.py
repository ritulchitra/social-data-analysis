# scripts/fetch_files/inspect_oecd_structure.py
import requests
import json
from pathlib import Path

# ---- Paste the Structure API URL here if you copied it from OECD.
# If you didn't copy it, this is a reasonable generic structure URL to try:
STRUCTURE_URL = "https://sdmx.oecd.org/public/rest/dataflow/OECD.WISE.INE/DSD_TIME_USE@DF_TIME_USE/1.0?references=all"

def fetch_structure(url: str):
    print("Requesting Structure API:", url)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def print_series_dimensions(struct):
    # Some responses put dimensions under 'structure' -> 'dimensions' -> 'series'
    dims = struct.get("structure", {}).get("dimensions", {}).get("series", [])
    if not dims:
        print("No 'series' dimensions found in structure.")
        return
    print("\n== Series dimensions (high-level, e.g. country, activity, sex) ==")
    for i, d in enumerate(dims):
        name = d.get("name") or d.get("id")
        print(f"{i}. ID: {d.get('id')}, Name: {name}, sample values:")
        # print first few values only to avoid huge output
        sample = d.get("values", [])[:20]
        for v in sample:
            # show both code and label
            print("   -", v.get("id"), ":", v.get("name"))
        print("   ... total values:", len(d.get("values", [])))
    return dims

def print_observation_dimensions(struct):
    obs = struct.get("structure", {}).get("dimensions", {}).get("observation", [])
    if not obs:
        print("No 'observation' dimensions found.")
        return
    print("\n== Observation dimensions (usually time) ==")
    for i, d in enumerate(obs):
        print(f"{i}. ID: {d.get('id')}, Name: {d.get('name')}, sample values:",
              [v.get("name") for v in d.get("values", [])[:10]], "...")
    return obs

def find_activity_values(dims, keywords=("cook","food","meal")):
    # attempt to find the activity dimension and show values that match keywords
    for d in dims:
        # check values for keyword match (case-insensitive)
        matching = []
        for v in d.get("values", []):
            label = (v.get("name") or "").lower()
            if any(k in label for k in keywords):
                matching.append((v.get("id"), v.get("name")))
        if matching:
            print(f"\nPossible activity dimension: ID={d.get('id')}, Name={d.get('name')}")
            print("Matching activity entries (code : label):")
            for code, lab in matching:
                print(" -", code, ":", lab)
            # show total activities in this dimension
            print("Total activities in this dimension:", len(d.get("values", [])))
            return d  # return first found
    print("\nNo activity entries matched the keywords:", keywords)
    return None

def main():
    struct_json = fetch_structure(STRUCTURE_URL)
    # optional: pretty print top-level keys
    print("Top-level keys in returned JSON:", list(struct_json.keys()))
    dims = print_series_dimensions(struct_json)
    print_observation_dimensions(struct_json)
    if dims:
        find_activity_values(dims)

if __name__ == "__main__":
    main()
