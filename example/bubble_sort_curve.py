"""
Code to estimate the bubble sort curve from this video:
https://www.youtube.com/watch?v=Gm8v_MR7TGk
"""
import random

import matplotlib.pyplot


def bubblesort_steps(data, steps=None):
    """
    Does bubblesort, to provided number of `steps`.
    `steps` should be < `len(data)`.
    When steps is specified, the last `steps` elements are sorted.
    """
    if steps is None:
        steps = len(data)

    for iteration in range(steps):
        for i in range(0, len(data) - iteration - 1):
            if data[i] > data[i+1]:
                data[i], data[i+1] = data[i+1], data[i]


def main():
    unsorted_datas = [0] * 1000

    # Get an average of 10,000 bubble sorts to estimate the curve
    for _ in range(100):
        data = [i+1 for i in range(1300)]
        random.shuffle(data)
        bubblesort_steps(data, steps=300)
        unsorted_data = data[:1000]
        for index, num in enumerate(unsorted_data):
            unsorted_datas[index] += num

    # plot the average value for each unsorted index
    unsorted_datas = [num / 1000 for num in unsorted_datas]

    matplotlib.pyplot.plot(unsorted_datas)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
