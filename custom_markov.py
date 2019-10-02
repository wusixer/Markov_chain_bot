import random

def markov(messages):
    word_dict = {}
    start_word = set()
    end_words = set()

    for message in messages:
        message = message.lower()
        words = message.split(' ')
        # start word and end word only count if the sentence contains more than 1 word
        if (len(words) > 1):
            start_word.add(words[0])
            end_words.add(words[-1])
        # loop through the current word
        for word_index in range(len(words)-1):
            word = words[word_index]
            # create a nested dictionary of each current word, for each word, record 
            # the possible next word and the occurances of the next word
            if word not in word_dict:
                word_dict[word] = {}
                next_word = words[word_index + 1]
                if next_word not in word_dict[word]:
                    word_dict[word][next_word] = 0
                word_dict[word][next_word] += 1

    for word in start_word:
        if word in end_words:
            end_words.remove(word)

    # randomly choose a word from a pile of start word as the start word
    cur_word = random.choice(list(start_word))
    answer = []
    answer.append(cur_word)

    # pick the next word if the length of sentence is less than a range 
    while(cur_word not in end_words):
        words = word_dict[cur_word]
        if len(words.keys()) == 0 or len(answer) > 200:
            break

        cur_word = None
        total_freq = sum(words.values())
        # pick the a list of next words using their frequency of ocuurance of the previous word
        # randomly pick one word 
        while cur_word is None:
            cur_words = []
            for word, freq in iter(words.items()):
                per = freq / total_freq
                if random.random() <= per:
                    cur_words.append(word)
            cur_word = random.choice(cur_words)
        answer.append(cur_word)
    return ' '.join(answer)
