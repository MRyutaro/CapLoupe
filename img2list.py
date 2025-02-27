import argparse
import os


def image_to_list(image_path, output_file):
    with open(image_path, "rb") as img_file:
        byte_list = list(img_file.read())

    variable_name = os.path.splitext(os.path.basename(image_path))[0]

    with open(output_file, "w") as out_file:
        out_file.write(f"{variable_name}_image = {byte_list}\n")

    print(
        f"Image converted and saved to {output_file} as {variable_name}_image.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert an image to a Python list.")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    parser.add_argument("output_file", type=str,
                        help="Path to the output Python file.")

    args = parser.parse_args()

    image_to_list(args.image_path, args.output_file)
