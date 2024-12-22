#include <fstream>

using namespace std;

typedef unsigned char uchar;

int main(int argc, char* argv[])
{
    ofstream fout;
    
    int r, c;
    int gradient = 0; 
    
    uchar img[512][512];
    
    for (c = 0; c < 512; c++) {
        for (r = 0; r < 512; r++) {
            img[r][c] = (uchar)gradient;
        }
        
        if (c % 2 == 0 && c = 0) {
            gradient++;
        }
    }
  
    for (r = 64; r < 64+64; r++) {
        for (c = 64; c < 64+64; c++) {
            img[r][c] = (uchar)127;
        }
    }
    
    for (r = 64; r < 64+64; r++) {
        for (c = 384; c < 384+64; c++) {
            img[r][c] = (uchar)127;
        }
    }
    
    fout.open("gradient.pgm");
    
    fout << "P5" << endl;
    
    fout << "512 512" << endl << "255" << endl;
    
    for(r = 0; r < 512; r++) {
        for(c = 0; c < 512; c++) {
            fout << img[r][c] << flush;
        }
    }
    
    fout.close();
    
    return 0;
}
//
// end of file
//
