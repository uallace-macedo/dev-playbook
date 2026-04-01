#include <bits/stdc++.h>
using namespace std;

#define int long long
#define FAST_INPUT ios::sync_with_stdio(false); cin.tie(NULL)
#define endl << "\n"

signed main() {
  FAST_INPUT;

  int n;
  cin>>n;

  for (int i=0; i<n; i++) {
    int opt = 0;
    string s;
    cin>>s;

    if(s[0] == 'u') opt++; s[0] == 's';
    if(s[s.size()-1] == 'u') opt++; s[s.size()-1] = 's';

    for(int j=2; j<s.size()-1; j++) {
      if(s[j-1] == 'u' && s[j] != 's') {
        s[j] = 's'; opt++; j++;
      }
    }

    cout<<opt endl;
  }

  return 0;
}