#include <bits/stdc++.h>
using namespace std;

#define FAST_INPUT ios::sync_with_stdio(false); cin.tie(NULL)
#define rep(t) for(int i=0;i<t;i++)
#define YES cout<<"YES\n"
#define NO cout<<"NO\n"
#define int long long

signed main() {
    FAST_INPUT;
    int n,n2,k,a,sum;
    
    cin>>n;
    rep(n) {
        cin>>n2>>k;
        sum=0;
        rep(n2) {
            cin>>a;
            sum+=a;
        }
        
        if(sum % 2 != 0) {
            YES;
        } else {
            if((k*n2-1) % 2 != 0) {
                YES;
            } else {
                NO;
            }
        }
    }
}