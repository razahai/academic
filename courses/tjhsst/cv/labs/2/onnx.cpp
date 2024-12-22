#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/dnn/dnn.hpp> 
#include <iostream>

using namespace std;
using namespace cv;
using namespace dnn;

int main(int argc, char* argv[]) {
    Net nn = readNetFromONNX("in/onnx/lenet.onnx");
    
    Mat img = imread("in/onnx/test/0/0_294.png", IMREAD_GRAYSCALE);
    
                               // 255.0 for mnist
    Mat blob1 = blobFromImage(img, 1.0, Size(28, 28));

    nn.setInput(blob1);
    
    Mat p = nn.forward();
    
    cout << "lenet" << endl;
    for(int j = 0; j < 10; j++) {
        cout << j << " " << p.at<float>(0, j) << endl;
    }
    
    Net nn2 = readNetFromONNX("in/onnx/mnist-12.onnx");
    Mat blob2 = blobFromImage(img, 255.0, Size(28, 28));
    
    nn2.setInput(blob2);
    
    Mat p2 = nn2.forward();
    
    cout << "mnist" << endl;
    for(int j = 0; j < 10; j++) {
        cout << j << " " << p2.at<float>(0, j) << endl;
    }

    return 0;
}
//
// end
//
// 0 -1.29173
// 1 -37.7373
// 2 -14.1875
// 3 -40.2945
// 4 24.9275
// 5 3.26107
// 6 -20.963
// 7 16.2836
// 8 7.30168
// 9 64.0996
//
/* ******************* */
