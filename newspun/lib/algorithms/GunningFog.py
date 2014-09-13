import sys

verbose = False

#countsyl by shallowsky, with some editing

#!//usr/bin/env python

# Count syllables in a word.
#
# Doesn't use any fancy knowledge, just a few super simple rules:
# a vowel starts each syllable;
# a doubled vowel doesn't add an extra syllable;
# two or more different vowels together are a diphthong,
# and probably don't start a new syllable but might;
# y is considered a vowel when it follows a consonant.
#
# Even with these simple rules, it gets results far better
# than python-hyphenate with the libreoffice hyphenation dictionary.
#
# Copyright 2013 by Akkana Peck http://shallowsky.com.
# Share and enjoy under the terms of the GPLv2 or later.

def count_syllables(word):
    vowels = ['a', 'e', 'i', 'o', 'u']
    on_vowel = False
    in_diphthong = False
    minsyl = 0
    maxsyl = 0
    lastchar = None
    word = word.lower()
    for c in word:
        is_vowel = c in vowels
        if on_vowel == None:
            on_vowel = is_vowel
        # y is a special case
        if c == 'y':
            is_vowel = not on_vowel
        if is_vowel:
            if verbose: print c, "is a vowel"
            if not on_vowel:
                # We weren't on a vowel before.
                # Seeing a new vowel bumps the syllable count.
                if verbose: print "new syllable"
                minsyl += 1
                maxsyl += 1
            elif on_vowel and not in_diphthong and c != lastchar:
                # We were already in a vowel.
                # Don't increment anything except the max count,
                # and only do that once per diphthong.
                if verbose: print c, "is a diphthong"
                in_diphthong = True
                maxsyl += 1
        elif verbose: print "[consonant]"
        on_vowel = is_vowel
        lastchar = c
    # Some special cases:
    if word[-1] == 'e':
        minsyl -= 1
    # if it ended with a consonant followed by y, count that as a syllable.
    if word[-1] == 'y' and not on_vowel:
        maxsyl += 1
    return (minsyl + maxsyl) / 2


def count(filename):
    clauses, words, hardwords = 0, 0, 0
    textf = open(filename, 'r')
    #
    for line in textf:
        # assuming major clauses end in '.', '!', '?', ':', or ';', count clauses
        clauses += line.count('.') + line.count('!') + line.count('?') + line.count(':') + line.count(';')
        tempwords = line.split(None)
        for word in tempwords:
            #four+ syllable words can be considered complex
            syllables = count_syllables(word.strip())
            if syllables > 3:
                hardwords += 1
            #discount words that are three syllables because of common endings
            #otherwise three syllable words are also complex
            elif syllables == 3:
                if not (word.endswith('ed') or word.endswith('ing') or word.endswith('es') or word.endswith('ly')):
                    hardwords += 1
        #number of words in text
        words += len(tempwords)
    textf.close()
    #making decimals work
    wordy = float(words)
    #The Gunning Fog formula for readability of text, in number of years of education necessary
    #to understand the material
    GunningFog = 0.4 * ((wordy / clauses) + 100 * (hardwords / wordy))
    print "Gunning Fog: ", GunningFog


if __name__ == '__main__':
    if sys.argv[1].startswith('-f'):
        count(sys.argv[2])
    else:
        count(sys.argv[1:])