import numpy as np
import cv2
import os


def get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1, a2, b1, b2])  # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])  # get first line
    l2 = np.cross(h[2], h[3])  # get second line
    x, y, z = np.cross(l1, l2)  # point of intersection
    if z == 0:  # lines are parallel
        return float('inf'), float('inf')
    return round(x / z), round(y / z)


# process mouse input, gather points and draw visual markers
def click_event(event, x, y, flags, params):
    global curr_img, coordinates, counter
    thickness = 3
    color = (255, 255, 255)

    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print("Selected coordinate: " + str(x) + ', ' + str(y))
        if len(coordinates) < 5:
            coordinates.append(np.array((x, y)))

        counter += 1

        if counter == 0:
            cv2.circle(curr_img, coordinates[counter], radius=0, color=(0, 0, 0), thickness=20)

        if counter == 4:
            cv2.line(curr_img, coordinates[0], coordinates[counter], color, thickness)
            cv2.line(curr_img, coordinates[1], coordinates[counter], color, thickness)
            cv2.line(curr_img, coordinates[2], coordinates[counter], color, thickness)
            cv2.line(curr_img, coordinates[3], coordinates[counter], color, thickness)
            cv2.circle(curr_img, coordinates[0], radius=0, color=(0, 0, 0), thickness=20)
            cv2.circle(curr_img, coordinates[1], radius=0, color=(0, 0, 0), thickness=20)
            cv2.circle(curr_img, coordinates[2], radius=0, color=(0, 0, 0), thickness=20)
            cv2.circle(curr_img, coordinates[3], radius=0, color=(0, 0, 0), thickness=20)
            cv2.circle(curr_img, coordinates[4], radius=0, color=(0, 0, 0), thickness=20)

        if len(coordinates) > 1 and len(coordinates) < 5:

            cv2.line(curr_img, coordinates[counter - 1], coordinates[counter], color, thickness)
            cv2.circle(curr_img, coordinates[counter - 1], radius=0, color=(0, 0, 0), thickness=20)
            cv2.circle(curr_img, coordinates[counter], radius=0, color=(0, 0, 0), thickness=20)

            if counter == 3:
                cv2.line(curr_img, coordinates[0], coordinates[3], color, thickness)
                cv2.circle(curr_img, coordinates[0], radius=0, color=(0, 0, 0), thickness=20)
                cv2.circle(curr_img, coordinates[3], radius=0, color=(0, 0, 0), thickness=20)

        cv2.imshow('image', curr_img)

    if event == cv2.EVENT_RBUTTONDOWN:
        curr_img = img.copy()
        coordinates.clear()
        counter = -1
        cv2.imshow('image', curr_img)

    if flags == 17:  # left click and ctrl click
        cv2.destroyAllWindows()  # destroys the window showing image

    # checking for right mouse clicks


# Main start
path = os.getcwd()
image_name = input("Insert 2D image file name \n")
image_type = input("Insert 2D image file type \n")
print(path)
img = cv2.imread(path + "\\input_2d_tour\\" + image_name + "." + image_type, cv2.IMREAD_COLOR)
H, W, c = img.shape
coordinates = []  # top left, top right, bottom left, bottom right, vanishing point

# Points GUI gathering
# Required order of input points top left, top right, bottom left, bottom right, vanishing point
print("Gathering bounding box and vanishing point...")
cv2.imshow('image', img)
curr_img = img.copy()
counter = -1
cv2.setMouseCallback('image', click_event)
cv2.waitKey(0)

# define all points
box_tlc = coordinates[0]
box_trc = coordinates[1]
box_brc = coordinates[2]
box_blc = coordinates[3]

vanishing_point = coordinates[4]

origin = np.array((0, 0))

image_tr = np.array((W, 0))
image_br = np.array((W, H))
image_bl = np.array((0, H))

# Find line intersections at edge of image
tr_intersect = get_intersect(vanishing_point, box_trc, origin, image_tr)
if tr_intersect[0] < 0 or tr_intersect[0] > W or tr_intersect[1] < 0 or tr_intersect[1] > H:
    tr_intersect = get_intersect(vanishing_point, box_trc, image_tr, image_br)

br_intersect = get_intersect(vanishing_point, box_brc, image_bl, image_br)
if br_intersect[0] < 0 or br_intersect[0] > W or br_intersect[1] < 0 or br_intersect[1] > H:
    br_intersect = get_intersect(vanishing_point, box_brc, image_tr, image_br)

bl_intersect = get_intersect(vanishing_point, box_blc, image_bl, image_br)
if bl_intersect[0] < 0 or bl_intersect[0] > W or bl_intersect[1] < 0 or bl_intersect[1] > H:
    bl_intersect = get_intersect(vanishing_point, box_blc, origin, image_bl)

tl_intersect = get_intersect(vanishing_point, box_tlc, origin, image_tr)
if tl_intersect[0] < 0 or tl_intersect[0] > W or tl_intersect[1] < 0 or tl_intersect[1] > H:
    tl_intersect = get_intersect(vanishing_point, box_tlc, origin, image_br)

tr_intersect = np.array(tr_intersect)
br_intersect = np.array(br_intersect)
tl_intersect = np.array(tl_intersect)
bl_intersect = np.array(bl_intersect)

# Determine depth
f = int(input("Insert focal length: "))
print("Calculating image depth...")
Vo = [W, vanishing_point[1]]
Vi = get_intersect(vanishing_point, Vo, box_trc, box_brc)
h = H - Vi[1]
a = box_brc[1] - Vi[1]
d = round((h * (f / a)) - f)

# Calculate Homography for each side of the image and store image
print("Generating texture map...")

result_dir = path + "\\tour_results\\" + image_name
if not(os.path.isdir(result_dir)):
    os.mkdir(result_dir)
os.chdir(result_dir)


src_r = np.array([[box_trc, tr_intersect, br_intersect, box_brc]])
dst_r = np.array([[[0, 0], [d, 0], [d, H], [0, H]]])  # rectangle Hxdepth

h, status = cv2.findHomography(src_r, dst_r)

im_out_r = cv2.warpPerspective(img, h, (d, H))
cv2.waitKey(0)
cv2.imwrite("right_face.jpg", im_out_r)

src_t = np.array([[tl_intersect, tr_intersect, box_trc, box_tlc]])
dst_t = np.array([[[0, 0], [W, 0], [W, d], [0, d]]])  # rectangle Hxdepth

h, status = cv2.findHomography(src_t, dst_t)

im_out_t = cv2.warpPerspective(img, h, (d, W))
cv2.waitKey(0)
cv2.imwrite("top_face.jpg", im_out_t)

src_b = np.array([[box_blc, box_brc, br_intersect, bl_intersect]])
dst_b = np.array([[[0, 0], [W, 0], [W, d], [0, d]]])  # rectangle Hxdepth

h, status = cv2.findHomography(src_b, dst_b)

im_out_b = cv2.warpPerspective(img, h, (d, W))
cv2.waitKey(0)
cv2.imwrite("bottom_face.jpg", im_out_b)

src_l = np.array([[tl_intersect, box_tlc, box_blc, bl_intersect]])
dst_l = np.array([[[0, 0], [d, 0], [d, H], [0, H]]])  # rectangle Hxdepth

h, status = cv2.findHomography(src_l, dst_l)

im_out_l = cv2.warpPerspective(img, h, (d, H))
cv2.waitKey(0)
cv2.imwrite("left_face.jpg", im_out_l)

src_c = np.array([[box_tlc, box_trc, box_brc, box_blc]])
dst_c = np.array([[[0, 0], [W, 0], [W, H], [0, H]]])  # rectangle Hxdepth

h, status = cv2.findHomography(src_c, dst_c)

im_out_c = cv2.warpPerspective(img, h, (d, H))
cv2.waitKey(0)
cv2.imwrite("center_face.jpg", im_out_c)
