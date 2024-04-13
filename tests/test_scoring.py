import pytest


def f(s, p):
    # Define the scaling factors for s and p
    scale_s = 3
    scale_p = 1

    # Calculate the base value for the constraints f(1,-2) == f(0.5, 0) == f(0,2)
    base_value = 1000  # scale_s * 0.5 + scale_p * 0

    # Adjust the function to increase with either s or p increasing
    return (scale_s * s + scale_p * p + base_value) / (scale_s + scale_p + base_value)


inputs = [
    (0, -2, -0.091),
    (0, -1, 0.091),
    (0, 0, 0.273),
    (0, 1, 0.455),
    (0, 2, 0.636),
    #
    (0.5, -2, 0.182),
    (0.5, -1, 0.364),
    (0.5, 0, 0.545),
    (0.5, 1, 0.727),
    (0.5, 2, 0.901),
]


@pytest.mark.parametrize("s, p, result", inputs)
def test_parameters(s, p, result):
    assert f(s, p) == pytest.approx(
        result, abs=0.01
    ), f"s: {s}, p: {p}, result: {result}"
