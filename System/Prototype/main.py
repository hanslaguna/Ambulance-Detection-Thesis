import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import torch
import subprocess
import os


# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=os.path.join(current_directory, 'yolov5', 'best.pt'))

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Labels
        self.result_label = tk.Label(self.window, text='Ambulance Detection Prototype')
        self.result_label.grid(column=0, row=0)

        # Buttons
        self.webcam_button = tk.Button(self.window, text='Webcam', width=50, command=self.detect_webcam)
        self.webcam_button.grid(column=0, row=1)

        self.upload_button = tk.Button(self.window, text='Upload Photo/Video', width=50, command=self.detect_upload)
        self.upload_button.grid(column=0, row=2)

        # Image panel for result
        self.result_panel = tk.Label(self.window)
        self.result_panel.grid(column=0, row=3)

    def process_detection_result(self, result, frame):
        # Implement your logic to process YOLOv5 output and update GUI accordingly
        pass

    def detect_webcam(self):
        # Create a pop-up dialog for the confidence threshold
        confidence_input = simpledialog.askfloat("Confidence Threshold", "Enter Confidence Threshold (0-1):",
                                                 minvalue=0, maxvalue=1)

        # Validate the confidence input
        if confidence_input is not None:
            # Construct the command to run detect.py for webcam
            command = [
                "python",
                "detect.py",
                "--weights", "best.pt",
                "--img", "640",
                "--conf", str(confidence_input),  # Pass the confidence threshold as a string
                "--source", "0"  # 0 for webcam
            ]

            try:
                # Set webcam running status to True
                self.webcam_running = True

                # Run the detection script with the specified working directory
                process = subprocess.Popen(command, cwd=os.path.join(current_directory, 'yolov5'))

                # Periodically check if the webcam window should be closed
                while self.webcam_running:
                    retcode = process.poll()
                    if retcode is not None:
                        # Detection script has finished
                        break

                    # Add a delay to avoid high CPU usage
                    self.window.update_idletasks()
                    self.window.update()

                # Display an alert pop-up when processing is complete
                messagebox.showinfo("Processing Complete", "Webcam processing complete.")

            except subprocess.CalledProcessError as e:
                # Handle any errors that occurred during script execution
                messagebox.showerror("Error", f"An error occurred: {e}")

            finally:
                # Set webcam running status to False when the loop is exited
                self.webcam_running = False

    def detect_upload(self):
        # Similar to your existing detect_upload method
        pass

    def detect_upload(self):
        # Ask the user to select a video file
        video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.jpg;*.png")])

        if video_path:
            # Ask the user to select an output folder
            output_folder = filedialog.askdirectory()

            # Create a pop-up dialog for the confidence threshold
            confidence_input = simpledialog.askfloat("Confidence Threshold", "Enter Confidence Threshold (0-1):",
                                                     minvalue=0, maxvalue=1)

            # Validate the confidence input
            if confidence_input is not None:
                # Construct the command to run detect.py
                command = [
                    "python",
                    "detect.py",
                    "--weights", "best.pt",
                    "--img", "640",
                    "--conf", str(confidence_input),  # Pass the confidence threshold as a string
                    "--source", video_path,
                    "--project", output_folder
                ]

                try:
                    # Run the detection script with the specified working directory
                    subprocess.run(command, check=True, cwd=os.path.join(current_directory, 'yolov5'))

                    # Display an alert pop-up when processing is complete
                    messagebox.showinfo("Processing Complete", "Video processing complete.")
                except subprocess.CalledProcessError as e:
                    # Handle any errors that occurred during script execution
                    messagebox.showerror("Error", f"An error occurred: {e}")


# Create and run the GUI
root = tk.Tk()
app = App(root, "YOLOv5 Object Detection")
root.mainloop()
