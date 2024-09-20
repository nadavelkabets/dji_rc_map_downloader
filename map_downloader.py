import math
from datetime import datetime
from urllib.request import urlretrieve
from sys import argv
import os
from multiprocessing import Pool
from shutil import rmtree

def usage():
    print("./map_downloader.py <north_lat> <west_long> <south_lat> <east_long>")

def latlon_to_tile(lat, lon, zoom):
    n = 2 ** zoom
    xtile = int(n * ((lon + 180) / 360))
    ytile = int(n * (1 - (math.log(math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat)))) / math.pi)) / 2)

    return xtile, ytile

def download_tile(tile_data):
    (xtile, ytile, zoom) = tile_data

    url = f"https://us.djiservice.org/styles/osm-bright/{zoom}/{xtile}/{ytile}@2x.png"    
    output = f"tile-{zoom}-{xtile}-{ytile}.png"
    print(urlretrieve(url, output))

def main():
    if len(argv) != 5:
        usage()
        exit(1)
         
    north_lat = float(argv[1])
    west_long = float(argv[2])
    south_lat = float(argv[3])
    east_long = float(argv[4])

    dirname = "tiles"
    if os.path.isdir(dirname):
         rmtree(dirname)
    os.makedirs("tiles")
    os.chdir("tiles")

    for current_zoom in range(1, 18):  # Zoom levels 1 to 17
        print(f"\nProcessing zoom level {current_zoom}")
        
        min_xtile, min_ytile = latlon_to_tile(north_lat, west_long, current_zoom)
        max_xtile, max_ytile = latlon_to_tile(south_lat, east_long, current_zoom)
        
        print(f"start x tile: {min_xtile}, start y tile: {min_ytile}")
        print(f"end x tile: {max_xtile}, end y tile: {max_ytile}")

        tiles_to_download = []
        for xtile in range(min_xtile, max_xtile + 1):
                    for ytile in range(min_ytile, max_ytile + 1):
                        tiles_to_download.append((xtile, ytile, current_zoom))

        Pool(8).map(download_tile, tiles_to_download)

    config = str([{"latitudeNorth":north_lat,"latitudeSouth":south_lat,"longitudeEast":east_long,"longitudeWest":west_long,"maxZoom":17,"minZoom":1,"name":"abc","timestamp":1726856188740}]).replace("'", '"')
    with open("config.json", "w") as f:
         f.write(str(config))

if __name__ == "__main__":
    main()