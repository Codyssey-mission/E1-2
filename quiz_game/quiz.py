class Quiz:
    def __init__(self, question, choices, answer):
        if len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")

        if answer not in [1, 2, 3, 4]:
            raise ValueError("정답 번호는 1부터 4 사이여야 합니다.")

        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print()
        print(f"문제: {self.question}")

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["question"],
            data["choices"],
            data["answer"]
        )
    
def get_default_quizzes():
    return [
        Quiz(
            "대한민국의 수도는 어디일까요?",
            ["부산", "서울", "인천", "대전"],
            2
        ),
        Quiz(
            "일본의 수도는 어디일까요?",
            ["오사카", "도쿄", "교토", "삿포로"],
            2
        ),
        Quiz(
            "프랑스의 수도는 어디일까요?",
            ["파리", "리옹", "마르세유", "니스"],
            1
        ),
        Quiz(
            "캐나다의 수도는 어디일까요?",
            ["토론토", "밴쿠버", "오타와", "몬트리올"],
            3
        ),
        Quiz(
            "호주의 수도는 어디일까요?",
            ["시드니", "멜버른", "캔버라", "퍼스"],
            3
        ),
        Quiz(
            "브라질의 수도는 어디일까요?",
            ["상파울루", "브라질리아", "리우데자네이루", "살바도르"],
            2
        )
    ]

if __name__ == "__main__":
    quizzes = get_default_quizzes()

    first_quiz = quizzes[0]
    first_quiz.display()

    print()
    print("정답 확인 테스트")
    print(first_quiz.is_correct(2))
