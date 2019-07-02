import os


'''
Mine Systems cisco drive csv to kml converter
Input a formatted .csv of the cisco-drive results
Generates a .kml
'''


def generate(csv_in):
    '''
    Generate a .kml from a formatted .csv
    csv_in is the input formatted .csv
    '''

    # Header of .kml
    header = (
        '<?xml version="1.0" encoding="utf-8" ?>'
        '<kml xmlns="http://www.opengis.net/kml/2.2">'
        '   <Document id="root_doc">'
    )

    # Ledgend of the colors for each throughput result
    ledgend = (
        '       <Folder><name>Legend - Time since correction</name>'
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:#53ff00;&quot;&gt;&lt;b&gt;Less than 1sec&lt;/b&gt;&lt;/span&gt;</name>'
        '           </Placemark>'
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:#f2ff03;&quot;&gt;&lt;b&gt;2sec&lt;/b&gt;&lt;/span&gt;</name>'
        '           </Placemark>'
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:#ffbc03;&quot;&gt;&lt;b&gt;3sec&lt;/b&gt;&lt;/span&gt;</name>'
        '           </Placemark>'
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:#ff8103;&quot;&gt;&lt;b&gt;4sec&lt;/b&gt;&lt;/span&gt;</name>'
        '           </Placemark>'
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:#ff3e03;&quot;&gt;&lt;b&gt;Greater than 4sec&lt;/b&gt;&lt;/span&gt;</name>'
        '           </Placemark>'
        '       </Folder>'
    )
    
    # Name for the drive results folder
    name = (
        '       <Folder><name>Track - {}</name>'
    )

    # Placemark for each segment of the results
    placemark = (
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:{c}&quot;&gt;{r}: {rssi} sec&lt;/span&gt;</name>'
        '               <Style><LineStyle><color>{lc}</color><width>4</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style>'
        '               <LineString><coordinates>{lon1},{lat1} {lon2},{lat2}</coordinates></LineString>'
        '           </Placemark>'
    )

    # Closing out the .kml
    footer = (
        '       </Folder>'
        '   </Document>'
        '  </kml>'
    )

    # Colors for throughputs
    color = {
        '4':'#ff3e03',
        '3':'#ff8103',
        '2':'#ffbc03',
        '1':'#f2ff03',
        '0':'#53ff00'
        }

    # Colors for the segments
    line_color = {
        '4':'ff033eff',
        '3':'ff0381ff',
        '2':'ff03bcff',
        '1':'ff03fff2',
        '0':'ff00ff53'
        }


    # Get the filename only from absolute directory?
    csv_filename = os.path.basename(csv_in)
    # Get the filename without extension
    drive_name = os.path.splitext(csv_filename)[0]
    # Add .kml extension to the drive_name
    kml_name = drive_name+'-corrections.kml'

    # Start point counter
    count = 0

    # Create .kml file
    with open(kml_name, 'w') as kml:
        # Write the header and ledgend to file
        kml.write(header)
        kml.write(ledgend)
        # Set the name inside kml
        name = name.format(drive_name)
        kml.write(name)

        # Open csv file for read only
        with open(csv_in,'r') as f:
            # Read each line
            for row in f:
                # Split line with comma deliminator
                cell = row.split(',')
                
                # Skip the first line in csv containing header info
                if count == 0:
                    count += 1
                    continue

                # Generate start of first segment from first point
                if count == 1:
                    if cell[6] and cell[7]:
                        lat2 = cell[6]
                        lon2 = cell[7]
                        total_corrections2 = float(cell[26])
                        tstamp2 = float(cell[0])
                        count_since_correction = 0
                    else:
                        continue
                # From second point onwards, start of segment is the end of last segment
                else:
                    lat2 = lat1
                    lon2 = lon1
                    total_corrections2 = total_corrections1
                    tstamp2 = tstamp1
                # Second point of segment
                if cell[6] and cell[7]:
                    lat1 = cell[6]
                    lon1 = cell[7]
                else:
                    continue
                
                # Convert corrections
                if cell[26]:
                    total_corrections1 = float(cell[26])
                    tstamp1 = float(cell[0])

                    # Difference in correction count
                    correction_increment = total_corrections1 - total_corrections2


                    # Time since last correction
                    if correction_increment == 0 and count_since_correction == 0:
                        # Last correction time
                        last_correction_time = tstamp2
                        count_since_correction += 1
                    elif correction_increment == 0 and count_since_correction >= 1:
                        count_since_correction += 1
                    elif correction_increment >= 1:
                        # Time since correction
                        last_correction_time = tstamp1

                    tsc = tstamp1 - last_correction_time

                else:
                    tsc = 999
                
                # Set segment colors based on rssi
                if tsc < 1:
                    rc = color['0']
                    lc = line_color['0']
                elif 1 <= tsc < 2:
                    rc = color['1']
                    lc = line_color['1']
                elif 2 <= tsc < 3:
                    rc = color['2']
                    lc = line_color['2']
                elif 3 <= tsc < 4:
                    rc = color['3']
                    lc = line_color['3']
                elif 4 <= tsc:
                    rc = color['4']
                    lc = line_color['4']
                elif tsc == 999:
                    rc = '#ffffff'
                    lc = '#ffffffff'
                

                # Insert values into the kml segment
                track = placemark.format(
                    c=rc,
                    r=count,
                    rssi=tsc,
                    lon1=lon1,
                    lat1=lat1,
                    lon2=lon2,
                    lat2=lat2,
                    lc=lc
                    )

                # Write segment to file      
                kml.write(track)
                # Increase count
                count += 1
            # Print total points
            print("Processed {} points".format(count))
            # Close csv file
            f.close
        # Write out the footer to kml
        kml.write(footer)
        # Close the kml
        kml.close



if __name__ == '__main__':
    csv_file = '20180914-CTO-BRA.csv'
    generate(csv_file)
