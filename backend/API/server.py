import os
import json

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from utils import *
from config import Config
from svg import SVG
from bezier import PolyBezier
from coeff import Coefficient_calculator

app = FastAPI()
# This initialises the FastAPI

origins = [
    "http://127.0.0.1:5500",
    "http://127.0.0.1:3000"
]
# This is the location of the frontend website

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# This allows requests to be sent on the same device between the frontend and backend


@app.post("/image")
async def process_image(file: UploadFile):
    """
    This function processes the input image file and returns a JSON data of the drawing data.
    @param file: image file
    @return: json
    """
    save_image(file)
    file_path = os.path.join(Config.IMAGE_PATH, file.filename)
    # get the absolute path to the image file
    extension = get_extension(file.filename)
    if extension != "svg" and extension in Config.ACCEPTABLE_EXTENSIONS:
        svg_path = convert_to_svg(file_path)
        # if the file is not an SVG image, convert to SVG
    elif extension not in Config.ACCEPTABLE_EXTENSIONS:
        raise Exception("The input file is not an image file")
    else:
        svg_path = file_path
    paths = parse_svg(svg_path)
    poly_beziers = compile_polybeziers(paths)
    xlim, ylim = get_lims(poly_beziers)
    sets_of_coeffs = get_sets_coeffs(poly_beziers, Config.NUM_VECTORS, Config.BY_DIST)
    data = {
        "lim": {"x": xlim, "y": ylim},
        "sets_of_coeffs": sets_of_coeffs,
    }
    return json.dumps(data)


def save_image(file):
    """
    This function saves the input file to the directory that is specified in the Config class
    @param file: file to be saved
    """
    with open(os.path.join("images", file.filename), "wb") as f:
        f.write(file.file.read())

def convert_to_svg(file_path: str) -> str:
    """
    This function converts the input file to an SVG image using Potrace
    @param file_path: file_path as a string
    @return: Path to the converted SVG image as a string
    """
    filename = get_filename(file_path)
    pnm = f"{filename}.pnm"
    if get_extension(filename) != "pnm":
        os.system(f"convert {file_path} -background white -alpha remove -alpha off {pnm}")
    svg = f"{filename}.svg"
    os.system(f"potrace --flat {pnm} -s -o {svg}")
    os.remove(pnm)
    return svg


def parse_svg(file_path):
    """
    This function parses the SVG file specified by the input path using the SVG class
    @param file_path: Path to the SVG file as a string
    @return: A list of Bezier curve objects
    """
    data = get_file_content(file_path)
    # svg file as a string
    paths = SVG(data).parse_path()
    return paths


def compile_polybeziers(paths: list) -> list:
    """
    This function creates PolyBezier(s) using the input list of Bezier curve objects
    @param paths: A list of Bezier curve objects
    @return: A list of PolyBezier curve objects
    """
    polys = []
    for path in paths:
        poly = PolyBezier(path)
        polys.append(poly)
    return polys


def get_sets_coeffs(polys: list, num: int, by_dist: bool = False) -> list:
    """
    This functoin gets a set of coefficients for each PolyBezier in the input polys list
    @param polys: A list of PolyBezier curve objects
    @param num: The number of vectors
    @param by_dist: If the tip of the pe moves at a constant speed in the animation
    @return: A list of set(s) of coefficeints
    """
    sets_of_coeffs = []
    for poly in polys:
        calc = Coefficient_calculator(poly, num, by_dist)
        sets_of_coeffs.append(calc.main())
    return sets_of_coeffs


def get_lims(polys: list):
    """
    This function gets the minimum and maximum values of real and imaginary coordinates
    @param polys: A list of PolyBezier curve objects
    @return: A tuple of tuples, consisting of xlim and ylim
    """
    lims = [poly.get_lims() for poly in polys]
    xs = [lim[0] for lim in lims]
    ys = [lim[1] for lim in lims]
    xlim = (min(xs, key=lambda item: item[0])[0], max(xs, key=lambda item: item[1])[1])
    ylim = (min(ys, key=lambda item: item[0])[0], max(ys, key=lambda item: item[1])[1])
    return xlim, ylim


if __name__ == "__main__":
    uvicorn.run("server:app", port=3000)
    # This sets up a server on the machine on which this file is executed
