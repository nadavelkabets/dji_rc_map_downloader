import argparse
import json
import math
import os
from datetime import datetime
from multiprocessing import Pool
from shutil import rmtree
from urllib.request import urlretrieve

def latlon_to_tile(lat, lon, zoom):
    n = 2 ** zoom
    xtile = int(n * ((lon + 180) / 360))
    ytile = int(n * (1 - (math.log(math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat)))) / math.pi)) / 2)

    return xtile, ytile

def download_tile(tile_data):
    (xtile, ytile, zoom) = tile_data

    url = f"https://us.djiservice.org/styles/osm-bright/{zoom}/{xtile}/{ytile}@2x.png"
    output = f"tile-{zoom}-{xtile}-{ytile}.png"
    try:
        result = urlretrieve(url, output)
        print(f"Downloaded: {output}")
        return (True, output)
    except Exception as e:
        print(f"Failed to download {output}: {e}")
        return (False, output)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Download offline map tiles for DJI RC controller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  %(prog)s --north 32.10 --south 32.07 --west 34.76 --east 34.80
  %(prog)s -n 32.10 -s 32.07 -w 34.76 -e 34.80 --name "Tel Aviv" --workers 4

The downloaded tiles will be saved in the 'tiles' directory along with a
config.json file. Copy this directory to your DJI RC SD card at:
  <sdcard>/DJI_RC/Android/data/dji.go.v5/files/DJI/tiles/
        """
    )
    parser.add_argument("-n", "--north", type=float, required=True,
                        help="Northern latitude of bounding box (e.g., 32.10)")
    parser.add_argument("-s", "--south", type=float, required=True,
                        help="Southern latitude of bounding box (e.g., 32.07)")
    parser.add_argument("-w", "--west", type=float, required=True,
                        help="Western longitude of bounding box (e.g., 34.76)")
    parser.add_argument("-e", "--east", type=float, required=True,
                        help="Eastern longitude of bounding box (e.g., 34.80)")
    parser.add_argument("--name", type=str, default="offline_map",
                        help="Name for the map region (default: offline_map)")
    parser.add_argument("--min-zoom", type=int, default=1,
                        help="Minimum zoom level (default: 1)")
    parser.add_argument("--max-zoom", type=int, default=17,
                        help="Maximum zoom level (default: 17)")
    parser.add_argument("--workers", type=int, default=8,
                        help="Number of parallel download workers (default: 8)")
    parser.add_argument("-o", "--output", type=str, default="tiles",
                        help="Output directory for tiles (default: tiles)")
    return parser.parse_args()


def main():
    args = parse_args()

    north_lat = args.north
    south_lat = args.south
    west_long = args.west
    east_long = args.east

    dirname = args.output
    if os.path.isdir(dirname):
        rmtree(dirname)
    os.makedirs(dirname)
    os.chdir(dirname)

    for current_zoom in range(args.min_zoom, args.max_zoom + 1):
        print(f"\nProcessing zoom level {current_zoom}")
        
        min_xtile, min_ytile = latlon_to_tile(north_lat, west_long, current_zoom)
        max_xtile, max_ytile = latlon_to_tile(south_lat, east_long, current_zoom)
        
        print(f"start x tile: {min_xtile}, start y tile: {min_ytile}")
        print(f"end x tile: {max_xtile}, end y tile: {max_ytile}")

        tiles_to_download = []
        for xtile in range(min_xtile, max_xtile + 1):
            for ytile in range(min_ytile, max_ytile + 1):
                tiles_to_download.append((xtile, ytile, current_zoom))

        print(f"Downloading {len(tiles_to_download)} tiles for zoom level {current_zoom}")
        with Pool(args.workers) as pool:
            results = pool.map(download_tile, tiles_to_download)

        successful = sum(1 for success, _ in results if success)
        print(f"Completed zoom level {current_zoom}: {successful}/{len(tiles_to_download)} tiles downloaded")

    timestamp = int(datetime.now().timestamp() * 1000)
    config = [{
        "latitudeNorth": north_lat,
        "latitudeSouth": south_lat,
        "longitudeEast": east_long,
        "longitudeWest": west_long,
        "maxZoom": args.max_zoom,
        "minZoom": args.min_zoom,
        "name": args.name,
        "timestamp": timestamp
    }]
    with open("config.json", "w") as f:
        json.dump(config, f)

    print(f"\nDownload complete! Tiles saved to '{dirname}/'")
    print(f"Copy the '{dirname}' directory to your DJI RC SD card at:")
    print("  <sdcard>/DJI_RC/Android/data/dji.go.v5/files/DJI/tiles/")

if __name__ == "__main__":
    main()