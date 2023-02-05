import logging
import os
import subprocess


def launch_runelite():
    logger = logging.getLogger(__name__)
    print(os.getcwd())
    logger.info('Booting RuneLite')
    rc = subprocess.call("./boot_runelite.sh")