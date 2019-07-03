import glob, os
import time
import csv
from convert import kml_snr, kml_rssi, kml_corrections, kml_amps, kml_latency


# Start timer
start_time = time.time()

# Get working directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# output files
output_path = '{}/output/'.format(dir_path)

# Create directories
if not os.path.exists(output_path):
    os.makedirs(output_path)


for csv_file in glob.glob("output/*.csv"):
    print('Converting '+csv_file)
    print("Processing SNR...")
    kml_snr.generate(csv_file)
    print("Processing RSSI...")
    kml_rssi.generate(csv_file)   
    print("Processing corrections...")
    kml_corrections.generate(csv_file)
    print("Processing amps...")
    kml_amps.generate(csv_file)
    print("Processing latency...")
    kml_latency.generate(csv_file)

elapsed = time.time() - start_time
print("Completed in {0:.2f} seconds".format(elapsed))
input("Press enter to exit ;)")

# python ./backend/convert/run.py