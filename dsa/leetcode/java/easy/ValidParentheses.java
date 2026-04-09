package java.easy;

import java.util.Map;
import java.util.Stack;

/**
 * LeetCode #20: Valid Parentheses
 * Approach: Using a Stack to ensure Last-In-First-Out (LIFO) order.
 * Time Complexity: O(n) - We traverse the string exactly once.
 * Space Complexity: O(n) - In the worst case (e.g., "((((("), we store all
 * characters in the stack.
 */

public class ValidParentheses {
  public static boolean validParenthesesV1(String s) { // 4ms
    if (s.length() == 1) {
      return false;
    }

    if (")]}".indexOf(s.charAt(0)) != -1) {
      return false;
    }

    Map<Character, Character> corresponds = Map.of(
        ')', '(',
        ']', '[',
        '}', '{');

    Stack<Character> st = new Stack<>();

    for (int i = 0; i < s.length(); i++) {
      char c = s.charAt(i);
      if ("([{".indexOf(c) != -1) {
        st.push(c);
        continue;
      }

      if (st.isEmpty() || st.pop() != corresponds.get(c)) {
        return false;
      }
    }

    return st.isEmpty();
  }

  public static boolean validParenthesesV2(String s) { // 1ms
    char[] st = new char[s.length()];
    int top = -1;

    for (char c : s.toCharArray()) {
      if (c == '(' || c == '[' || c == '{') {
        st[++top] = c;
        continue;
      }

      if (top == -1)
        return false;
      char last = st[top--];

      if (last == '(' && c != ')')
        return false;
      if (last == '[' && c != ']')
        return false;
      if (last == '{' && c != '}')
        return false;
    }

    return top == -1;
  }

  public static void main(String[] args) {
    assert validParenthesesV2("()") == true : "Test Failed: ()"; // Test Case 1: Simple valid
    assert validParenthesesV2("()[]{}") == true : "Test Failed: ()[]{}"; // Test Case 2: Different types
    assert validParenthesesV2("(]") == false : "Test Failed: (]"; // Test Case 3: Invalid order
    assert validParenthesesV2("(((([{}{}]))))") == true : "Test Failed: Nested brackets"; // Test Case 4: Nested
    assert validParenthesesV2("]") == false : "Test Failed: Single closing"; // Test Case 5: Single closing
    assert validParenthesesV2("((") == false : "Test Failed: Unclosed openers"; // Test Case 6: Unclosed openers

    System.out.println("✅ All Valid Parentheses tests passed!");
  }
}