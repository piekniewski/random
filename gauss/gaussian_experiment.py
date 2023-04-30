import numpy as np
import cv2

def random_clt(xx = 400, yy = 200, n_bins = 100, runtime=1000, plot_range=3.5):
    samples = []
    hist_img = np.zeros((yy, xx, 3), dtype=np.uint8)
    bias = 0.0
    sigma = np.sqrt(1.0 / 12)  # Variance of uniform distribution

    for i in range(runtime):
        # Spin 100x quickly to fill up histogram
        for j in range(100):
            M = np.random.rand(yy, xx) - 0.5
            m_sample = np.sqrt(np.prod(M.shape)) * M.mean()
            samples.append(m_sample)
        # If bias is set, sample needs to be clipped as well to keep within -0.5,0.5
        if bias != 0:
           M = np.clip(M + bias, a_min=-0.5, a_max=0.5)
           m_sample = np.sqrt(np.prod(M.shape)) * M.mean()

        hist, bins = np.histogram(samples, bins=n_bins, range=(-plot_range, plot_range), density=True)
        hist_img.fill(0)
        # Plot the histogram
        h_max = hist.max()
        mmul = int(xx/n_bins)
        for x, v in enumerate(hist):
            vv = v / h_max
            cv2.line(hist_img, (x*mmul, yy-10), (x*mmul, yy-10-int(vv * (yy/2))), color=(128, 255, 128), thickness=2)
        # Plot the sigma intervals
        for n_sigma in range(1, 12, 1):
            ss = int(xx * (n_sigma * sigma + plot_range) / (plot_range * 2))
            cv2.line(hist_img, (ss, 20), (ss, yy - 30), color=(255, 128, 128), thickness=1)
            cv2.putText(hist_img, "%ds" % n_sigma, (ss, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 255, 255), 1, cv2.LINE_AA)
            ss = int(xx * (n_sigma * (-1 * sigma) + plot_range) / (plot_range * 2))
            cv2.line(hist_img, (ss, 20), (ss, yy - 30), color=(255, 128, 128), thickness=1)
            cv2.putText(hist_img, "-%ds" % n_sigma, (ss, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 255, 255), 1, cv2.LINE_AA)

        # Plot where the sample landed
        ss = int(xx*(m_sample + plot_range)/(plot_range*2))
        cv2.line(hist_img, (ss, 40), (ss, yy-30),  color=(128, 128, 255), thickness=1)
        n_sig = int(np.abs(m_sample)/sigma) + 1
        cv2.putText(hist_img,
                    "%d sigma" % n_sig,
                    (ss, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (128, 128, 255),
                    1,
                    cv2.LINE_AA)
        if bias != 0:
            cv2.putText(hist_img,
                        "%2.3f bias" % bias,
                        (ss, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4,
                        (128, 128, 255),
                        1,
                        cv2.LINE_AA)

        # Compose the image and display
        m_image = ((M + 0.5)*255).astype(np.uint8)
        img = np.vstack((cv2.cvtColor(m_image, cv2.COLOR_GRAY2RGB), hist_img))
        cv2.imshow("Random grid", img)
        # Press "s" to introduce random bias and freeze animation until a key is pressed
        if bias == 0:
            k = cv2.waitKey(1) & 0xFF
        else:
            k = cv2.waitKey(0) & 0xFF
            bias = 0
        if k == ord("s"):
            bias = (np.random.rand()-0.5) * 0.025
            print("Selected random biad ", bias)


if __name__ == '__main__':
    random_clt()

