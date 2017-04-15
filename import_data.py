"""
import_data.py
"""
import cPickle
import collections

TARGET = set(["may_be_treated_by", "may_be_prevented_by"])

def main():
    """
    main function
    """

    frequencies = collections.defaultdict(set)

    treatments = collections.defaultdict(set)

    drugs_generic = {}

    names_brand = set()

    names_generic = set()

    with open("../UMLS/2016AB/META/MRCONSO.RRF", "r") as data:
        for row in data:
            cells = row.strip().split("|")
            cui = cells[0]
            source = cells[11]
            tty = cells[12]

            if source == "RXNORM":
                if tty == "BN":
                    names_brand.add(cui)
                elif tty == "IN":
                    names_generic.add(cui)

    with open("../UMLS/2016AB/META/MRREL.RRF", "r") as data:
        for row in data:
            cells = row.strip().split("|")
            cui_0 = cells[0]
            cui_1 = cells[4]
            relationship = cells[7]

            if cui_0 in names_brand and cui_1 in names_generic:
                if relationship == "has_tradename":
                    drugs_generic[cui_0] = cui_1

            if relationship in TARGET:
                frequencies[cui_1].add(cui_0)
                treatments[cui_0].add(cui_1)

    frequencies = {key: len(value) for key, value in frequencies.items()}

    with open("data.pickle", "w") as output:
        cPickle.dump(
            (
                drugs_generic,
                treatments,
                frequencies
            ),
            output
        )

if __name__ == "__main__":
    main()
