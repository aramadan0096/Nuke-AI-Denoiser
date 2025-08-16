import os
import subprocess
import nuke

fristFrame = int(nuke.Root()['first_frame'].value())
lastFrame = int(nuke.Root()['last_frame'].value())
frameRange = str(fristFrame) + '-' + str(lastFrame)
ret = nuke.getFramesAndViews('Frame range', frameRange)
range = ret[0]
range = range.split('-')
fristRenderFrame = int(range[0])
lastRenderFrame = int(range[1])
print('first frame is: ' + str(fristRenderFrame))
print('last frame is: ' + str(lastRenderFrame))

node = nuke.thisNode()
search_path = node['out'].value()
print(search_path)
rgb_path = os.path.join(search_path, 'rgb')
normal_path = os.path.join(search_path, 'normals')
albedo_path = os.path.join(search_path, 'albedo')
motionvector_path = os.path.join(search_path, 'motionvector')
output_dir = os.path.join(search_path, 'denoised')

print('search_path is: ' + search_path)
print('normal_path is: ' + normal_path)
print('albedo_path is: ' + albedo_path)
print('motionvector_path is: ' + motionvector_path)
print('output_dir is: ' + output_dir)

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

repeat = int(node['repeat'].value())
blend_amount = str(node['blend'].value())
use_hdr = str(int(node['hdr'].value()))
# Read knob value safely (avoid passing a Knob/None into subprocess)
pre_knob = node.knob('preDenoised_path')
preDenoised_path = pre_knob.value() if pre_knob else ''
path_to_denoiser = r'D:\tools\Optix\denoisr_bin9'
output_prefix = 'denoised_'
denoiser_exe = os.path.join(path_to_denoiser, 'Denoiser.exe')

print('repeat is: ' + str(repeat))
print('blend_amount is: ' + blend_amount)
print('use_hdr is: ' + use_hdr)

# Basic sanity check for the denoiser binary
if not os.path.isfile(denoiser_exe):
    nuke.message('Denoiser not found: {}'.format(denoiser_exe))
    raise RuntimeError('Missing denoiser exe at {}'.format(denoiser_exe))

file_extension = 'exr'
writeNodes = ['Write_Beauty','Write_Albedo','Write_Normals','Write_Motionvector']
writeList = []
with nuke.toNode(node.name()):
    for n in nuke.allNodes():
        if n.name() in writeNodes:
            writeList.append(n)

    nuke.executeMultiple(writeList, ((fristRenderFrame, lastRenderFrame, 1), (fristRenderFrame, lastRenderFrame, 1), (fristRenderFrame, lastRenderFrame, 1), (fristRenderFrame, lastRenderFrame, 1)))


##########
# DENOISE
##########

for root, _, files in os.walk(search_path):
    if os.path.basename(root) != 'rgb':
        continue  # Only process the RGB directory

    for file in files:
        if file.startswith('rgb.') and file.endswith('.exr'):
            # Input RGB file
            input_file = os.path.join(root, file)

            # Output file in denoised directory
            output_file = os.path.join(
                output_dir,
                (output_prefix) + (file.replace('rgb.', 'rgb_', 1))
            )

            # Find corresponding albedo/normal/motion-vector frames
            frame_part = file.split('.')[1]  # Extract the #### part
            albedo_file = 'albedo.{}.{}'.format(frame_part, file_extension)
            normals_file = 'normals.{}.{}'.format(frame_part, file_extension)
            mv_file = 'motionvector.{}.{}'.format(frame_part, file_extension)

            albedo_frame_path = os.path.join(search_path, 'albedo', albedo_file)
            normals_frame_path = os.path.join(search_path, 'normals', normals_file)
            mv_frame_path = os.path.join(search_path, 'motionvector', mv_file)

            # Build the denoiser command (only include optional inputs if they exist)
            cmd = [
                str(denoiser_exe),
                '-i', str(input_file),
                '-o', str(output_file),
                '-hdr', str(use_hdr),
                '-blend', str(blend_amount),
                '-repeat', str(repeat),
            ]

            if os.path.exists(albedo_frame_path):
                cmd.extend(['-a', albedo_frame_path])
            if os.path.exists(normals_frame_path):
                cmd.extend(['-n', normals_frame_path])
            if os.path.exists(mv_frame_path):
                cmd.extend(['-mv', mv_frame_path])
            if preDenoised_path:
                cmd.extend(['-pi', preDenoised_path])

            FNULL = open(os.devnull, 'w')
            subprocess.call(cmd, stdout=FNULL, stderr=FNULL)
            print('Processed: {} -> {}'.format(input_file, output_file))


prefix = node['prefix'].value()
if prefix == '':
    prefix = prefix
else:
    prefix = prefix + '_'

n = nuke.selectedNode()
topnode_name = nuke.tcl("full_name [topnode %s]" % n.name())
topnode = nuke.toNode(topnode_name)
filename = os.path.basename(topnode['file'].value())
filename = prefix + filename
# denoisedRender = os.path.join(output_dir, 'denoised_rgb_%04d.exr')
denoisedRender = os.path.join(output_dir, filename)
denoisedRender = denoisedRender.replace('\\','/')
read = nuke.nodes.Read(file=denoisedRender, colorspace='scene_linear', first=fristRenderFrame, last=lastRenderFrame)

selectX = node.xpos()
selectY = node.ypos()

read.setXpos(selectX)
read.setYpos(selectY + 100)

nuke.message('Denoising process completed.')