from typing import List

from collections import Counter, defaultdict


class Solution:
    """
    Strat: reduce all words in B to the smallest superword which is a superset for all B.
    Then if A[i] is a superset of superword, it will also be a superset of all B
    Although B[:] may have many required letters, as long as we fulfill the most demanding requirement, we won't need to worry about the other cases.

    x -> all letters in A
    y -> all letters in B
    Time:  O(x + y)
        We go through every letter once
    Space: O(x)
        The hashmaps, arrays and counters are all O(26) = O(1)
        The ans can be O(x)
    """

    def wordSubsets(self, A: List[str], B: List[str]) -> List[str]:
        return self.wordSubsetsBuiltin(A, B)

    def wordSubsetsBuiltin(self, A: List[str], B: List[str]) -> List[str]:
        """
        The builtin operations available in Counter lend very well to this problem.
        Normally, dictA | dictB replaces common values in dictA with values in dictB.
        From documentation, this is different for Counter objects:

        (snippet)
        Several mathematical operations are provided for combining Counter objects to produce multisets (counters that have counts greater than zero).
        Intersection and union return the minimum and maximum of corresponding counts.
        Equality and inclusion compare corresponding counts.
        Each operation can accept inputs with signed counts, but the output will exclude results with counts of zero or less.

        Example:
        >>> c = Counter(a=3, b=1)
        >>> d = Counter(a=1, b=2)
        >>> c & d                       # intersection:  min(c[x], d[x])
        Counter({'a': 1, 'b': 1})
        >>> c | d                       # union:  max(c[x], d[x])
        Counter({'a': 3, 'b': 2})
        >>> c <= d                      # inclusion:  c[x] <= d[x]
        False
        """
        # freq of B-superword
        Bdict = Counter()
        # reduce all words in B to the smallest superword which is a superset for all B
        for Bword in B:
            Bdict |= Counter(Bword)

        # Now A[i] is valid if Counter(A[i]) is a superset of or equal to Counter(superword)
        return [Aword for Aword in A if Bdict <= Counter(Aword)]

    def wordSubsetsArray(self, A: List[str], B: List[str]) -> List[str]:
        """Performing the strat using array, to potentially reduce the time complexity coefficient"""

        def getWordFreqArr(word):
            wordArr = [0] * 26
            for ch in word:
                wordArr[ord(ch) - ord("a")] += 1
            return wordArr

        def makeSuperset(arr1, arr2):
            for i in range(26):
                arr1[i] = max(arr1[i], arr2[i])

        # freq of B-superword
        BMaxArr = [0] * 26
        # reduce all words in B to the smallest superword which is a superset for all B
        for Bword in B:
            makeSuperset(BMaxArr, getWordFreqArr(Bword))

        # find the universal words
        universal_words = []
        for Aword in A:
            # freq of A-word
            AArr = getWordFreqArr(Aword)
            if all(AArr[i] >= BMaxArr[i] for i in range(26)):
                # checking all Bword letters was a success
                universal_words.append(Aword)

        return universal_words

    def wordSubsetsHashmap(self, A: List[str], B: List[str]) -> List[str]:
        """Performing the strat using hashmaps"""

        # freq of all A-words
        Adict = {word: Counter(word) for word in A}
        # freq of B-superword
        Bdict = defaultdict(int)

        # reduce all words in B to the smallest superword which is a superset for all B
        for Bword in B:
            Bwdict = Counter(Bword)
            for ch, count in Bwdict.items():
                Bdict[ch] = max(Bdict[ch], Bwdict[ch])

        # find the universal words
        universal_words = []
        for Aword, Awdict in Adict.items():
            for Bch, Bcount in Bdict.items():
                if Bch not in Awdict or Awdict[Bch] < Bcount:
                    break
            else:
                # checking all Bword letters was a success
                universal_words.append(Aword)

        return universal_words
