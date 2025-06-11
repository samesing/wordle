import logging

import numpy as np

RESPONSE_GREEN = 'g'
RESPONSE_YELLOW = 'y'
RESPONSE_GRAY = 'x'

def check(guess, answer):
    response = [None] * 5
    if((guess is not None) and (answer is not None)):
        if guess == answer:
            response = np.repeat(RESPONSE_GREEN, 5)
        else:
            guessly = list(guess)
            answerly = list(answer)

            #print("Provided Answer is", answer)
            #print("Current Guess is", guess)

            response = [RESPONSE_GREEN if (i == j) else RESPONSE_GRAY for i, j in zip(guessly, answerly)]
            remaining = [i for i, j in zip(answerly, response) if (j == RESPONSE_GRAY)]

            for thisI, thisR in enumerate(response):
                if thisR != RESPONSE_GREEN:
                    toMatch = guessly[thisI]
                    # print("trying to match {} at position {} with remaining {}".format(toMatch, thisI, remaining))
                    if toMatch in remaining:
                        response[thisI] = RESPONSE_YELLOW
                        remaining.remove(toMatch)
                    else:
                        response[thisI] = RESPONSE_GRAY

    return response


def propose_next_word(currentGuess, responseCurrentGuess, remainingDictionary):
    #logger = logging.getLogger("wordle")
    #logger.info(f"Current Guess Word is {currentGuess}")
    #logger.info("Response for matching {}' is {}".format(currentGuess, responseCurrentGuess))

    likeliest = []

    if (currentGuess is not None) and (responseCurrentGuess is not None) and (remainingDictionary is not None):
        should = [j for i, j in zip(responseCurrentGuess, list(currentGuess)) if ((i == RESPONSE_YELLOW) or (i == RESPONSE_GREEN))]
        #print("Characters to include", should)
        should = set(should)

        prevent = [j for i, j in zip(responseCurrentGuess, list(currentGuess)) if ((i == RESPONSE_GRAY) and (j not in should))]
        #print("Characters to avoid", prevent)

        minCountChars = {}
        for x in [j for i, j in zip(responseCurrentGuess, list(currentGuess)) if (i != RESPONSE_GRAY) ]:
            minCountChars[x] = minCountChars.get(x, 0) + 1
        #print(minCountChars)
        if remainingDictionary is not None:
            for thisWord in remainingDictionary:
                matching = should.issubset(set(thisWord))
                if matching and (not any(t in thisWord for t in prevent)):
                    if (all(i == j for i, j, k in zip(currentGuess, thisWord, responseCurrentGuess) if (k == RESPONSE_GREEN)))\
                            and (all(i != j for i, j, k in zip(currentGuess, thisWord, responseCurrentGuess) if (
                            (k == RESPONSE_GRAY) or (k == RESPONSE_YELLOW)))):
                        totalMatch = True
                        #print("Matching Word is", thisWord)
                        for x in set(thisWord):
                           if (x in minCountChars) and (minCountChars[x] > thisWord.count(x)):
                               totalMatch = False
                        if totalMatch:
                            likeliest.append(thisWord)

    #print(len(likeliest))
    #print(likeliest)

    if len(likeliest) == 0:
        return {
            'next_word_proposal': None,
            'reduced_dictionary': None
        }
    elif len(likeliest) == 1:
        return {
            'next_word_proposal': likeliest[0],
            'reduced_dictionary': None
        }
    else:
        others = {}
        for likely in likeliest:
            others[likely] = set(likely) - should

        #print(others)
        sortedSet = {}
        for index, other in others.items():
            for option in other:
                sortedSet[option] = sortedSet.get(option, 1) + 1

        #print(sortedSet)
        # sortedSet = sorted(sortedSet.items(), key=lambda x: x[1], reverse=True)
        # print(sortedSet)

        finalists = {}
        for check, checkers in others.items():
            frequency = 1
            for checker in checkers:
                frequency *= sortedSet[checker]

            finalists[check] = frequency
            #print("frequency for {} is {}".format(checkers, frequency))

        finalists = sorted(finalists.items(), key=lambda x: x[1], reverse=True)
        #print(finalists)

        reducedDict = likeliest

        return {
            'next_word_proposal': finalists[0][0],
            'reduced_dictionary': reducedDict
        }
