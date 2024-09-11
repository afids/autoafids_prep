#!/usr/bin/env python
# coding: utf-8

import ants
import csv
import scipy.io
import numpy as np

def registration(fixed_image, moving_image, out_im, xfm_ras):
    """
    Function that peforms rigid registration.

    Parameters
    ----------

        fixed_image :: str
            Path to reference image to perform registration

        moving_image :: str
            Path to target image that needs to be transformed

        out_im :: str
            Path to resampled image

        xfm_ras :: str
            Path to output affine transformation matrix

    Returns
    -------
        None

    """

    # Load images
    fixed_image = ants.image_read(fixed_image)
    moving_image = ants.image_read(moving_image)

    # Perform rigid registration
    registration_result = ants.registration(
        fixed=fixed_image,
        moving=moving_image,
        type_of_transform='Rigid'
    )

    # Access the results
    registered_image = registration_result['warpedmovout']
    transformation_file_path = registration_result['fwdtransforms'][0]
    transformation_vector_nested = scipy.io.loadmat(transformation_file_path)["AffineTransform_float_3_3"]
    transformation_vector = [transformation_vector_nested[i][0] for i in range(0,len(transformation_vector_nested))]

    # Create the new 3x4 transformation matrix
    transformation_matrix = np.zeros((3, 4))

    # Reshape the vector into a 4x3 matrix, with the last row representing the translation matrix elements
    matrix_4x3 = [transformation_vector[i:i + 3] for i in range(0, len(transformation_vector), 3)]

    # Copy the first three rows and columns from the 4x3 matrix
    transformation_matrix[:, :3] = matrix_4x3[:3][:]

    # Copy the last row of the 4x3 matrix as the last column of the 3x4 matrix
    transformation_matrix[:, 3] = matrix_4x3[3][:]

    # Save the registered image
    ants.image_write(registered_image, out_im)

    # Save the transformation matrix
    with open(xfm_ras, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=' ')
        for row in transformation_matrix:
            writer.writerow(row)

        # Unlike NiftyReg, antspy does not include affine transformation homogeneous coordinate elements.
        # Therefore, we manually write them to the .mat file.
        writer.writerow('0001')
    


if __name__ == "__main__":
    registration(
        fixed_image=snakemake.input["im_resamp"],
        moving_image=snakemake.params["moving"],
        out_im=snakemake.output["out_im"],
        xfm_ras=snakemake.output["xfm_ras"]
    )