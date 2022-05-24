Wire 57 Evaluation algorithm

For each sentence:
    Create the matrix of shape triplet x prediction called scores
    Create the matrix of shape triplet x prediction called exact scores

    Fill the matrix with map -> tuple_exact_match #True False Matrix
    Fill the matrix with map -> tuple_match # Scores filled with [precision, recall]

    Aggregate function these functions
