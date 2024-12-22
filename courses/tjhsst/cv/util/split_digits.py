from PIL import Image
import os

def split_mnist_image(image_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the image file
    img = Image.open(image_path)

    # Define the dimensions of each digit image
    digit_width, digit_height = 20, 20

    # Number of columns per digit
    columns_per_digit = 100

    # Total width of the image (in pixels)
    total_width = columns_per_digit * digit_width

    # Loop over each digit (0-9)
    for digit in range(10):
        digit_dir = os.path.join(output_dir, str(digit))
        if not os.path.exists(digit_dir):
            os.makedirs(digit_dir)

        # Loop over each row and column for the current digit
        for row in range(5):
            for col in range(columns_per_digit):
                # Calculate the starting position of the digit block
                left = col * digit_width
                upper = digit * 5 * digit_height + row * digit_height
                right = left + digit_width
                lower = upper + digit_height

                # Debug: Print coordinates
                print(f"Digit: {digit}, Row: {row}, Col: {col}, Coordinates: ({left}, {upper}, {right}, {lower})")

                # Crop the image
                cropped_img = img.crop((left, upper, right, lower))

                # Save the cropped image
                cropped_img_filename = f"{digit}_{row * columns_per_digit + col}.png"
                cropped_img.save(os.path.join(digit_dir, cropped_img_filename))

    print("Image splitting complete.")

image_path = '/csl/users/--/cluster/cv/in/onnx/digits.png'
output_dir = '/csl/users/--/cluster/cv/in/onnx/test/'
split_mnist_image(image_path, output_dir)
