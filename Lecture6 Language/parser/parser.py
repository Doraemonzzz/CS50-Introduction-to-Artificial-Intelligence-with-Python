import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

#参考https://github.com/nahueespinosa/ai50/blob/master/parser/parser.py
NONTERMINALS = """
S -> NP VP | S Conj S | NP VP Conj VP
AP -> Adj | Adj AP
NP -> N | Det NP | AP NP | NP PP
PP -> P NP | P S
VP -> V | V NP | V NP PP | V PP | VP Adv | Adv VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

def judge(word):
    flag = False
    for s in word:
        if s.isalpha():
            flag = True
            break
    
    return flag

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.wordpunct_tokenize(sentence)
    res = []
    for word in words:
        word_lower = word.lower()
        if judge(word_lower):
            res.append(word_lower)
    
    return res

def np_chunk_helper(tree, List):
    if tree == None:
        return
    #计算NP的数量
    cnt = 0
    tmp = []
    for t in tree.subtrees():
        if t.label() == "NP":
            tmp.append(t)
            cnt += 1
    #如果只有1个NP则更新
    if cnt == 1:
        t = tmp[0]
        #防止重复
        if t not in List:
            List.append(t)
        return
    elif cnt > 1:
        for t in tree.subtrees():
            #排除自己
            if t != tree:
                np_chunk_helper(t, List)
    
        return
    
    return

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    List = []
    np_chunk_helper(tree, List)
    
    return List


if __name__ == "__main__":
    main()
