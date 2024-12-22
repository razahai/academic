#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>

using namespace std;
using namespace cv;

class KMean3 {
    public:
        int count;
        int prevcount = 0;
        int percent;
    
        int r;
        int g;
        int b;
        
        int rsum = 0;
        int gsum = 0;
        int bsum = 0;
    
        KMean3() {
            r = 0;
            g = 0;
            b = 0;
            count = 0;
        }
    
        virtual ~KMean3() = default;
    
        KMean3(int red, int green, int blue) {
            r = red;
            g = green;
            b = blue;
            count = 0;
        }
    
        int distance(int red, int green, int blue) {
            int rdiff = r-red;
            int gdiff = g-green;
            int bdiff = b-blue;
            
            return (rdiff * rdiff) + (gdiff * gdiff) + (bdiff * bdiff);
        }
};

void kmeans_cluster(Mat img, KMean3 means[], const int k) {
    // starting values
    for (int i = 0; i < k; i++) {
        means[i] = KMean3(((double)i/(k-1))*255, ((double)i/(k-1))*255, ((double)i/(k-1))*255);
    }
    
    int changed = img.rows * img.cols;
    while (changed = 0) {
        for (int r = 0; r < img.rows; r++) {
            for (int c = 0; c < img.cols; c++) {
                Vec3b px = img.at<Vec3b>(r, c);
                int dist = INT_MAX; 
                int km = -1;
                
                for (int i = 0; i < k; i++) {
                    KMean3 mean = means[i];
                    int curdist = mean.distance((int)px[2], (int)px[1], (int)px[0]);
                    
                    if (curdist < dist) {
                        dist = curdist;
                        km = i;
                    }
                }
                
                means[km].rsum += (int)px[2];
                means[km].gsum += (int)px[1];
                means[km].bsum += (int)px[0];
                means[km].count += 1;
            }
        }
        
        int overallChanged = 0;
        for (int i = 0; i < k; i++) {
            int count = means[i].count;
            
            if (count == 0) continue;
            
            int ravg = means[i].rsum / count;
            int gavg = means[i].gsum / count;
            int bavg = means[i].bsum / count;
            
            means[i].r = ravg;
            means[i].g = gavg;
            means[i].b = bavg;
        
            int numChanged = abs(means[i].count-means[i].prevcount);
            overallChanged += numChanged;
            means[i].prevcount = means[i].count;
            means[i].percent = (1.0*count/(img.rows*img.cols))*100;
            means[i].rsum = 0;
            means[i].gsum = 0;
            means[i].bsum = 0;
            means[i].count = 0;
        }
        
        changed = overallChanged;
    }
}

int main(int argc, char* argv[])
{
    string fname;
    string num;
    const int k = 2; // white & x
    
    num = argv[1];
    fname = "in/cards/" + num + ".png";
    
    Mat card = imread(fname, IMREAD_UNCHANGED);
    
    if (card.channels() > 3) {
        // remove alpha channel
        cvtColor(card, card, COLOR_BGRA2BGR);
    }

    KMean3 kmeans[k];
    
    kmeans_cluster(card, kmeans, k);
    
    cout << "Card " << num << endl;
    
    for (int i = 0; i < k; i++) {
        if (kmeans[i].r > 200 && kmeans[i].g > 200 && kmeans[i].b > 200) {
            cout << "White: (" << kmeans[i].r << ", " << kmeans[i].g << ", " << kmeans[i].b << ")" << endl; 
        } else if (kmeans[i].r > kmeans[i].g && kmeans[i].r > kmeans[i].b) {
            cout << "Red: (" << kmeans[i].r << ", " << kmeans[i].g << ", " << kmeans[i].b << ")" << endl;
        } else if (kmeans[i].g > kmeans[i].r && kmeans[i].g > kmeans[i].b) {
            cout << "Green: (" << kmeans[i].r << ", " << kmeans[i].g << ", " << kmeans[i].b << ")" << endl;
        } else if (kmeans[i].g < 100 && kmeans[i].r > kmeans[i].g && kmeans[i].b > kmeans[i].g) {
            cout << "Purple: (" << kmeans[i].r << ", " << kmeans[i].g << ", " << kmeans[i].b << ")" << endl;
        } else {
            cout << "Unknown: (" << kmeans[i].r << ", " << kmeans[i].g << ", " << kmeans[i].b << ")" << endl;
        }
    }
    
    // edge detection https://homepages.inf.ed.ac.uk/rbf/HIPR2/sobel.htm
    
    cvtColor(card, card, COLOR_BGR2GRAY);
    Mat edges(card.rows, card.cols, CV_8UC1, Scalar(255));
    
    double kernel[3][3] = {
        {0.111, 0.111, 0.111},
        {0.111, 0.111, 0.111},
        {0.111, 0.111, 0.111}
    };
 
    for (int r = 1; r < card.rows-1; r++) {
        for (int c = 1; c < card.cols-1; c++) {
            double k0 = ((int)card.at<uchar>(r-1, c-1))*kernel[0][0];
            double k1 = ((int)card.at<uchar>(r-1, c))*kernel[0][1];
            double k2 = ((int)card.at<uchar>(r-1, c+1))*kernel[0][2];
            double k3 = ((int)card.at<uchar>(r, c-1))*kernel[1][0];
            double k4 = ((int)card.at<uchar>(r, c))*kernel[1][1];
            double k5 = ((int)card.at<uchar>(r, c+1))*kernel[1][2];
            double k6 = ((int)card.at<uchar>(r+1, c-1))*kernel[2][0];
            double k7 = ((int)card.at<uchar>(r+1, c))*kernel[2][1];
            double k8 = ((int)card.at<uchar>(r+1, c+1))*kernel[2][2];

            double mag = k0+k1+k2+k3+k4+k5+k6+k7+k8;
            uchar m = mag;

            edges.at<uchar>(r, c) = m;
        }
     }

    int gx[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    int gy[3][3] = {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };
     
    for (int r = 1; r < card.rows-1; r++) {
        for (int c = 1; c < card.cols-1; c++) {
            int gx0 = ((int)card.at<uchar>(r-1, c-1))*gx[0][0];
            int gx1 = ((int)card.at<uchar>(r-1, c))*gx[0][1];
            int gx2 = ((int)card.at<uchar>(r-1, c+1))*gx[0][2];
            int gx3 = ((int)card.at<uchar>(r, c-1))*gx[1][0];
            int gx4 = ((int)card.at<uchar>(r, c))*gx[1][1];
            int gx5 = ((int)card.at<uchar>(r, c+1))*gx[1][2];
            int gx6 = ((int)card.at<uchar>(r+1, c-1))*gx[2][0];
            int gx7 = ((int)card.at<uchar>(r+1, c))*gx[2][1];
            int gx8 = ((int)card.at<uchar>(r+1, c+1))*gx[2][2];
            
            int gy0 = ((int)card.at<uchar>(r-1, c-1))*gy[0][0];
            int gy1 = ((int)card.at<uchar>(r-1, c))*gy[0][1];
            int gy2 = ((int)card.at<uchar>(r-1, c+1))*gy[0][2];
            int gy3 = ((int)card.at<uchar>(r, c-1))*gy[1][0];
            int gy4 = ((int)card.at<uchar>(r, c))*gy[1][1];
            int gy5 = ((int)card.at<uchar>(r, c+1))*gy[1][2];
            int gy6 = ((int)card.at<uchar>(r+1, c-1))*gy[2][0];
            int gy7 = ((int)card.at<uchar>(r+1, c))*gy[2][1];
            int gy8 = ((int)card.at<uchar>(r+1, c+1))*gy[2][2];
            
            int mag_x = gx0+gx1+gx2+gx3+gx4+gx5+gx6+gx7+gx8;
            int mag_y = gy0+gy1+gy2+gy3+gy4+gy5+gy6+gy7+gy8;
            int mag = abs(mag_x)+abs(mag_y);

            if (mag > 110) {
                edges.at<uchar>(r,c) = 0;
            } else {
                edges.at<uchar>(r,c) = 255;
            }
        }
     }
    
    imwrite("out/cards/card_" + num + "_sobel_edges.png", edges);
    
    return 0;
}
//
// end
//
