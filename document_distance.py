# Purpose: Check for similarity between two texts by comparing different kinds of word statistics.

import string
import math


### DO NOT MODIFY THIS FUNCTION
def load_file(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        string, contains file contents
    """
    # print("Loading file %s" % filename)
    inFile = open(filename, 'r')
    line = inFile.read().strip()
    for char in string.punctuation:
        line = line.replace(char, "")
    inFile.close()
    return line.lower()


### Problem 0: Prep Data ###
def text_to_list(input_text):
    """
    Args:
        input_text: string representation of text from file.
                    assume the string is made of lowercase characters
    Returns:
        list representation of input_text, where each word is a different element in the list
    """
    return input_text.split()

### Problem 1: Get Frequency ###
def get_frequencies(input_iterable):
    """
    Args:
        input_iterable: a string or a list of strings, all are made of lowercase characters
    Returns:
        dictionary that maps string:int where each string
        is a letter or word in input_iterable and the corresponding int
        is the frequency of the letter or word in input_iterable
    Note: 
        You can assume that the only kinds of white space in the text documents we provide will be new lines or space(s) between words (i.e. there are no tabs)
    """
    frequencies = {}
    for i in range(len(input_iterable)):
        if input_iterable[i] not in frequencies:
            frequencies[input_iterable[i]] = 1
        else:
            frequencies[input_iterable[i]] += 1
    return frequencies


### Problem 2: Letter Frequencies ###
def get_letter_frequencies(word):
    """
    Args:
        word: word as a string
    Returns:
        dictionary that maps string:int where each string
        is a letter in word and the corresponding int
        is the frequency of the letter in word
    """
    # Initialization of an empty dict
    letter_frequencies = {}
    
    for i in range(len(word)):
        # If letter not in the dict, equalite to 1
        if word[i] not in letter_frequencies:
            letter_frequencies[word[i]] = 1
        # If it is, add up 1
        else:
            letter_frequencies[word[i]] += 1
    return letter_frequencies


### Problem 3: Similarity ###
def calculate_similarity_score(freq_dict1, freq_dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        freq_dict1: frequency dictionary of letters of word1 or words of text1
        freq_dict2: frequency dictionary of letters of word2 or words of text2
    Returns:
        float, a number between 0 and 1, inclusive
        representing how similar the words/texts are to each other

        The difference in words/text frequencies = DIFF sums words
        from these three scenarios:
        * If an element occurs in dict1 and dict2 then
          get the difference in frequencies
        * If an element occurs only in dict1 then take the
          frequency from dict1
        * If an element occurs only in dict2 then take the
          frequency from dict2
         The total frequencies = ALL is calculated by summing
         all frequencies in both dict1 and dict2.
        Return 1-(DIFF/ALL) rounded to 2 decimal places
    """
    # Check if the inputs are letters or words!
    
    # Initialization of delta and sigma values
    delta_diff = 0
    sigma_sum = 0
    
    # Combine keys of two dicts
    union_of_dicts = freq_dict1.keys() | freq_dict2.keys()
    
    #   Find delta_diff and sigma_sum by looping union of dicts
    # to get different values and summation of all values
    for element in union_of_dicts:
        
        # Get the frequency keys for both dicts, defaulting to 0
        freq1 = freq_dict1.get(element, 0)
        freq2 = freq_dict2.get(element, 0)
        
        delta_diff += abs(freq1 - freq2)
        sigma_sum  += freq1 + freq2

    # Integrate similarity formula and round by 2
    similarity = round(1 - (delta_diff/sigma_sum), 2)
    return similarity

### Problem 4: Most Frequent Word(s) ###
def get_most_frequent_words(freq_dict1, freq_dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        freq_dict1: frequency dictionary for one text
        freq_dict2: frequency dictionary for another text
    Returns:
        list of the most frequent word(s) in the input dictionaries

    The most frequent word:
        * is based on the combined word frequencies across both dictionaries.
          If a word occurs in both dictionaries, consider the sum the
          freqencies as the combined word frequency.
        * need not be in both dictionaries, i.e it can be exclusively in
          dict1, dict2, or shared by dict1 and dict2.
    If multiple words are tied (i.e. share the same highest frequency),
    return an alphabetically ordered list of all these words.
    """
    
    combined_dicts = {key: freq_dict1.get(key, 0) + freq_dict2.get(key, 0) for key in freq_dict1 | freq_dict2}
    
    # Find highest frequency by sorting dicts alphabetically or highest value
    dicts_sorted = list(sorted(combined_dicts.items(), key= lambda x: (-x[1], x[0])))
    
    # Take highest value as a reference
    highest_value = dicts_sorted[0][1]
    
    # Get most frequent word/s and return "key" as a list
    most_freq_words_of_dicts = [i[0] for i in dicts_sorted if i[1] == highest_value]
    
    
    return most_freq_words_of_dicts



### Problem 5: Finding TF-IDF ###
def get_tf(file_path):
    """
    Args:
        file_path: name of file in the form of a string
    Returns:
        a dictionary mapping each word to its TF

    * TF is calculatd as TF(i) = (number times word *i* appears
        in the document) / (total number of words in the document)
    * Think about how we can use get_frequencies from earlier
    """
    # Open file and read
    loaded_file = load_file(file_path)
    
    # Convert text to a list and get frequencies
    word_list = text_to_list(loaded_file)
    freqs = get_frequencies(word_list)
    
    # Get total number of words
    total_words = sum(freqs.values())
    
    # Get how many times a word appears (Term Frequency formula) and return 
    tf = {k: v / total_words for k, v in freqs.items()}

    return tf

def get_idf(file_paths):
    """
    Args:
        file_paths: list of names of files, where each file name is a string
    Returns:
       a dictionary mapping each word to its IDF

    * IDF is calculated as IDF(i) = log_10(total number of documents / number of
    documents with word *i* in it), where log_10 is log base 10 and can be called
    with math.log10()

    """
    # Initialization of main dict
    idf_dict = {}
    
    # Find total number of documents
    total_documents = len(file_paths)
    
    # Open files, read and append to words_list
    for each_file in file_paths:
        texts = load_file(each_file)
        words_list = text_to_list(texts)
        word_freqs = get_frequencies(words_list)
    
    # Take every word in IDF dict
        for word in word_freqs:
            if word in idf_dict:
                idf_dict[word] += 1
            else:
                idf_dict[word] = 1
    
    # Calculate IDF formula
    for word in idf_dict:
        idf_dict[word] = math.log10(total_documents / idf_dict[word])
        
    return idf_dict
    
    
def get_tfidf(tf_file_path, idf_file_paths):
    """
        Args:
            tf_file_path: name of file in the form of a string (used to calculate TF)
            idf_file_paths: list of names of files, where each file name is a string
            (used to calculate IDF)
        Returns:
           a sorted list of tuples (in increasing TF-IDF score), where each tuple is
           of the form (word, TF-IDF). In case of words with the same TF-IDF, the
           words should be sorted in increasing alphabetical order.

        * TF-IDF(i) = TF(i) * IDF(i)
        """
    # Use previous specified functions to get arguments correctly
    tf = get_tf(tf_file_path)
    idf = get_idf(idf_file_paths)
    
    # Calculate TD-IDF formula
    tf_idf = [(word, tf[word] * idf[word])for word in tf if word in idf]
    
    # Return TD-IDF, in alphabetical or in increasing order
    return sorted(tf_idf, key= lambda x: (x[1], x[0]))

