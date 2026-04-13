from __future__ import annotations

import json
from pathlib import Path

from quiz import Quiz, get_default_quizzes


class QuizGame:
    def __init__(self) -> None:
        self.state_path = Path(__file__).resolve().parent / "state.json"
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.running = True
        self.load_state()

    def show_menu(self) -> None:
        print("\n==== 수도 맞추기 퀴즈 게임 ====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 종료")

    def read_input(self, prompt: str) -> str | None:
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print("\n입력이 취소되었습니다. 가능한 범위에서 저장 후 종료합니다.")
            self.safe_shutdown()
            return None
        except EOFError:
            print("\n입력 스트림이 종료되었습니다. 가능한 범위에서 저장 후 종료합니다.")
            self.safe_shutdown()
            return None

    def prompt_non_empty(self, prompt: str) -> str | None:
        while self.running:
            value = self.read_input(prompt)
            if value is None:
                return None
            if value == "":
                print("빈 입력은 허용되지 않습니다. 다시 입력해주세요.")
                continue
            return value
        return None

    def prompt_int_in_range(self, prompt: str, minimum: int, maximum: int) -> int | None:
        while self.running:
            raw_value = self.read_input(prompt)
            if raw_value is None:
                return None
            if raw_value == "":
                print("입력이 비어 있습니다. 다시 입력해주세요.")
                continue
            try:
                value = int(raw_value)
            except ValueError:
                print("숫자만 입력해주세요.")
                continue
            if not minimum <= value <= maximum:
                print(f"{minimum}부터 {maximum} 사이의 숫자를 입력해주세요.")
                continue
            return value
        return None

    def get_menu_choice(self) -> int:
        choice = self.prompt_int_in_range("메뉴 번호를 입력하세요: ", 1, 5)
        return choice if choice is not None else 5

    def load_state(self) -> None:
        if not self.state_path.exists():
            print("state.json이 없어 기본 퀴즈 데이터로 시작합니다.")
            self.reset_default_state()
            self.save_state()
            return

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes_data = data["quizzes"]
            best_score = data.get("best_score")

            if not isinstance(quizzes_data, list):
                raise ValueError("quizzes 값이 목록이 아닙니다.")
            if best_score is not None and not isinstance(best_score, int):
                raise ValueError("best_score 값이 정수가 아닙니다.")

            self.quizzes = [Quiz.from_dict(item) for item in quizzes_data]
            self.best_score = best_score
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"state.json을 읽을 수 없어 기본 데이터로 복구합니다. ({error})")
            self.reset_default_state()
            self.save_state()

    def reset_default_state(self) -> None:
        self.quizzes = get_default_quizzes()
        self.best_score = None

    def save_state(self) -> None:
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with self.state_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f"저장 중 오류가 발생했습니다: {error}")

    def play_quiz(self) -> None:
        print("\n[퀴즈 풀기]")
        if not self.quizzes:
            print("출제할 퀴즈가 없습니다.")
            return

        score = 0
        total = len(self.quizzes)

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{index}/{total}]")
            quiz.display()
            answer = self.prompt_int_in_range("정답 번호를 입력하세요 (1~4): ", 1, 4)
            if answer is None:
                return

            if quiz.is_correct(answer):
                score += 1
                print("정답입니다.")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n결과: {total}문제 중 {score}문제 정답")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("최고 점수가 갱신되었습니다.")
            self.save_state()
        else:
            print(f"현재 최고 점수는 {self.best_score}점입니다.")

    def add_quiz(self) -> None:
        print("\n[퀴즈 추가]")

        question = self.prompt_non_empty("문제를 입력하세요: ")
        if question is None:
            return

        choices: list[str] = []
        for index in range(1, 5):
            choice = self.prompt_non_empty(f"{index}번 선택지를 입력하세요: ")
            if choice is None:
                return
            choices.append(choice)

        answer = self.prompt_int_in_range("정답 번호를 입력하세요 (1~4): ", 1, 4)
        if answer is None:
            return

        try:
            new_quiz = Quiz(question=question, choices=choices, answer=answer)
        except ValueError as error:
            print(f"퀴즈를 추가할 수 없습니다: {error}")
            return

        self.quizzes.append(new_quiz)
        self.save_state()
        print("새 퀴즈가 저장되었습니다.")

    def show_quizzes(self) -> None:
        print("\n[퀴즈 목록 보기]")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{index}번 퀴즈]")
            quiz.display()

    def show_best_score(self) -> None:
        print("\n[최고 점수 확인]")
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않아 최고 점수가 없습니다.")
            return
        print(f"현재 최고 점수: {self.best_score}")

    def exit_game(self) -> None:
        print("\n게임을 종료합니다.")
        self.safe_shutdown()

    def safe_shutdown(self) -> None:
        self.save_state()
        self.running = False

    def run(self) -> None:
        while self.running:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quizzes()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                self.exit_game()


if __name__ == "__main__":
    QuizGame().run()
