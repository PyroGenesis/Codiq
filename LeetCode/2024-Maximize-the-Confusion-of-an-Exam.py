from collections import deque, Counter

class Solution:
    def maxConsecutiveAnswers(self, answerKey: str, k: int) -> int:
        # k==0 not in constraints
        n = len(answerKey)

        def maxConsecutiveLetter(letter: str) -> int:
            nonlocal answerKey, k, n

            i, j = 0, 0
            max_letter = 0
            changes_left = k
            
            while j < n:
                if answerKey[j] == letter:
                    pass
                elif changes_left > 0:
                    changes_left -= 1
                else:
                    while answerKey[i] == letter:
                        assert i < j, f'i should not exceed j when searching for (complementary of {letter}) to switch back to'
                        i += 1
                    i += 1
                    changes_left += 1
                
                j += 1
                window_len = j - i
                max_letter = max(max_letter, window_len)

            return max_letter

        return max(maxConsecutiveLetter('T'), maxConsecutiveLetter('F'))

