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
        double percent;
    
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

class KMean1 {
    public:
        int count;
        int prevcount = 0;
        double percent;
    
        int c;
        
        int csum = 0;
        
        KMean1() {
            c = 0;
            count = 0;
        }
    
        virtual ~KMean1() = default;
    
        KMean1(int color) {
            c = color;
            count = 0;
        }
    
        int distance(int color) {
            int diff = c-color;
            
            return (diff * diff);
        }
};

void cluster3(Mat img, KMean3 means[], const int k) {
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

void cluster1(Mat img, KMean1 means[], const int k) {
    // starting values
    for (int i = 0; i < k; i++) {
        means[i] = KMean1(((double)i/(k-1))*255);
//         cout << means[i].c << endl;
    }
    
    int changed = img.rows * img.cols;
    while (changed = 0) {
        for (int r = 0; r < img.rows; r++) {
            for (int c = 0; c < img.cols; c++) {
                int px = (int)img.at<uchar>(r, c);
                int dist = INT_MAX; 
                int km = -1;
                
                for (int i = 0; i < k; i++) {
                    KMean1 mean = means[i];
                    int curdist = mean.distance(px);
                    
                    if (curdist < dist) {
                        dist = curdist;
                        km = i;
                    }
                }
                
                means[km].csum += px;
                means[km].count += 1;
            }
        }
        
        int overallChanged = 0;
        for (int i = 0; i < k; i++) {
            int count = means[i].count;
            
            if (count == 0) continue;
            
            int avg = means[i].csum / count;
            
            means[i].c = avg;
            
            int numChanged = abs(means[i].count-means[i].prevcount);
            overallChanged += numChanged;
            means[i].percent = (1.0*count/(img.rows*img.cols))*100;
            means[i].prevcount = means[i].count;
            means[i].csum = 0;
            means[i].count = 0;
        }
        
        changed = overallChanged;
    }
}

int main(int argc, char* argv[])
{
    Mat img;
    
    const int k = 4;
    string fname;
    fname = "peppers";
    
    if (argc > 1) {
        fname = argv[1];
    }

    img = imread("in/" + fname + ".png", IMREAD_UNCHANGED);
    Mat kmeanified(img.rows, img.cols, CV_8UC3, Scalar(0,0,0));
    cout << fname << " " << img.channels() << endl;
    if (img.channels() > 3) {
        cvtColor(img, img, COLOR_BGRA2BGR);
    }
    
    if (img.channels() == 3) {
        KMean3 kmeans[k];

        for (int i = 0; i < k; i++) {
            cout << ((double)i/(k-1))*255 << " " << ((double)i/(k-1))*255 << " " << ((double)i/(k-1))*255 << endl;
        }
        
        cluster3(img, kmeans, k);
        
        for (int i = 0; i < k; i++) {
            cout << kmeans[i].r << " " << kmeans[i].g << " " << kmeans[i].b << endl;
        }
        
        
        for (int r = 0; r < img.rows; r++) {
            for (int c = 0; c < img.cols; c++) {
                Vec3b px = img.at<Vec3b>(r, c);
                int dist = INT_MAX;
                int km = 0;

                for (int i = 0; i < k; i++) {
                    int curdist = kmeans[i].distance((int)px[2], (int)px[1], (int)px[0]);

                    if (curdist < dist) {
                        dist = curdist;
                        km = i;
                    }
                }

                px = Vec3b(kmeans[km].b, kmeans[km].g, kmeans[km].r);

                kmeanified.at<Vec3b>(r, c) = px;            
            }
        }

        imwrite("out/" + fname + "_kmeans_rgb.png", kmeanified);
    } else if (img.channels() == 1) {
        KMean1 kmeans[k];
        
        cluster1(img, kmeans, k);
        
        for (int r = 0; r < img.rows; r++) {
            for (int c = 0; c < img.cols; c++) {
                int grayscale = (int)img.at<uchar>(r, c);
                int dist = INT_MAX;
                int km = 0;
                
                for (int i = 0; i < k; i++) {
                    int curdist = kmeans[i].distance(grayscale);
                    
                    if (curdist < dist) {
                        dist = curdist;
                        km = i;
                    }
                }
                
                Vec3b px = Vec3b(kmeans[km].c, kmeans[km].c, kmeans[km].c);
                
                kmeanified.at<Vec3b>(r, c) = px;
            }
        }
  
        imwrite("out/" + fname + "_kmeans_grayscale.png", kmeanified);
    }
    
    return 0;
}
//
// end
//
