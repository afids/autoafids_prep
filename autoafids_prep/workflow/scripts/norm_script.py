#!/usr/bin/env python
# coding: utf-8

import nibabel as nib


def normalize(input_im, output_im):
    """

    To normalize MRI image using min-max technique.

    Parameters
    ----------
        input_im:: str
            Input image that needs to be normalized.

        output_im:: str
            Name of the modified image

    Returns
    -------
        None

    """
    nii = nib.load(input_im)
    nii_affine = nii.affine
    nii_data = nii.get_fdata()

    nii_data_normalized = (nii_data - nii_data.min()) / (
        nii_data.max() - nii_data.min()
    )

    nib.save(nib.Nifti1Image(nii_data_normalized, affine=nii_affine), output_im)


if __name__ == "__main__":
    normalize(
        input_im=snakemake.input["image"],
        output_im=snakemake.output["train_nii"],
    )
