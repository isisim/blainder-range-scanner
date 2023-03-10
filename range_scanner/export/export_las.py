import laspy
import numpy as np
import os

def export(filePath, fileName, data, exportNoiseData):
    print("Exporting data into .las format...")

    # create header 
    # see https://laspy.readthedocs.io/en/latest/tut_background.html for info on point formats
    header = laspy.LasHeader(version="1.4",point_format=8)

    # create output file path
    outfile = laspy.LasData(header=header)
    
    # assign data
    outfile.pt_src_id = data[1]

    allX = data[2]
    allY = data[3]
    allZ = data[4]

    # generate some additional information
    xmin = np.floor(np.min(allX))
    ymin = np.floor(np.min(allY))
    zmin = np.floor(np.min(allZ))

    outfile.header.offset = [xmin,ymin,zmin]
    scaleFactor = 0.0001
    outfile.header.scale = [scaleFactor, scaleFactor, scaleFactor]

    # Define the new attribute using the add_extra_dim() method
    outfile.add_extra_dim(laspy.ExtraBytesParams(name="label", type=np.long, description="Class labeling"))
    outfile.add_extra_dim(laspy.ExtraBytesParams(name="instance", type=np.long, description="Object instancing"))

    print(data[0])
    print(data[1])

    # Add the new attribute to the LAS file
    outfile.label = data[0]
    outfile.instance = data[1]

    outfile.x = allX
    outfile.y = allY
    outfile.z = allZ

    # for scaling factors see: https://www.asprs.org/wp-content/uploads/2010/12/LAS_1_4_r13.pdf
    outfile.intensity = data[6] * 65535

    outfile.red = data[7] * 65535
    outfile.green = data[8] * 65535
    outfile.blue = data[9] * 65535

    outfile.write(os.path.join(filePath, "%s_parts.las" % fileName))

    
    if exportNoiseData:
        # create output file path
        outfile = laspy.LasData(header=header)
        
        # assign data
        outfile.pt_src_id = data[1]

        allX = data[10]
        allY = data[11]
        allZ = data[12]

        # generate some additional information
        xmin = np.floor(np.min(allX))
        ymin = np.floor(np.min(allY))
        zmin = np.floor(np.min(allZ))

        outfile.header.offset = [xmin,ymin,zmin]
        outfile.header.scale = [0.001,0.001,0.001]

        outfile.x = allX
        outfile.y = allY
        outfile.z = allZ

        outfile.intensity = data[6] * 65535

        outfile.red = data[7] * 65535
        outfile.green = data[8] * 65535
        outfile.blue = data[9] * 65535

        outfile.write(os.path.join(filePath, "%s_noise_parts.las" % fileName))

        
    print("Done.")
