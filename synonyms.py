import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

def cosine_similarity(vec1, vec2):
# This function returns the cosine similarity between the sparse vectors vec1 and vec2, stored as dictionaries.
# For example,
# cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6})
# should return approximately 0.70 (as a float)

    dot_prod = 0
    sum_of_squares1 = 0
    sum_of_squares2 = 0

# Calculate Dot Product
    for word, occurence in vec1.items():
        if word in vec2:
            dot_prod += occurence * vec2[word]

# Calculate Magnitude of Each Vector
    for component in vec1:
        sum_of_squares1 += vec1[component]**2

    vec1_mag = math.sqrt(sum_of_squares1)

    for component in vec2:
        sum_of_squares2 += vec2[component]**2

    vec2_mag = math.sqrt(sum_of_squares2)

# Calculate Cosine Similarity
    cos_sim = dot_prod/(vec1_mag*vec2_mag)

    return cos_sim

def build_semantic_descriptors(sentences):
    # Initialize the semantic descriptors dictionary
    semantic_descriptors = {}

    # Iterate over each sentence
    for sentence in sentences:
        # Initialize an empty list to track unique words in the sentence
        distinct_words = []

        # Iterate over the words in the sentence
        for word in sentence:
            # Only add the word if it's not already in distinct_words
            if word not in distinct_words:
                distinct_words.append(word)

        # Update co-occurrence counts for each word
        for word in distinct_words:
            if word not in semantic_descriptors:
                semantic_descriptors[word] = {}

            for co_word in distinct_words:
                if word != co_word:  # Skip self-co-occurrences

                    if co_word in semantic_descriptors[word]:
                        semantic_descriptors[word][co_word] += 1

                    else:
                        semantic_descriptors[word][co_word] = 1

    return semantic_descriptors

def build_semantic_descriptors_from_files(filenames):
    punc_to_replace = [",", "-", "--", ":", ";"]
    all_strings = []
    cur_sentence = ""
    all_sentences = []

    for i in range(len(filenames)):
        f = open(filenames[i], "r", encoding="latin1")
        text = f.read()
        text = text.lower()
        for punc in punc_to_replace:
            text = text.replace(punc, " ")

        for char in text:
            if char != "." and char != "!" and char != "?":
                cur_sentence += char
            else:
                all_strings.append(cur_sentence)
                cur_sentence = ""
        if cur_sentence.strip():
            all_strings.append(cur_sentence.strip())

        for sentence in all_strings:
            sent_to_add = sentence.split()
            all_sentences.append(sent_to_add)

        # Reset all_strings for the next file to avoid overlapping content
        all_strings = []

    return build_semantic_descriptors(all_sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):

    most_sim = choices[0]
    highest_sim = -3
    all_sims = {}

    for choice in choices:
        if word in semantic_descriptors and choice in semantic_descriptors:
            all_sims[choice] = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])

        else:
             all_sims[choice] = -1

    for key, value in all_sims.items():
        if value > highest_sim:
            highest_sim = value
            most_sim = key

    return most_sim

def run_similarity_test(filename, semantic_descriptors, similarity_fn):

    score = 0
    num_questions = 0

    f = open(filename, "r", encoding="latin1")
    for line in f:
        question = line.split()
        word = question[0]
        actual_ans = question[1]
        choices = question[2:]

        computer_ans = most_similar_word(word, choices, semantic_descriptors, similarity_fn)

        if computer_ans == actual_ans:
            score += 1

        num_questions += 1

    if num_questions > 0:
        percent = (score/num_questions) * 100.0

    else:
        percent = 0.0

    return percent

if __name__ == "__main__":

#     vec1 = {"a": 1, "b": 2, "c": 3}
#     vec2 = {"b": 4, "c": 5, "d": 6}
#     print(cosine_similarity(vec1, vec2))
#
#     sentences = [["i", "am", "a", "sick", "man"],
# ["i", "am", "a", "spiteful", "man"],
# ["i", "am", "an", "unattractive", "man"],
# ["i", "believe", "my", "liver", "is", "diseased"],
# ["however", "i", "know", "nothing", "at", "all", "about", "my",
# "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
#
#     print(build_semantic_descriptors(sentences))
    print(build_semantic_descriptors_from_files(filenames))