#include <bits/stdc++.h>
using namespace std;

#define endl "\n"

class Solution {
  public:
    int findJudge(int n, vector<vector<int>>& trust) {
      vector<int> pj(n,0);
      vector<int> t(n,0);

      for(const auto& c : trust) {
        int tr = c[0];
        int cf = c[1];

        pj[tr-1] = 1;
        t[cf-1]++;
      }

      for(int i=0; i<n; i++) {
        if(pj[i] == 0 && t[i] == n - 1) return i+1;
      }

      return -1;
    }
};

int main() {
  Solution sol;

  int n1 = 2;
  vector<vector<int>> trust1 = {{1,2}};
  cout << "Test 1: " << sol.findJudge(n1, trust1) << " (Waited 2)" << endl;

  int n2 = 3;
  vector<vector<int>> trust2 = {{1, 3}, {2, 3}};
  cout << "Test 2: " << sol.findJudge(n2, trust2) << " (Waited: 3)" << endl;

  int n3 = 3;
  vector<vector<int>> trust3 = {{1, 3}, {2, 3}, {3, 1}};
  cout << "Test 3: " << sol.findJudge(n3, trust3) << " (Waited: -1)" << endl;

  return 0;
}