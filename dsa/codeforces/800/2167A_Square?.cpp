#include <bits/stdc++.h>
using namespace std;

#define int long long
#define FAST_INPUT ios::sync_with_stdio(false); cin.tie(NULL)
#define endl << "\n"
#define rep(n) for(int i=0;i<n;i++)
#define YES cout<<"YES" endl
#define NO cout<<"NO" endl

signed main() {
  FAST_INPUT;

  int n;
  cin>>n;

  rep(n) {
    int a,b,c,d;
    if (!(cin>>a>>b>>c>>d)) break;

    if ((a != b || a != c || a != d) || (a == 0)) {
      NO;
      continue;
    }

    YES;
  }

  return 0;
}