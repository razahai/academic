#include <fstream>
#include <iostream>

using namespace std;

typedef unsigned char uchar;

int main(int argc, char* argv[])
{
    ofstream fout;
    
    int r, c;
    int color[] = {0, 255, 0}; 
    int middle_row = 0;
    int middle_col = 0;
    
    uchar img[480][640][3];
    for (r = 0; r < 480; r++) {
        for (c = 0; c < 640; c++) {
            if (middle_row == 24 || middle_row == 25) {
                if (color[0] == 255) {
                    img[r][c][0] = (uchar)255;
                    img[r][c][1] = (uchar)0;
                    img[r][c][2] = (uchar)0;
                } else {
                    img[r][c][0] = (uchar)color[0];
                    img[r][c][1] = (uchar)color[1];
                    img[r][c][2] = (uchar)color[2];
                }
            } else if (middle_col == 31 || middle_col == 32) { // since col is off by 1 the middle is technically at 31 and 32 (the variable) when it should be at 32 and 33
                if (color[0] == 0) {
                    img[r][c][0] = (uchar)255;
                    img[r][c][1] = (uchar)0;
                    img[r][c][2] = (uchar)0;
                } else {
                    img[r][c][0] = (uchar)color[0];
                    img[r][c][1] = (uchar)color[1];
                    img[r][c][2] = (uchar)color[2];
                }
            } else {
                img[r][c][0] = (uchar)color[0];
                img[r][c][1] = (uchar)color[1];
                img[r][c][2] = (uchar)color[2];
            }
            
            if ((c+1) % 10 == 0) {
                if (color[0] == 255) {
                    color[0] = 0;
                    color[1] = 255;
                    color[2] = 0;
                } else {
                    color[0] = 255;
                    color[1] = 255;
                    color[2] = 255;
                }
                middle_col++;
            }
        }
        if (r % 10 == 0 && r = 0) {
            if (color[0] == 255) {
                color[0] = 0;
                color[1] = 255;
                color[2] = 0;
            } else {
                color[0] = 255;
                color[1] = 255;
                color[2] = 255;
            }
            middle_row++;
        }
        middle_col = 0;
    }
    
    
    fout.open("greenred.ppm");
    
    fout << "P6" << endl;
    
    fout << "640 480" << endl << "255" << endl;
    
    for(r = 0; r < 480; r++) {
        for(c = 0; c < 640; c++) {
            fout << img[r][c][0] << img[r][c][1] << img[r][c][2] << flush;
        }
    }
    
    fout.close();
    
    return 0;
}
//
// end of file
//
