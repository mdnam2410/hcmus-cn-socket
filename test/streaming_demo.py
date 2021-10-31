from app.client.packages.portal import Portal
import app.core.protocol as protocol

import cv2
import numpy as np
from PIL import Image

if __name__ == '__main__':
    # Create the portal and connect to the server
    portal = Portal()
    portal.connect('127.0.0.1', protocol.SERVER_PORT)

    # Start by initialize the stream service
    response, stream = portal.initialize_screen_stream()
    # Stream is None if the initialization fails
    if stream is None:
        print('Stream fails')

    # Loop in the stream to retrieve the frames
    for width, height, frame in stream:
        # width, height is the size of the frame
        print(width, height)
        # frame is a raw array of bytes of image (RGBA mode)
        print(frame)
        
        # Load the frame by any library
        # For example, use PIL.Image
        image = Image(mode='RGBA', size=(width, height), data=frame)

        # Display the image using any library
        # For example, cv2 and numpy
        cv2.imshow(winname='Stream', mat=np.array(image))

    # The above for loop is controlled by these functions
    # Start the stream
    portal.start_stream()

    # Pause the stream
    portal.pause_stream()

    # Restart the stream
    portal.restart_stream()

    # Stop the stream
    portal.stop_stream()
