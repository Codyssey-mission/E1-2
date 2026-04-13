from __future__ import annotations


class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int):
        if len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")
        if answer not in (1, 2, 3, 4):
            raise ValueError("정답 번호는 1부터 4 사이여야 합니다.")

        cleaned_question = question.strip()
        cleaned_choices = [choice.strip() for choice in choices]

        if not cleaned_question:
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if any(not choice for choice in cleaned_choices):
            raise ValueError("선택지는 비어 있을 수 없습니다.")

        self.question = cleaned_question
        self.choices = cleaned_choices
        self.answer = answer

    def display(self) -> None:
        print(f"문제: {self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer: int) -> bool:
        return user_answer == self.answer

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )


def get_default_quizzes() -> list[Quiz]:
    return [
        Quiz(
            "대한민국의 수도는 어디일까요?",
            ["부산", "서울", "인천", "대전"],
            2,
        ),
        Quiz(
            "일본의 수도는 어디일까요?",
            ["오사카", "도쿄", "교토", "삿포로"],
            2,
        ),
        Quiz(
            "프랑스의 수도는 어디일까요?",
            ["파리", "리옹", "마르세유", "니스"],
            1,
        ),
        Quiz(
            "캐나다의 수도는 어디일까요?",
            ["토론토", "밴쿠버", "오타와", "몬트리올"],
            3,
        ),
        Quiz(
            "호주의 수도는 어디일까요?",
            ["시드니", "멜버른", "캔버라", "퍼스"],
            3,
        ),
        Quiz(
            "브라질의 수도는 어디일까요?",
            ["상파울루", "브라질리아", "리우데자네이루", "살바도르"],
            2,
        ),
    ]
