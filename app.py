# python imports
import argparse
import asyncio
import logging
import time
from datetime import datetime

# idotmatrix imports
from core.cmd import CMD

import life.life
import clock.clock
import particles.particles

def log():
    # set basic logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
        handlers=[logging.StreamHandler()],
    )
    # set log level of asyncio
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    # set log level of bleak
    logging.getLogger("bleak").setLevel(logging.WARNING)

def run_game_of_life(args, cmd):
    # set a path to save the image to
    life_image_path = "./images/life/next_generation.png"

    # Create an initial grid
    grid = life.life.create_grid()

    # delay updates
    timeout = 1.0

    while True:
        # Generate the next generation
        grid = life.life.get_next_generation(grid)

        # Render the next generation as a PNG image
        life.life.render_grid_to_png(grid, life_image_path)

        # Set the image path
        args.set_image = life_image_path

        # run set image command
        asyncio.run(cmd.run(args))

        # delay update
        time.sleep(timeout)

def seconds_remaining_in_minute():
    now = datetime.now()
    return 60 - now.second

def run_clock(args, cmd):

    remaining_seconds = seconds_remaining_in_minute()

    # generate clock image
    CLOCK_IMAGE_PATH = './images/clock/clock.png'
    clock.clock.save_clock_image(CLOCK_IMAGE_PATH)

    # Set the image path
    args.set_image = CLOCK_IMAGE_PATH

    # run set image command
    asyncio.run(cmd.run(args))

    # delay update
    time.sleep(remaining_seconds)

    while True:

        # generate clock image
        CLOCK_IMAGE_PATH = './images/clock/clock.png'
        clock.clock.save_clock_image(CLOCK_IMAGE_PATH)

        # Set the image path
        args.set_image = CLOCK_IMAGE_PATH

        # run set image command
        asyncio.run(cmd.run(args))

        # delay update
        time.sleep(seconds_remaining_in_minute())


def run_particles(args,cmd):
    PARTICLES_IMAGE_PATH = './images/particles/particles.png'
    grid = particles.particles.create_grid()
    timeout = 0.2
    while True:
        # render next frame
        particles.particles.render_grid_to_png(grid, PARTICLES_IMAGE_PATH)

        # Set the image path
        args.set_image = PARTICLES_IMAGE_PATH

        # run set image command
        asyncio.run(cmd.run(args))

        # delay update
        time.sleep(timeout)

def main():
    cmd = CMD()
    parser = argparse.ArgumentParser(
        description="control all your 16x16 or 32x32 pixel displays"
    )
    # global argument
    parser.add_argument(
        "--address",
        action="store",
        help="the bluetooth address of the device",
    )
    # add cmd arguments
    cmd.add_arguments(parser)
    # parse arguments
    args = parser.parse_args()
    # run command
    asyncio.run(cmd.run(args))

    """ my code here... """
    # Set the image path
    args.set_image = "./images/demo_32.png"
    
    # Enable image mode
    args.image = True
    
    # Run command
    asyncio.run(cmd.run(args))

    # Game of life - requires image mode already enabled
    #run_game_of_life(args, cmd)

    # Custom clock
    run_clock(args, cmd)

    # Particles
    #run_particles(args,cmd)



if __name__ == "__main__":
    log()
    log = logging.getLogger("idotmatrix")
    log.info("initialize app")
    try:
        main()
    except KeyboardInterrupt:
        log.info("Caught keyboard interrupt. Stopping app.")
