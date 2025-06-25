import cv2

test_image_location = "C:/medusa-test-images/2008/06"


image1_path = "C:/repos/bitbucket/Cosmos/medusa/test-images/img_1.jpg"
image2_path = "C:/repos/bitbucket/Cosmos/medusa/test-images/img_2.jpg"

image1 = cv2.imread(image1_path)
image2 = cv2.imread(image2_path)

hist_img1 = cv2.calcHist([image1], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
hist_img1[255, 255, 255] = 0 #ignore all white pixels
cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
hist_img2 = cv2.calcHist([image2], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
hist_img2[255, 255, 255] = 0  #ignore all white pixels
cv2.normalize(hist_img2, hist_img2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
# Find the metric value
metric_val = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL)
print(f"Similarity Score: ", round(metric_val, 2))
# Similarity Score: 0.94
