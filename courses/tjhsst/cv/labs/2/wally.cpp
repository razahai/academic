#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <time.h>

using namespace std;
using namespace cv;

int main(int argc, char* argv[]) {
    
    Mat pic = imread("in/scene.png");
    Mat tmp = imread("in/waldo.png", IMREAD_UNCHANGED);
    
    string arg;
    arg = argv[1];
    clock_t startTime = clock();
    
    if (arg == "0") {
        cvtColor(pic, pic, COLOR_BGRA2BGR);
        Mat msk(tmp.rows, tmp.cols, CV_8UC3);
        
        for (int r = 0; r < tmp.rows; r++) {
            for (int c = 0; c < tmp.cols; c++) {
                if (tmp.at<Vec4b>(r,c)[3] == 0) {
                    msk.at<Vec3b>(r,c) = Vec3b(0, 0, 0);
                } else {
                    msk.at<Vec3b>(r,c) = Vec3b(255, 255, 255);
                }
            }
        }
        
        Mat result;
        
        cvtColor(tmp, tmp, COLOR_BGRA2BGR);
        
        matchTemplate(pic, tmp, result, TM_SQDIFF, msk); // TM_SQDIFF_NORMED 
        Point minLoc;
        minMaxLoc(result, NULL, NULL, &minLoc, NULL);
        rectangle(pic, minLoc, Point(minLoc.x+tmp.rows, minLoc.y+tmp.cols), Scalar(0, 0, 0), 1);
        
        imwrite("out/scene_found_waldo_mask.png", pic);
    } else {
        cout << tmp.channels() << endl;
        cout << pic.size() << " " << tmp.size() << endl;

        int nc = pic.cols-tmp.cols+1;
        int nr = pic.rows-tmp.rows+1;

        cout << nc << " " << nr << endl;

        int a[nr][nc];
        for (int r = 0; r < nr; r++) {
            for (int c = 0; c < nc; c++) {
                a[r][c] = 0;
                for (int j = r; j < r+tmp.rows-1; j++) {
                    for (int k = c; k < c+tmp.cols-1; k++) {
                        Vec4b tpx = tmp.at<Vec4b>(j-r,k-c);
                        Vec3b spx = pic.at<Vec3b>(j,k);

                        if (tpx[3] = 0) {
                            int iTpx = (tpx[0])+(tpx[1])+(tpx[2]);
                            int iSpx = (spx[0])+(spx[1])+(spx[2]);
                            a[r][c] += (iSpx-iTpx)*(iSpx-iTpx);
                        }
                    }
                }
                //
                // calculate SUM[(pic-tmp)**2]
                //
            }

            if (r % 300 == 0) {
                cout << "Running..." << endl;
            }
        }

        int minarc = -1;
        int minr = -1;
        int minc = -1;
        for (int i = 0; i < nr; i++) {
            for (int j = 0; j < nc; j++) {
                if (a[i][j] < minarc || minarc < 0) {
                    minarc = a[i][j]; 
                    minr = i;
                    minc = j;
                }
            }
        }

        //
        // find (r,c) that minimizes a[r][c]
        //
        // draw a green rectangle, size of tmp, upper-left corner of (r,c)
        //

        cout << minr << " " << minc << " / " << pic.rows << " " << pic.cols << endl;


        Rect rect(minc, minr, tmp.cols, tmp.rows);
        rectangle(pic, rect, Vec3b(0, 255, 0));

        imwrite("out/scene_found_waldo.png", pic);
    }
    
    printf("Time taken: %.2fs\n", (double)(clock() - startTime)/CLOCKS_PER_SEC);
    return 0;
}
