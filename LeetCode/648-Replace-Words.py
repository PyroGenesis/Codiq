from typing import List

from .CustomStructures import Trie

# custom class to add a function for this problem
class DerivativeFinderTrie(Trie):
    def get_derivative(self, word: str):
        '''Gets the shortest prefix for word which is a valid entry'''
        derivative = []
        node = self.root
        for ch in word:
            if ch not in node.children:
                # this prefix reached is not present in trie
                return word
            derivative.append(ch)
            node = node.children[ch]
            # need to check if prefix reached is a valid complete root
            if node.end:
                return ''.join(derivative)
        # root == word or root is a prefix of word
        return word


class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        return self.replaceWordsTrieSoln(dictionary, sentence)
    

    '''
    Trie solution:
        A trie is perfect for finding a word from a set of words.
            We do need an extension to the basic trie so that it returns
                either the smallest prefix of the valid shich is a valid entry OR
                otherwise the word itself
        We add all the words from the dictionary to this trie
        Every sentence word is then put through the trie. Our extended fn will give us the correct result.

        Let d -> number of dictionary words (roots)
            s -> number of sentence words
            w -> length of largest / average word
        
        Time:  O(d*w + s*w)
            creating dictionary trie:               O(d*w)
            splitting / merging words:              O(s*w)
            get_derivative for every sentence word: O(s*w)
                Iterating over every sentence word:     O(s)
                Putting the word through the trie:      O(w)
        
        Space: O(d*w + s*w)
            Dictionary trie:        O(d*w)
                d*w is worst case if there are no common prefix between any of the roots
                otherwise it will be lower
            split sentence words:   O(s*w)
    '''
    def replaceWordsTrieSoln(self, dictionary: List[str], sentence: str) -> str:
        # create and populate the trie
        trie = DerivativeFinderTrie()
        for root in dictionary:
            trie.insert(root)
        
        # split the sentence into words
        # get the derivative root for every word
        # merge them back into a sentence
        return ' '.join(trie.get_derivative(word) for word in sentence.split(' '))
    
    '''
    Simple (but bad) solution:
        The idea is to keep the roots in a set
        Then for every word in the sentence, you get every prefix subset and see if it matches any of the roots

        Let d -> number of dictionary words (roots)
            s -> number of sentence words
            w -> length of largest / average word
        
        Time:  O(d*w + s*(w^2))
            creating dictionary set:                O(d*w)
            splitting / merging words:              O(s*w)
            get_derivative for every sentence word: O(s * w^2)
                Iterating over every sentence word:     O(s)
                iterating from 1 to len(w):             O(w)
                creating subset:                        O(w)
                checking hashset:                       O(1)
        
        Space: O(d*w + s*w)
            Dictionary set:         O(d*w)
                It will always d*w in any case
            split sentence words:   O(s*w)
            temporary prefixes:     O(w)
    '''
    def replaceWordsHashsetSoln(self, dictionary: List[str], sentence: str) -> str:
        # create a set of all the dictionary words
        dictionary_set = set(dictionary)

        # helper fn
        def get_derivative(word: str):
            nonlocal dictionary_set
            
            # loop through every possible prefix subset
            # skip the 0-length and full-length prefixes
            for i in range(1, len(word)):
                # create the prefix subset
                subset = word[:i]
                # check if the subset is a root
                if subset in dictionary_set:
                    return subset
            # didn't find a root
            return word
        
        # split the sentence into words
        # get the derivative root for every word
        # merge them back into a sentence
        return ' '.join(get_derivative(word) for word in sentence.split(' '))
    
    '''
    Skipped:
        Brute-force solution
            Terrible and would have a massive time complexity
    '''
