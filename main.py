import argparse
import logging

import examples.two_tons
import examples.spinner
import examples.earth_moon

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Gravity")
    parser.add_argument("--scene", help="select compute scene")
    args = parser.parse_args()
    scene_name = args.scene

    available_scenes = dict(
        two_tons=examples.two_tons.TwoTons(),
        spinner=examples.spinner.Spinner(),
        earth_moon=examples.earth_moon.EarthMoon(),
    )
    scene = available_scenes.get(scene_name)
    if scene:
        logging.info("Starting.")
        scene.run()
        logging.info("Ending.")
    else:
        logging.error(f"""The scene "{scene_name}" is missing.\n"""
                      f"""Available scene keys is: {", ".join([ f'"{name}"' for name in available_scenes.keys()])}.""")
