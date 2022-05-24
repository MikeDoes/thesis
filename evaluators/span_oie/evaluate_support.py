def lexical_match(annotation, prediction, ignoreStopwords, ignoreCase, LEXICAL_THRESHOLD=0.5):        
        sentence_annotation = annotation.bow().split(' ')
        sentence_example = prediction.bow().split(' ')
        
        count = 0

        for w1 in sentence_annotation:
            for w2 in sentence_example:
                if w1 == w2:
                    count += 1

        # We check how well does the extraction lexically cover the reference
        # Note: this is somewhat lenient as it doesn't penalize the extraction for
        # being too long. Also why do we refer to this as sentence? Should it not be triplet?
        # If it is an relation or argument than it should be called a phrase

        coverage = float(count) / len(sentence_annotation)

        return coverage > LEXICAL_THRESHOLD