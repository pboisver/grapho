from typing import Any, Optional

import pandas as pd


def test_bools():
    li: list = list()
    di: dict = dict()
    se: set = set()
    assert not li and not di and not se

    ln = dn = sn = None
    assert not ln and not dn and not sn

    df = pd.DataFrame()
    assert df.empty

    def foo():
        return []

    assert not foo()

    def bar():
        return None

    assert not bar()

    def baz(val: Optional[Any] = None):
        return val

    assert baz([2])
    assert baz([2]) or None
    assert (baz(False) or None) is not False
    assert (baz(False) or None) is None
    assert not baz() and baz() is None