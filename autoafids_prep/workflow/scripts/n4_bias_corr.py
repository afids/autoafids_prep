# scripts/n4_bias_correction_snakemake.py
import SimpleITK as sitk
import sys

def n4_bias_correction(input_image_path, output_image_path):
    input_image = sitk.ReadImage(input_image_path, sitk.sitkFloat32)

    corrector = sitk.N4BiasFieldCorrectionImageFilter()

    # Perform the bias field correction
    output_image = corrector.Execute(input_image)

    sitk.WriteImage(output_image, output_image_path)

def main(snakemake):
    input_image_path = snakemake.input.im
    output_image_path = snakemake.output.corrected_im
    
    n4_bias_correction(input_image_path, output_image_path)

if __name__ == "__main__":
    main(snakemake)
