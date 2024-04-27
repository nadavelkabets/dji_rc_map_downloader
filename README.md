# dji_rc_map_downloader
A script to download and generate an offline map for DJI RC controller


Data:
https://data.maptiler.com/downloads
It is possible to choose specific region

Parse:
https://github.com/alfanhui/mbtilesToPngs
Read how to download in PNG format

Format:
DJI controller expects config.json in this format:
`[{"latitudeNorth":32.10401267811626,"latitudeSouth":32.07950018521896,"longitudeEast":34.80357594482135,"longitudeWest":34.75961490703324,"maxZoom":17,"minZoom":1,"name":"TLV north","timestamp":1714180803938}]`

