#Task 1
def count_freq(word):
    """
    This function takes in a parameter 'word' that is a string of length M.
    It then finds the number of times each alphabet occurs in the string.
    It returns an array that contains the frequency of each alphabet.
    Written by Cheryl Lau

    Precondition: word parameter is a string of characters
    Postcondition:an array that contains the frequency of each alphabet is returned

    Input:
        word: word input parameter from trainer function
    Return:
        count_array: an array that lists the frequency of each alphabet, where each index
        represents the ASCII value of its corresponding alphabet

    Time complexity: 
        Best: O(M + M) = O(M) where M is the length of word
        Worst: O(M + M) = O(M) where M is the length of word
    Space complexity: 
        Input: O(M) where M is the length of word
        Aux: O(K) where K is the largest alphabet's ASCII value

    """
    max_item = word[0]
    #find largest character
    for item in word:
        if ord(item) > ord(max_item):
            max_item = item
    #initiate count_array
    count_array = [0] * (ord(max_item) - 97 + 1)
    #update count_array
    for item in word:
        count_array[ord(item) -97] = count_array[ord(item)-97] + 1
    return count_array

def get_valid_words(wordlist,word):
    """
    This function eliminates strings that do not have the same alphabets as the guessed word
    Written by Cheryl Lau

    Precondition: word parameter is a string and wordlist is an array of strings
    Postcondition: a new list with strings of the same character with word is returned

    Input:
        wordlist: the input wordlist from trainer function
        word: the input word from trainer function
    Return:
        newlist: a list that does not have strings that does not have the same 
        alphabet as word

    Time complexity: 
        Best: O(N)
        Worst: O(NM)
        where M =length of word, N=length of wordlist
    Space complexity: 
        Input: O(NM + M) = O(NM)
        Aux: O(NM) 
        where N=length of wordlist, M= length of word

    """
    newlist = []
    #get frequency count of the characters in word
    word_freq = count_freq(word)
    #iterate through each string in wordlist and compare
    for i in range(len(wordlist)):
        item_freq = count_freq(wordlist[i])
        if len(item_freq) == len(word_freq):
            for j in range(len(word_freq)):
                if word_freq[j] != item_freq[j]:
                    break
                elif j == len(word_freq)-1:
                    newlist.append(wordlist[i])
                else:
                    continue
    return newlist

def get_ones_word(wordlist,char,index):
    """
    This function removes strings from wordlist that does not has
    the same character as char at the input parameter index
    Written by Cheryl Lau

    Precondition: word parameter is a string of characters
    Postcondition: list of words from wordlist where the character at index = char is returned

    Input:
        wordlist: input wordlist parameter from trainer function
        char: the character in the guessed word that is at the correct place
        index: the index of the character that is in the correct place
    Return:
        count_array: list of words from wordlist where the character at index = char

    Time complexity: 
        Best: O(N)
        Worst: O(N)
        where N =length of wordlist
    Space complexity: 
        Input: O(NM+1+1) = O(NM)
        where N = length of wordlist, M = length of string in wordlist
        Aux: O(N+K) = O(N)
        where N = the length of wordlist, K=length of alphabets from a-z

    """
    num_of_char = 26
    count_array = [None] * num_of_char
    #initialize count array
    for i in range(len(count_array)):
        count_array[i] = []
    #update count array by appending elements from wordlist
    for item in wordlist:
        count_array[ord(item[index])-97].append(item)
    return count_array[ord(char)-97]
    
def radix_sort(wordlist):
    """
    This function sorts the strings in wordlist in lexicographic order
    Written by Cheryl Lau

    Precondition: 
    -the length of each string in the wordlist must be fixed
    -wordlist must be made up of strings
    Postcondition:
    a sorted list is returned by function

    Input:
        wordlist: input wordlist parameter from trainer function
    Return:
        wordlist: input wordlist parameter from trainer function but sorted in lexicographic order

    Time complexity: 
        Best: O(1) when list is empty
        Worst: O(M) + O(M*(K+N)) = O(MK + MN) ~= O(MN) since K<=26
        where M = length of string (which is fixed), N=length of wordlist, K=largest character ASCII value
    Space complexity: 
        Input: O(MN)
        Aux: O(K+N) ~= O(N) since K <= 26
        where M=length of string in wordlist (fixed), N=length of wordlist, K = largest character's ASCII value

    """
    #if wordlist is empty, return itself
    if len(wordlist) == 0:
        return wordlist
    tmp = wordlist[0]
    max_chr = tmp[0]
    #find largest character in wordlist
    for chr in tmp:
        if ord(chr) > ord(max_chr):
            max_chr = chr
    #initiate count_arr
    count_arr = [None] * (ord(max_chr) + 1)
    #iterate through column and perform counting sort at each iteration
    for i in range(len(tmp)-1,-1,-1): 
        for j in range(len(count_arr)):
            count_arr[j] = []
        for j in range(len(wordlist)):
            count_arr[ord(wordlist[j][i])].append(wordlist[j])
        ind = 0
        for k in range(len(count_arr)):
            for item in count_arr[k]: 
                wordlist[ind] = item
                ind = ind + 1
    return wordlist

def trainer(wordlist,word,marker):
    """
    This finds strings that meet the criteria of marker and word
    Written by Cheryl Lau

    Precondition: word parameter is a string of characters and is not empty
    Postcondition: a list of strings that meets the word and marker criteria is returned

    Input:
        wordlist: an list of strings where each string has a length M
        word: a string of characters of length M
        marker: an array of 0 and 1 of length M
    Return:
        wordlist that is updated with the strings that meets the criteria

    Time complexity: 
        Best: O(NM)
        Worst: O(NM) + O(M) + O(XN) + O(NM) + O(NM) = O(NM) since X <= M
        where N= length of wordlist
        M = length of word and strings in wordlist
        X = number of 0s in marker
    Space complexity: 
        Input: O(NM + M + M) = O(NM)
        Aux: O(N+K) + O(M) + O(NM) + O(NM) + O(K+N) = O(NM)
        where N= length of wordlist
        M = length of word and strings in wordlist
        K = ASCII value of largest alphabet (<=26)

    """
    for i in range(len(word)):
        if marker[i] == 1:
            wordlist = get_ones_word(wordlist,word[i],i)
    #initialize a list of index that has value 0 in the marker
    zero_index_lst = []
    for i in range(len(marker)):
        if marker[i] == 0:
            zero_index_lst.append(i)
    #remove words that has same char as word when marker = 0
    for j in zero_index_lst: #O(X)
        newlist = []
        for i in range(len(wordlist)):
            if word[j] != wordlist[i][j]:
                newlist.append(wordlist[i])
        wordlist = newlist
    wordlist = get_valid_words(wordlist,word)
    return radix_sort(wordlist)

#Task 2
def find_max_col(arr,lft_col,rgt_col):
    """
    This function finds the index of the maximum value in a row,
    between the index lft_col and rgt_col (inclusive)
    Written by Cheryl Lau

    Precondition: arr is not an empty list
    Postcondition: an index of the max value in the array is returned

    Input:
        arr: row array 
        lft_col: starting index
        rgt_col: ending index
    Return:
        max_index: index of the max value in the row

    Time complexity: 
        Best: O(1) when lft_col - rgt_col = 0
        Worst: O(N) where N is the size of the matrix
    Space complexity: 
        Input: O(M) where M is the length of arr
        Aux: O(1)

    """
    max_index = lft_col
    for i in range(lft_col,rgt_col+1):
        if arr[i] > arr[max_index]:
            max_index = i
    return max_index

def find_max_nbr_row(M,mid_row,max_col):
    """
    This function compares the neighbouring row of an element in the matrix M
    and returns the row_index that has the largest element
    Written by Cheryl Lau

    Precondition: mid_row and max_col must be positive and is less than or equals to len(M)-1
    Postcondition: row index of the largest element when comapred with neighbouring value is returned

    Input:
        M: the input matrix
        mid_row: the row index of the value to be compared with its neighbours
        max_col: the column index of the value to be compared with its neighbours
    Return:
        cur_max_row: the row index of the largest value amoung the compared rows

    Time complexity: 
        Best: O(1)
        Worst: O(1)
    Space complexity: 
        Input: O(N^2) where N is the length of matrix M
        Aux: O(1)

    """
    #check if mid_row is at the edge of matrix M
    if len(M) == 1:
        return mid_row
    elif mid_row == 0:
        row_above = mid_row
        row_below = mid_row + 1
    elif mid_row == len(M)-1:
        row_below = mid_row
        row_above = mid_row-1
    else:
        row_above = mid_row-1
        row_below = mid_row+1
    cur_max_row = row_above
    for i in range(row_above,row_below+1):
        if M[i][max_col] > M[cur_max_row][max_col]:
            cur_max_row = i
    return cur_max_row

def find_max_row(M,col_index,top_row,bot_row):
    """
    This function finds the row index of the maximum value in a column,
    between the index top_row and bot_row
    Written by Cheryl Lau

    Precondition: M is not an empty matrix
    Postcondition: a row index of the max value in the column is returned

    Input:
        M: input matrix
        col_index: the column to find the maximum value
        top_row:the start of the column
        bot_row: the end of the column
    Return:
        max_index: index of the max value in the row

    Time complexity: 
        Best: O(1) when abs(lft_col - rgt_col) == 0
        Worst: O(N) where N is the size of the matrix
    Space complexity: 
        Input: O(N^2) where N is the length of M
        Aux: O(1)

    """
    max_row = top_row
    for i in range(top_row,bot_row+1):
        if M[i][col_index] > M[max_row][col_index]:
            max_row = i
    return max_row

def find_max_nbr_col(row_arr,col):
    """
    This function compares an element in an array with its left n right neighbour elements
    and returns the index of the element that is the largest among them
    Written by Cheryl Lau

    Precondition: row_arr must have at least 1 element
    Postcondition: column index of the largest value amoung the ones compared is returned

    Input:
        row_arr: a row from matrix M 
        col: the column index of the element that will be compared
    Return:
        cur_max_: the column index that has the largest value among the ones compared
        in this function

    Time complexity: 
        Best: O(1) 
        Worst: O(1)
    Space complexity: 
        Input: O(N) where N is the length of row_arr
        Aux: O(1)

    """
    #check if col is at the edge of matrix
    if len(row_arr) == 1:
        return col
    elif col == 0:
        start = col
        end = col + 2
    elif col == len(row_arr)-1:
        start = col -1
        end = col + 1
    else:
        start = col -1
        end = col + 2
    cur_max = start
    for i in range(start,end):
        if row_arr[i] > row_arr[cur_max]:
            cur_max = i
    return cur_max


def local_maximum(M):
    """
    This function finds any one local maximum that exists in matrix M
    site reference:http://courses.csail.mit.edu/6.006/spring11/lectures/lec02.pdf
    Written by Cheryl Lau

    Precondition: matrix M is n by n in size and has distinct elements, where n is >= 1
    Postcondition: one local maximum's coordinates is returned

    Input:
        M: a n by n matrix
    Return:
        an array with 2 elements, where the first element is the row index and the second is column index
        of any one of the local maximum in matrix M

    Time complexity: 
        Best: O(N) 
        Worst: O(N)
        where N is the length of the matrix
    Space complexity: 
        Input: O(N^2) where N is the length of the matrix
        Aux: O(1)

    """
    #initialize length of matrix, rows, columns indexes
    n = len(M)
    top_row = 0
    lft_col = 0
    bot_row = n-1
    rgt_col = n-1
    cur_max_col = 0
    cur_max_row = 0
    new_max_col = 0
    new_max_row = 0
    #slice matrix into 4 quarters at each iteration
    while top_row <= bot_row:
        #finds the global max at the 1st row, mid row and last row
        step = (bot_row-top_row)//2
        if step == 0:
            step = step + 1
        for i in range(top_row, bot_row+1, step):
            tmp_max_col = find_max_col(M[i], lft_col, rgt_col)
            if M[i][tmp_max_col] > M[cur_max_row][cur_max_col]:
                cur_max_row = i
                cur_max_col = tmp_max_col
        #finds the global max at the 1st col, mid col, last col,
        step = (rgt_col-lft_col)//2
        if step == 0:
            step = step + 1
        for j in range(lft_col, rgt_col+1, step):
            tmp_max_row = find_max_row(M, j, top_row, bot_row)
            if M[tmp_max_row][j] > M[cur_max_row][cur_max_col]:
                cur_max_col = j
                cur_max_row = tmp_max_row
        #check if its a local max
        new_max_row = find_max_nbr_row(M, cur_max_row, cur_max_col)
        new_max_col = find_max_nbr_col(M[cur_max_row], cur_max_col) 
        if new_max_col == cur_max_col and new_max_row == cur_max_row:
            return [cur_max_row, cur_max_col]
        else:
            #enter the quarter that the new max value is at and slice into 4 smaller quarters
            dst_up = abs(new_max_row - top_row)
            dst_bot = abs(new_max_row - bot_row)
            if dst_up > dst_bot:
                top_row = (top_row + bot_row)//2 + 1
            else:
                bot_row = (top_row + bot_row)//2 - 1
            dst_up = abs(new_max_col - lft_col)
            dst_bot = abs(new_max_col - rgt_col)
            if dst_up > dst_bot:
                lft_col = (lft_col + rgt_col)//2 + 1
            else:
                rgt_col = (lft_col + rgt_col)//2 - 1
