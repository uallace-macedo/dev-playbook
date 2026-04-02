#include <iostream>
using namespace std;

int main(){
  srand(time(NULL));
  
  int num = (rand() % 10);
  int num2 = (rand() % 20);
  int num3 = (rand() % 30);
  
  cout<<num<<"\n";
  cout<<num2<<"\n";
  cout<<num3<<"\n";

  return 0;
}