# dji_rc_map_downloader
A script to download and generate an offline map for DJI RC controller

The offline map tiles are located at:
```
<sdcard_mount_dir>/DJI_RC/Android/data/dji.go.v5/files/DJI/tiles/
```

The directory includes skippy map tiles in png format and a config.json index file

Skippy format:
https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames


Index file format:
```
[{"latitudeNorth":32.10401267811626,"latitudeSouth":32.07950018521896,"longitudeEast":34.80357594482135,"longitudeWest":34.75961490703324,"maxZoom":17,"minZoom":1,"name":"TLV north","timestamp":1714180803938}]
```

