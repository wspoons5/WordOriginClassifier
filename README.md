# Purpose
This repository contains Python 3 code that classifies a word as either of Latin or Greek origin by assessing conditional letter frequencies and positioning. 

# Explanation
Suppose you have two sets, L and G, where L contains English words of Latin origin and G contains English words of Greek origin. We are given a word we want to classify, *unclassified* that is of either Latin or Greek origin; however, we do not know which it is. We can classify *unclassified* by looking at it's sequence of letters and classifying it as the language for which we are more likely to observe that sequence of letters.

For each language origin, we can estimate the actual unconditional letter frequency using our sets L and G. We can also estimate *conditional* letter frequencies from these sets. A conditional letter frequency is the probability of observing a particular letter *after* another letter. That is, let *a* and *b* both be letters, then the conditional frequency of *a* given *b* is how many times we are likely to see *b* directly after *a*. After obtaining estimates of the conditional letter frequencies and the unconditional letter frequencies via word sets L and G we can estimate the probability of observing the word *unclassified* in both Greek and Latin. We then return the language for which the probability of observing *unclassified* is highest.

We do this by taking the probability of observing the first letter of the unclassified word (obtained from the *unconditional* letter frequency) and then multiplying that by the probability of conditionally observing each other letter given the letter that preceded it.

# Future Work
**Support classification of more language origins:** English has more origin languages than Latin and Greek. French, Germanic, and Italian are also prominent. Expanding our classifier to support classification of a word beyond Latin or Greek origin would improve its useability greatly.

**Revise unconditional letter frequencies:** Currently, we are using the unconditional letter frequencies to determine the probability of observing the first letter in the word to be classified. However, a better approach would be to use the unconditional *leading* letter frequency. There is no theoretical reason to believe that the unconditional letter frequencies and unconditional leading letter frequencies would be identical. Therefore, using the unconditional leading letter frequency when determining the probability of the first letter is likely to yield better results.

**Expand to general language classification:** This method could also be extended to classify strings by which language they are written in. Seeing the degree of success that this yields would be interesting.
