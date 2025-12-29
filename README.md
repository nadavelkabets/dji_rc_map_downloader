# DJI RC Map Downloader

A Python script to download and generate offline map tiles for DJI RC controllers.

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Usage

```bash
python map_downloader.py -n NORTH -s SOUTH -w WEST -e EAST [OPTIONS]
```

### Required Arguments

| Argument | Description |
|----------|-------------|
| `-n, --north` | Northern latitude of bounding box |
| `-s, --south` | Southern latitude of bounding box |
| `-w, --west` | Western longitude of bounding box |
| `-e, --east` | Eastern longitude of bounding box |

### Optional Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--name` | `offline_map` | Name for the map region |
| `--min-zoom` | `1` | Minimum zoom level |
| `--max-zoom` | `17` | Maximum zoom level |
| `--workers` | `8` | Number of parallel download workers |
| `-o, --output` | `tiles` | Output directory for tiles |

### Examples

Download map tiles for a small area:
```bash
python map_downloader.py -n 32.10 -s 32.07 -w 34.76 -e 34.80
```

Download with custom name and fewer workers:
```bash
python map_downloader.py -n 32.10 -s 32.07 -w 34.76 -e 34.80 --name "Tel Aviv" --workers 4
```

Download only zoom levels 10-15:
```bash
python map_downloader.py -n 32.10 -s 32.07 -w 34.76 -e 34.80 --min-zoom 10 --max-zoom 15
```

## Installation on DJI RC

1. Run the script to download tiles for your desired area
2. Connect your DJI RC controller to your computer via USB
3. Copy the `tiles` directory (or your custom output directory) to:
   ```
   <sdcard>/DJI_RC/Android/data/dji.go.v5/files/DJI/tiles/
   ```
4. The offline map will be available in your DJI app

## Output Format

The script generates:
- **Map tiles**: PNG images in [Slippy map](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames) format (`tile-{zoom}-{x}-{y}.png`)
- **config.json**: Index file required by the DJI app

Example `config.json`:
```json
[{
  "latitudeNorth": 32.10,
  "latitudeSouth": 32.07,
  "longitudeEast": 34.80,
  "longitudeWest": 34.76,
  "maxZoom": 17,
  "minZoom": 1,
  "name": "Tel Aviv",
  "timestamp": 1714180803938
}]
```

## Notes

- Higher zoom levels generate exponentially more tiles. A small area at zoom 17 can have thousands of tiles.
- The script uses multiprocessing for faster downloads. Adjust `--workers` based on your connection.
- Existing output directory will be deleted before downloading.
