#include <iostream>
#include <ctime>
#include <cstdlib>
#include<fstream>
using namespace std;

int rand31(){
    // RAND31_MAX = 2147483647
    return ( (rand() << 16) | (rand() << 1) | (rand() & 1) );
}

int main() {

    
    unsigned before = clock();
    srand(time(NULL));
    static long numbers[1000000];
        char filename[]="text.txt";
    fstream fp;
    fp.open(filename, ios::out);//開啟檔案
    if(!fp){//如果開啟檔案失敗，fp為0；成功，fp為非0
        cout<<"Fail to open file: "<<filename<<endl;
    }
    cout<<"File Descriptor: "<<fp<<endl;
    for (int i = 0; i < 1000000; i++)
        numbers[i] = (rand31() % 1000000)+1;
    for (int i = 0; i < 1000000; i++)
        fp<<numbers[i]<<" ";//寫入字串
         cout<<clock() - before<<endl;
    fp.close();//關閉檔案
    system("pause");
    return EXIT_SUCCESS;
    return 0;
}
