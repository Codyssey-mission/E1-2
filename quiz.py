from __future__ import annotations

from typing import Any, Dict, List, Optional


class Quiz:
    # 퀴즈 한 문제에 필요한 데이터를 검증하고 초기화한다.
    def __init__(self, question: str, choices: List[str], answer: int, hint: str):
        if len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")
        if answer not in (1, 2, 3, 4):
            raise ValueError("정답 번호는 1부터 4 사이여야 합니다.")

        cleaned_question = question.strip()
        cleaned_choices = [choice.strip() for choice in choices]
        cleaned_hint = hint.strip()

        if not cleaned_question:
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if any(not choice for choice in cleaned_choices):
            raise ValueError("선택지는 비어 있을 수 없습니다.")
        if not cleaned_hint:
            raise ValueError("힌트는 비어 있을 수 없습니다.")

        self.question = cleaned_question
        self.choices = cleaned_choices
        self.answer = answer
        self.hint = cleaned_hint

    # 문제와 4개의 선택지를 화면에 출력한다.
    def display(self) -> None:
        print(f"문제: {self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    # 사용자가 고른 번호가 정답과 일치하는지 확인한다.
    def is_correct(self, user_answer: int) -> bool:
        return user_answer == self.answer

    # 퀴즈 객체를 JSON 저장용 딕셔너리로 변환한다.
    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    # 저장된 딕셔너리 데이터를 Quiz 객체로 복원한다.
    def from_dict(cls, data: Dict[str, Any]) -> "Quiz":
        hint = data.get("hint")
        if not isinstance(hint, str) or not hint.strip():
            hint = cls.build_default_hint(data["choices"], data["answer"])
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=hint,
        )

    @staticmethod
    # 힌트가 없을 때 정답 선택지의 첫 글자를 이용해 기본 힌트를 만든다.
    def build_default_hint(choices: List[str], answer: int) -> str:
        answer_text = choices[answer - 1]
        first_letter = answer_text[0]
        return f"정답은 '{first_letter}'(으)로 시작합니다."


# 기본으로 제공할 수도 퀴즈 목록을 생성한다.
def get_default_quizzes() -> List[Quiz]:
    return [
        Quiz(
            "대한민국의 수도는 어디일까요?",
            ["부산", "서울", "인천", "대전"],
            2,
            "한강이 흐르는 대한민국의 대표 도시입니다.",
        ),
        Quiz(
            "일본의 수도는 어디일까요?",
            ["오사카", "도쿄", "교토", "삿포로"],
            2,
            "일본의 정치와 경제 중심지입니다.",
        ),
        Quiz(
            "프랑스의 수도는 어디일까요?",
            ["파리", "리옹", "마르세유", "니스"],
            1,
            "에펠탑이 있는 도시입니다.",
        ),
        Quiz(
            "캐나다의 수도는 어디일까요?",
            ["토론토", "밴쿠버", "오타와", "몬트리올"],
            3,
            "토론토도 밴쿠버도 아닌 행정 수도입니다.",
        ),
        Quiz(
            "호주의 수도는 어디일까요?",
            ["시드니", "멜버른", "캔버라", "퍼스"],
            3,
            "시드니와 멜버른 사이 절충으로 정해진 도시입니다.",
        ),
        Quiz(
            "브라질의 수도는 어디일까요?",
            ["상파울루", "브라질리아", "리우데자네이루", "살바도르"],
            2,
            "계획도시로 건설된 브라질의 수도입니다.",
        ),
    ]
