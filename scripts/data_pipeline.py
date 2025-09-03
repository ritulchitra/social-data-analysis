from fetch_data import fetch_data
from backup_raw_data import backup_raw_data
from transform_data import transform_data
from save_clean_data import save_clean_data

def main():
    data = fetch_data()
    backup_raw_data(data)
    cleaned_data = transform_data(data)
    save_clean_data(cleaned_data)

if __name__ == "__main__":
    main()
