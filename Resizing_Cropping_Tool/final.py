import cv2 as cv
import os

def resize_image(frame, target_width=None, target_height=None):
    #Resize the image while maintaining aspect ratio
    height, width = frame.shape[:2]
    
    if target_width and not target_height:
        scale = target_width / width
    elif target_height and not target_width:
        scale = target_height / height
    elif target_width and target_height:
        scale = min(target_width / width, target_height / height)
    else:
        return frame  # No resizing if dimensions are not provided

    new_width = int(width * scale)
    new_height = int(height * scale)
    return cv.resize(frame, (new_width, new_height), interpolation=cv.INTER_LINEAR)

def crop_image(frame, start_x, end_x, start_y, end_y):
    #Crop the image to specified dimensions
    return frame[start_y:end_y, start_x:end_x]

def user_input():
    #Get user input for resizing or cropping operations
    print("Choose an operation:")
    print("1: Resize the image")
    print("2: Crop the image")
    
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        target_width = int(input("Enter target width (or 0 to skip): ")) or None
        target_height = int(input("Enter target height (or 0 to skip): ")) or None
        return choice, (target_width, target_height)
    
    elif choice == '2':
        start_x = int(input("Enter start width (x): "))
        end_x = int(input("Enter end width (x): "))
        start_y = int(input("Enter start height (y): "))
        end_y = int(input("Enter end height (y): "))
        return choice, (start_x, end_x, start_y, end_y)
    
    else:
        print("Invalid choice. Please select 1 or 2.")
        return None, None

def process_images(input_folder, output_folder, choice, params):
    #Batch process images for resizing or cropping
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)
        img = cv.imread(img_path)
        
        if img is None:
            print(f"Error: Could not read image {filename}")
            continue

        # Process image based on user input
        if choice == '1':  # Resize
            target_width, target_height = params
            final_image = resize_image(img, target_width, target_height)
        elif choice == '2':  # Crop
            start_x, end_x, start_y, end_y = params
            final_image = crop_image(img, start_x, end_x, start_y, end_y)

        # Save the processed image
        output_path = os.path.join(output_folder, filename)
        cv.imwrite(output_path, final_image)
        print(f"Processed and saved: {output_path}")

    print("Batch processing complete.")

def main():
    input_folder = 'Images' #Use a folder of sample images and change folder name if needed
    output_folder = 'Processed_Images'
    
    choice, params = user_input()
    if choice and params:
        process_images(input_folder, output_folder, choice, params)


main()
