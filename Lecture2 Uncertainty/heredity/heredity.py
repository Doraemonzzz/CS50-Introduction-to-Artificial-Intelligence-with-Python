import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

#原本为i个gene，生成j个gene的概率
#i=0,1,2, j=0,1
def get_prob(i, j):
    if j != 0 and j != 1:
        return 0
    p = PROBS["mutation"]
    if i == 0:
        p1 = 1 - p
        if j == 0:
            return p1
        else:
            return 1 - p1
    elif i == 1:
        p1 = 0.5 * (1 - p) + 0.5 * p
        if j == 0:
            return p1
        else:
            return 1 - p1
    else:
        p1 = p
        if j == 0:
            return p1
        else:
            return 1- p1
        
def get_num(people, one_gene, two_genes, person):
    zero_gene = set(people.keys()) - one_gene - two_genes
    if person in zero_gene:
        return 0
    elif person in one_gene:
        return 1
    else:
        return 2
            

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    prob = 1
    
    for person in people:
        #计算数量
        n1 = get_num(people, one_gene, two_genes, person)
        #trait
        p = PROBS["trait"][n1][True]
        if person not in have_trait:
            p = 1 - p
        prob *= p
        #没有父节点
        if people[person]['mother'] == None:
            prob *= PROBS["gene"][n1]
        else:
            father = people[person]['father']
            mother = people[person]['mother']
            n2 = get_num(people, one_gene, two_genes, father)
            n3 = get_num(people, one_gene, two_genes, mother)
            p1 = 0
            #穷举所有情况
            for i in range(n1 + 1):
                j = n1 - i
                p1 += get_prob(n2, i) * get_prob(n3, j)
            prob *= p1
        
    return prob
            

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        n = get_num(probabilities, one_gene, two_genes, person)
        probabilities[person]["gene"][n] += p
        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        s = 0
        for i in probabilities[person]["gene"]:
            s += probabilities[person]["gene"][i]
        for i in probabilities[person]["gene"]:
            probabilities[person]["gene"][i] /= s
        
        s = 0
        for i in probabilities[person]["trait"]:
            s += probabilities[person]["trait"][i]
        for i in probabilities[person]["trait"]:
            probabilities[person]["trait"][i] /= s


if __name__ == "__main__":
    main()
