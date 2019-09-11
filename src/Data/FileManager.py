import os
import csv
import open3d as o3
import cv2
import numpy as np


# system navigation
def get_items_in_dir(my_path=""):
    my_path = os.getcwd() if my_path == "" or my_path is None else my_path
    files = []
    for roots, dirs, items in os.walk(my_path):
        [files.append(os.path.join(roots, item)) for item in items]
    return files


def __is_dir_file_correct__(file):
    dirname = os.path.dirname(file)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    if os.path.exists(dirname) and os.path.isdir(dirname):
        if os.path.exists(dirname):
            return True, dirname
        else:
            return True, os.getcwd()
    else:
        raise Exception("IS_DIR_FILE_CORRECT: error checking the file, file path not right")
        return False, None


def is_file_correct(file):
    dircorrect, dirname = __is_dir_file_correct__(file)
    file = os.path.join(dirname, os.path.basename(file))
    if dircorrect and os.path.exists(file) and os.path.isfile(file):
        return True, file
    else:
        print("IS_FILE_CORRECT: error checking the file, file path not right")
        return False, None


def is_new_file_correct(file):
    dircorrect, dirname = __is_dir_file_correct__(file)
    file = os.path.join(str(dirname), str(os.path.basename(file)))
    if dircorrect:
        if not os.path.exists(file):
            return True, file
        else:
            # TODO
            # changes filename to "file (1), (2) ..."
            # right now it just overrides the file
            return True, file
    else:
        print("IS_FILE_CORRECT: error checking the file, file path not right")
        return False, None


def is_data_correct(data):
    if data is not None:
        return True
    elif data:
        return True
    else:
        print("IS_DATA_CORRECT: error writing the file, the data is empty")
        return False


# CSV
def write_csv(file, data):
    correct, file = is_new_file_correct(file)
    if correct:
        if is_data_correct(data):
            with open(file, mode='w+') as f:
                writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
                writer.writeheader()
                writer.writerows(data)
        else:
            print("error writing the csv file, data is empty")
    else:
        print("error writing the csv file, file path not right")


def load_csv(file):
    correct, file = is_file_correct(file)
    if correct and os.path.exists(file):
        with open(file) as f:
            reader = csv.reader(f, delimiter=',')
            line_count = 0
            for row in reader:
                if line_count == 0:
                    print("Column names are {}\n".format(row))
                    line_count += 1
                else:
                    print("{0}}: Column names are {1}}\n".format(line_count, row))
                    line_count += 1
            print("Processed {} lines.\n".format(line_count))

# def load_csv(file):
#     correct, file = is_file_correct(file)
#     if correct and os.path.exists(file):
#         with open(file) as f:
#             reader = csv.reader(f, delimiter=',')
#             line_count = 0
#             for row in reader:
#                 if line_count == 0:
#                     print(f'Column names are {", ".join(row)}')
#                     line_count += 1
#                 else:
#                     print(f'{line_count}.:  {", ".join(row)}')
#                     line_count += 1
#             print(f'Processed {line_count} lines.')


def create_csv():
    """
    Creates a csv file with all the files in the current dir and its expected result for the neural network
    :return:
    """
    files = get_items_in_dir()
    data_RGBDIJ = []
    data_PNG = []

    for item in files:
        if ".mine" in item:
            data = data_RGBDIJ
        elif ".png" in item:
            data = data_PNG
        else:
            continue

        item = item.replace("/home/alberto/Documents/workspace/Robolab/RoboLAMB/RoboLAMB/", "")

        if "con_oveja" in item:
            file = {"path": item, "result": "lamb"}
            data.append(file)
        elif "mal_oveja" in item:
            file = {"path": item, "result": "error"}
            data.append(file)
        elif "sin_oveja" in item:
            file = {"path": item, "result": "empty"}
            data.append(file)

    write_csv(os.path.join(os.getcwd(), "out_RGBDIJ.csv"), data_RGBDIJ)
    write_csv(os.path.join(os.getcwd(), "out_PNG.csv"), data_PNG)


# Working with Images
# RGBD, Open3D_PointCloud, RGBDij
class RGBDIJ:
    #
    # def __init__(self, collection):
    #     # self.collection = np.zeros((480, 640, 6), dtype=np.float64)
    #     self._collection = collection

    @classmethod
    def load_file(cls, file_path):
        color_image = np.zeros((480, 640, 3), dtype=np.uint8)
        depth_image = np.zeros((480, 640, 1), dtype=np.uint16)
        correct, file_path = is_file_correct(file_path)
        if correct:
            with open(file_path, "r") as f:
                for line in f:
                    if len(line) < 2:
                        print(line)
                        continue
                    line = line.split(" ")
                    i = int(line[4])
                    j = int(line[5])
                    color_image[i][j][0] = np.uint8(line[0])
                    color_image[i][j][1] = np.uint8(line[1])
                    color_image[i][j][2] = np.uint8(line[2])
                    depth_image[i][j] = np.uint16(line[3])
            return color_image, depth_image
        else:
            raise Exception("cannot load file " + str(file_path))

    @classmethod
    def save_file(cls, color_image, depth_image, file):
        correct, file_path = is_new_file_correct(file)
        if correct:
            with open(file, "w+") as f:
                for (i, j, pos), value in np.ndenumerate(color_image):
                    f.write(str(value) + " ")
                    if pos == 2:
                        f.write(str(depth_image[i][j]) + " " + str(i) + " " + str(j) + " \n")




if __name__ == '__main__':
    create_csv()
