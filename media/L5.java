import java.util.Arrays;

class Solution {
    static int total = 0;

    // BACKTRACKING + RECURSION
    static void findDistinct(String s, int indexS, StringBuilder currentString, String target) {
        // Base Case
        if (indexS >= s.length()) {
            if (currentString.toString().equals(target)) {
                total++;
                return;
            } else {
                return;
            }
        }

        // Take Case
        currentString.append(s.charAt(indexS));
        findDistinct(s, indexS + 1, currentString, target);
        currentString.deleteCharAt(currentString.length() - 1);

        // Non-take Case
        findDistinct(s, indexS + 1, currentString, target);
    }

    // DP + Memoization
    static int countDistinct(String s, int indexS, String target, int indexT, int[][] memo) {
        // Base Case
        if (indexT >= target.length())
            return 1;
        if (indexS >= s.length())
            return 0;

        // Step 2: If already calculated, just return it
        if (memo[indexS][indexT] != -1) {
            return memo[indexS][indexT];
        }

        // Step 3: If not calculated, calculate it and then return it
        int take = 0;
        int nonTake = 0;
        // Case when characters are equal, we take it
        if (s.charAt(indexS) == target.charAt(indexT)) {
            take = countDistinct(s, indexS + 1, target, indexT + 1, memo);
            nonTake = countDistinct(s, indexS + 1, target, indexT, memo);
            return memo[indexS][indexT] = take + nonTake;
        }

        // Case when characters aren't equal
        return memo[indexS][indexT] = countDistinct(s, indexS + 1, target, indexT, memo);
    }
}
