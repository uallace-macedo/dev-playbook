package java.easy;
/**
* LeetCode #1: Two Sum
* * Approach: One-pass Hash Table
* Time Complexity: O(n) - We traverse the list containing n elements only once.
* Space Complexity: O(n) - The extra space required depends on the number of
* items stored in the map.
* * Logic:
* As we iterate, we calculate the 'complement' (target - current value).
* We check if this complement exists in our Map (which acts as our memory).
* If it exists, we have found the pair and return their indices.
* Otherwise, we store the current number and its index to be found by future
* iterations.
*/

import java.util.Map;
import java.util.HashMap;

public class TwoSum {
  public static int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();

    for (int i = 0; i < nums.length; i++) {
      int diff = target - nums[i];
      if (map.containsKey(diff)) {
        return new int[] { map.get(diff), i };
      }

      map.put(nums[i], i);
    }

    return new int[] {};
  }

  public static void main(String[] args) {
    int[] result1 = twoSum(new int[] { 2, 7, 11, 15 }, 9); // expected [0,1]
    assert result1[0] == 0 : "WRONG OUTPUT - RESULT1[0]";
    assert result1[1] == 1 : "WRONG OUTPUT - RESULT1[1]";

    int[] result2 = twoSum(new int[] { 3, 2, 4 }, 6); // expected [1,2]
    assert result2[0] == 1 : "WRONG OUTPUT - RESULT2[0]";
    assert result2[1] == 2 : "WRONG OUTPUT - RESULT2[1]";

    int[] result3 = twoSum(new int[] { 3, 3 }, 6); // expected [0,1]
    assert result3[0] == 0 : "WRONG OUTPUT - RESULT3[0]";
    assert result3[1] == 1 : "WRONG OUTPUT - RESULT3[1]";

    int[] result4 = twoSum(new int[] { -1, -3, -5, 10 }, -4); // real case - expected [0,1]
    assert result4[0] == 0 : "WRONG OUTPUT - RESULT4[0]";
    assert result4[1] == 1 : "WRONG OUTPUT - RESULT4[1]";

    System.out.println("✅ All tests passed!");
  }
}