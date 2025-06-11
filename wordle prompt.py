from wip.wordle import propose_next_word

allDictionary = []
with open("data//wordle-allowed-guesses.txt") as f:
    for line in f:
        allDictionary.append(line.strip().lower())

currentGuess = input("What is your first guess?")

# List of 6 questions
questions = [
    "Share the feedback for first guess.",
    "Share the feedback for second guess.",
    "Share the feedback for third guess.",
    "Share the feedback for fourth guess.",
    "Share the feedback for fifth guess.",
    "Share the feedback for last guess."
]

all_guesses = {'steps': 1, 'guesses': []}

loop = 1
for q in questions:
    all_guesses['guesses'].append(currentGuess)
    currentResponse = input(q)
    if set(currentResponse) != {'g'}:
        next_word = propose_next_word(currentGuess, currentResponse, allDictionary)

        if (next_word is None) or (next_word['next_word_proposal'] is None):
            solved_in_steps = 0
            logger.info(
                "Could not solve despite {} {} guesses". \
                    format(loop, all_guesses['guesses']))
            break

        allDictionary = next_word['reduced_dictionary']
        currentGuess = next_word['next_word_proposal']
        loop = loop + 1
        print("The next word suggestion is:", currentGuess)
    else:
        print(
            "Solved {} in {} attempts. All attempts made {}". \
                format(currentGuess, loop, all_guesses['guesses']))
        break

# Print all answers
