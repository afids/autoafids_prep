#!/usr/bin/env python
# coding: utf-8
import csv
import re

import numpy as np
import pandas as pd


def determineFCSVCoordSystem(input_fcsv):
    """
    Determines if the fcsv file uses Right-Anterior-Superior (RAS) or Left-Posterior-Superior (LPS) coordiante system.

    Parameters
    ----------
        input_fscv:: str
            filename
    Returns
    -------
        coord_sys:: str
            Coordinate system found in the fscv file

    """

    coord_flag = re.compile("# CoordinateSystem")
    coord_sys = None
    with open(input_fcsv, "r+") as fid:
        rdr = csv.DictReader(filter(lambda row: row[0] == "#", fid))

        # Loop through header to find coordinate system (break out of loop once found)
        for row in rdr:
            cleaned_dict = {k: v for k, v in row.items() if k is not None}
            if any(coord_flag.match(x) for x in list(cleaned_dict.values())):
                coord_str = list(filter(coord_flag.match, list(cleaned_dict.values())))
                coord_sys = coord_str[0].split("=")[-1].strip()

                break

    return coord_sys


def xfm_fcsv(fcsv_source, xfm_txt, template, fcsv_new):
    """

    Parameters
    ----------
        fscv_source:: str
            Filepath to the source fscv file.

        xfm_txt:: str
            Filepath to the xfm file.

        template:: str
            Filepath to the template.

        fscv_new:: str
            New fscv file with updated coordinate system.

    Returns
    -------
        None

    """

    # Load transform and groundtruth fcsv
    sub2template = np.loadtxt(xfm_txt)
    fcsv_df = pd.read_table(fcsv_source, sep=",", header=2)

    # Check (and update coord system, if necessary)
    coordSys = determineFCSVCoordSystem(fcsv_source)
    if any(x in coordSys for x in {"LPS", "1"}):
        fcsv_df["x"] = -1 * fcsv_df["x"]  # flip orientation in x
        fcsv_df["y"] = -1 * fcsv_df["y"]  # flip orientation in y

    coords = fcsv_df[["x", "y", "z"]].to_numpy()

    # to plot in mni space, need to transform coords
    tcoords = np.zeros(coords.shape)
    for i in range(len(coords)):
        vec = np.hstack([coords[i, :], 1])
        tvec = np.linalg.inv(sub2template) @ vec.T
        tcoords[i, :] = tvec[:3]

    with open(template, "r", encoding="utf-8") as file:
        list_of_lists = []
        reader = csv.reader(file)
        for i in range(3):
            list_of_lists.append(next(reader))
        for idx, val in enumerate(reader):
            val[1:4] = tcoords[idx][:3]
            list_of_lists.append(val)

    with open(fcsv_new, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(list_of_lists)


if __name__ == "__main__":
    xfm_fcsv(
        fcsv_source=snakemake.params["fcsv_mni"],
        xfm_txt=snakemake.input["xfm_new"],
        template=snakemake.params["fcsv"],
        fcsv_new=snakemake.output["fcsv_new"],
    )
