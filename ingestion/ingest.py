import os
import requests
from datetime import datetime

# BASE_URL ="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-02.parquet"
BASE_URL ="https://d37ci6vzurychx.cloudfront.net/trip-data"
START_YEAR = 2025
END_YEAR = 2025
OUTPUT_DIR = 'data'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# YELLOW_URL = "yellow_tripdata_{year}-{part}.parquet"

def generate_month(year):
    return [f'{year}-{month:02d}' for month in range(1, 13)]

def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True, timeout=30)

        content_type = response.headers.get("Content-Type", "")
        
        if response.status_code == 200 and "octet-stream" in content_type:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            if os.path.getsize(save_path) < 1000:
                print(f"Corrupted (too small): {url}")
                os.remove(save_path)
            else:
                print(f"Downloaded: {save_path}")

        else:
            print(f"Invalid response: {url} | type={content_type}")

    except Exception as e:
        print(f"Error downloading {url}: {e}")


def main():
    for year in range(START_YEAR, END_YEAR+1):
        months = generate_month(year)
        
        for month in months:
            file_name = f'yellow_tripdata_{month}.parquet' 
            url = f'{BASE_URL}/{file_name}'
            save_path = os.path.join(OUTPUT_DIR, file_name)
            
            if not os.path.exists(save_path):
                print('downloading')
                download_file(url, save_path)

if __name__ == "__main__":
    main()
