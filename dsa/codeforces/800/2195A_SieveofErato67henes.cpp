#include <bits/stdc++.h>
using namespace std;

#define int long long
#define FAST_INPUT ios::sync_with_stdio(false); cin.tie(NULL)
#define endl "\n"
#define rep(n) for(int i=0;i<n;i++)

signed main() {
  FAST_INPUT;

  int n;
  cin>>n;

  rep(n) {
    int n2;
    if(!(cin>>n2)) break;

    bool s7 = false;
    rep(n2) {
      int a;
      if(!(cin>>a)) break;
      if(a==67)s7=true;
    }

    if(s7) {
      cout<<"YES" endl;
    } else {
      cout<<"NO" endl;
    }
  }
}