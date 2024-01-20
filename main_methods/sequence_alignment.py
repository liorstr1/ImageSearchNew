def sequence_alignment(seq1, seq2):
    # Initialize the matrix
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill the matrix
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                dp[i][j] = i + j
            elif seq1[i - 1] in seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1])

    # Trace back to find the alignment
    alignment1, alignment2 = [], []
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i - 1] in seq2[j - 1]:
            alignment1.append(seq1[i - 1])
            alignment2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] < dp[i][j - 1]:
            alignment1.append(seq1[i - 1])
            alignment2.append('-m-')
            i -= 1
        else:
            alignment1.append('-m-')
            alignment2.append(seq2[j - 1])
            j -= 1

    while i > 0:
        alignment1.append(seq1[i - 1])
        alignment2.append('-m-')
        i -= 1

    while j > 0:
        alignment1.append('-m-')
        alignment2.append(seq2[j - 1])
        j -= 1

    return alignment1[::-1], alignment2[::-1]


def get_consensus(sentences, threshold=0.5):
    consensus = []
    for seq in sentences:
        if not consensus:
            for c in seq.split(' '):
                consensus.append({c: 1})
        else:
            res = sequence_alignment(
                seq.split(' '),
                [list(co.keys()) for co in consensus]
            )
            idx_in_consensus = 0
            for idx in range(len((res[0]))):
                if res[0][idx] == '-m-':
                    consensus[idx_in_consensus]['-m-'] = 1
                    idx_in_consensus += 1
                elif res[1][idx] == '-m-':
                    to_add_dict = [{'-m-': 1, res[0][idx]: 1}]
                    consensus = consensus[:idx_in_consensus] + to_add_dict + consensus[idx_in_consensus:]
                    idx_in_consensus += 1
                elif res[0][idx] in res[1][idx]:
                    consensus[idx_in_consensus][res[0][idx]] += 1
                    idx_in_consensus += 1

    res = []
    for c in consensus:
        passed = [k for k, count in c.items() if count/len(sentences) >= threshold and k != '-m-']
        if passed:
            if isinstance(passed, list):
                res.extend(passed)
            else:
                res.append(passed[0])
    return " ".join(res)
