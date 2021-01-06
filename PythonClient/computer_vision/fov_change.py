# In settings.json first activate computer vision mode:
# https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode

import setup_path
import airsim

import pprint
import os
import tempfile

pp = pprint.PrettyPrinter(indent=4)

client = airsim.VehicleClient()
client.confirmConnection()

airsim.wait_key('Press any key to get camera parameters')

CAM_NAME = "front_center"

def printCameraInfo(camera_name):
    camera_info = client.simGetCameraInfo(camera_name)
    print(f"CameraInfo: {camera_name}")
    pp.pprint(camera_info)

printCameraInfo(CAM_NAME)

tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_cv_mode")
print ("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise

airsim.wait_key('Press any key to get images')

requests = [airsim.ImageRequest(CAM_NAME, airsim.ImageType.Scene),
           airsim.ImageRequest(CAM_NAME, airsim.ImageType.DepthVis)]

def save_images(responses, prefix = ""):
    for i, response in enumerate(responses):
        filename = os.path.join(tmp_dir, prefix + "_" + str(i))
        if response.pixels_as_float:
            print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_float), pprint.pformat(response.camera_position)))
            airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
        else:
            print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_uint8), pprint.pformat(response.camera_position)))
            airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)


responses = client.simGetImages(requests)
save_images(responses, "old_fov")

airsim.wait_key('Press any key to change FoV and get images')

client.simSetCameraFov(CAM_NAME, 120)
responses = client.simGetImages(requests)
save_images(responses, "new_fov")

printCameraInfo(CAM_NAME)
