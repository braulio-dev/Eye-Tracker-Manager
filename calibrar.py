import asyncio
import tkinter as tk
import tobii_research as tr
import time
import threading

def circulo(canvas, x, y):
    return canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="red", outline="black")


def calibrar(eyetracker):
    if eyetracker is None:
        print('No eye tracker')
        return

    calibracion = tk.Tk()
    calibracion.overrideredirect(True)  # turns off title bar
    calibracion.state('zoomed')
    calibracion.resizable(False, False)
    calibracion.title("Calibrar")
    calibration = tr.ScreenBasedCalibration(eyetracker)

    canvas = tk.Canvas(calibracion, bg='gray')
    canvas.pack(fill='both', expand=True)
    canvas.pack()

    def calibrate_async():
        calibration.enter_calibration_mode()
        print("Entered calibration mode for eye tracker with serial number {0}.".format(eyetracker.serial_number))

        points_to_calibrate = [(0.5, 0.5), (0.1, 0.1), (0.1, 0.9), (0.9, 0.1), (0.9, 0.9)]

        for point in points_to_calibrate:
            print("Show a point on screen at {0}.".format(point))

            cir = circulo(canvas, point[0] * calibracion.winfo_screenwidth(), point[1] * calibracion.winfo_screenheight())
            calibracion.update()

            time.sleep(1.5)
            canvas.delete(cir)

            print("Collecting data at {0}.".format(point))
            if calibration.collect_data(point[0], point[1]) != tr.CALIBRATION_STATUS_SUCCESS:
                calibration.collect_data(point[0], point[1])

        print("Computing and applying calibration.")
        calibration_result = calibration.compute_and_apply()
        print("Compute and apply returned {0} and collected at {1} points.".format(calibration_result.status, len(calibration_result.calibration_points)))

        recalibrate_point = (0.1, 0.1)
        print("Removing calibration point at {0}.".format(recalibrate_point))
        calibration.discard_data(recalibrate_point[0], recalibrate_point[1])

        print("Show a point on screen at {0}.".format(recalibrate_point))
        cir = circulo(canvas, recalibrate_point[0] * calibracion.winfo_screenwidth(), recalibrate_point[1] * calibracion.winfo_screenheight())
        calibracion.update()
        time.sleep(1.5)
        canvas.delete(cir)
        calibration.collect_data(recalibrate_point[0], recalibrate_point[1])

        print("Computing and applying calibration.")
        calibration_result = calibration.compute_and_apply()
        print("Compute and apply returned {0} and collected at {1} points.".format(calibration_result.status, len(calibration_result.calibration_points)))

        calibration.leave_calibration_mode()

        print("Left calibration mode")

        # Close the fullscreen window
        calibracion.destroy()
        calibracion.quit()

    # Run calibration asynchronously in a separate thread
    calibration_thread = threading.Thread(target=calibrate_async)
    calibration_thread.start()
    calibracion.mainloop()

