import math

from spam_detect import models
from spam_detect.dataset import Example


def test_prob_calculation():
    dataset = [
        Example(email="spam rules", spam=True),
        Example(email="ham rules", spam=False),
        Example(email="hello ham", spam=False),
    ]

    classify_func, _ = models.NaiveBayes(
        decision_boundary=0.5, test_set_size=0.0
    ).train(dataset)
    email = "hello spam"
    probs_if_ham = [
        (1 + 0.5) / (2 + 2 * 0.5),  # "hello" (present)
        (0 + 0.5) / (2 + 2 * 0.5),  # "spam" (present)
        1 - (2 + 0.5) / (2 + 2 * 0.5),  # "ham" (not present)
        1 - (1 + 0.5) / (2 + 2 * 0.5),  # "rules" (not present)
    ]
    probs_if_spam = [
        (0 + 0.5) / (1 + 2 * 0.5),  # "hello" (present)
        (1 + 0.5) / (1 + 2 * 0.5),  # "spam" (present)
        1 - (0 + 0.5) / (1 + 2 * 0.5),  # "ham" (not present)
        1 - (1 + 0.5) / (1 + 2 * 0.5),  # "rules" (not present)
    ]
    p_if_spam = math.exp(sum(math.log(p) for p in probs_if_spam))
    p_if_ham = math.exp(sum(math.log(p) for p in probs_if_ham))

    # Should be about 0.83
    actual = classify_func(email).score
    expected = p_if_spam / (p_if_spam + p_if_ham)
    residual = abs(actual - expected)
    assert residual <= 0.001
