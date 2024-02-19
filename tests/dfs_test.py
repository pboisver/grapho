from pandas import DataFrame

input_message: dict = {
    "@id": "123cb",
    "perf_content": [
        ["id", "passed", "total", "goal"],
        ["1", 4, 5, 10],
        ["2", 3, 6, 10],
        ["3", 7, 10, 10],
    ],
}
input_message2: str = """{
    "@id": "123cb",
    "perf_content": [
        ["id", "passed", "total", "goal"],
        ["1", 4, 5, 10],
        ["2", 3, 6, 10],
        ["3", 7, 10, 10]
    ]
}"""


def test_load_from_array(capsys):
    data: list[list] = input_message.get("perf_content")
    # data: list[list] = json.loads(input_message2).get("perf_content")

    df: DataFrame = DataFrame(data[1:], columns=data[0])

    with capsys.disabled():
        print()
        print(df)


def test_with_measures():
    input_message: dict = {
        "@id": "123cb",
        "perf_content": [
            ["id", "passed", "total", "goal"],
            ["1", 4, 5, 10],
            ["2", 3, 6, 10],
            ["3", 7, 10, 10]
        ]
    }

    data = input_message["perf_content"]
    df = DataFrame(data[1:], columns=data[0])
    
    df = df.set_index('id')
    
    df[0:1]

    pass
    # df[0:0] == [1]
