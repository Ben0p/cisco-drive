# cisco-drive

Caterpillar Command network validation tool 
(In progress)

## Intended use

* Receive UDP correction data
* Subscribe to all-machine-position multicast group
* Pings application server
* Gets RSSI and AP from wireless client
* Records to .csv
* Converts to .kml

## Architecture

* Separated frontend and backend for future
* Backend
    * Python script to scrape data from various sources
    * Presents as a rest API json for frontend
    * Logs data to .csv aswell
    * Utilizing multiprocess
    * Using multiprocess queue for worker processes
    * Master process retreives data from queue and logs it
* Frontend
    * Intend to use Angular
    * T.B.A

See TODO