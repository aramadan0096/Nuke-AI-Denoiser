# Registers the OptixDenoiser gizmo in Nuke's Nodes toolbar.
# Place this file alongside init.py so Nuke auto-loads it from the plugin path.

import nuke


def _register_optix_gizmo():
    # Create/locate a top-level "OptiX" menu with an icon.
    nodes_menu = nuke.menu('Nodes')
    optix_menu = nodes_menu.findItem('OptiX')
    if optix_menu is None:
        # The icon file is resolved via plugin paths (init.py adds ./imgs)
        optix_menu = nodes_menu.addMenu('OptiX', icon='nvidiaLogo.png')

    # Add command to create the gizmo node.
    # Gizmo class name must match the Group name inside the .gizmo file.
    optix_menu.addCommand(
        'Optix Denoiser',
        'nuke.createNode("optixDenoiser.gizmo")',
        icon='nvidiaLogo.png',
    )


try:
    _register_optix_gizmo()
except Exception as e:
    # Use tprint so it shows in Script Editor without stopping Nuke from loading.
    nuke.tprint('OptixDenoiser menu setup failed: {}'.format(e))
