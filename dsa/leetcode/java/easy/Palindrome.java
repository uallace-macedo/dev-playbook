package java.easy;

/**
 * LeetCode #9: Palindrome Number
 * * Approach: Reversing the half or full integer mathematically.
 * Time Complexity: O(log10(n)) - We divide the input by 10 in every iteration.
 * Space Complexity: O(1) - We only use a few integer variables.
 * * Logic:
 * We use the modulo operator (%) to extract the last digit and division (/)
 * to remove it. By multiplying the 'reversedNumber' by 10 each time,
 * we "shift" the digits to the left to build the reversed version.
 */

public class Palindrome {

  public static boolean palindrome(int x) {
    if (x < 0)
      return false;
    if (x % 10 == 0 && x != 0)
      return false;

    int reversedNumber = 0;
    int temp = x;

    while (temp > 0) {
      int lastDigit = temp % 10;
      reversedNumber = reversedNumber * 10 + lastDigit;
      temp /= 10;
    }

    return reversedNumber == x;
  }

  public static void main(String[] args) {
    assert palindrome(121) == true : "Test Failed: 121 should be true";
    assert palindrome(-121) == false : "Test Failed: -121 should be false"; // Test Case 2: Negative number
    assert palindrome(10) == false : "Test Failed: 10 should be false"; // Test Case 3: Ending with zero
    assert palindrome(7) == true : "Test Failed: 7 should be true"; // Test Case 4: Single digit (always palindrome)
    assert palindrome(1234321) == true : "Test Failed: 1234321 should be true"; // Test Case 5: Large palindrome
    assert palindrome(0) == true : "Test Failed: 0 should be true"; // Test Case 6: Zero itself

    System.out.println("✅ All Palindrome tests passed!");
  }
}