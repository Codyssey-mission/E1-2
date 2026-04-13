from __future__ import annotations

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import shutil
import os

from quiz import Quiz, get_default_quizzes


class QuizGame:
    def __init__(self) -> None:
        self.state_path = Path(__file__).resolve().parent / "state.json"
        self.quizzes: List[Quiz] = []
        self.best_score: Optional[int] = None
        self.score_history: List[Dict[str, Any]] = []
        self.running = True
        self.load_state()

    def show_menu(self) -> None:
        print("\n==== 수도 맞추기 퀴즈 게임 ====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 삭제")
        print("4. 퀴즈 목록 보기")
        print("5. 최고 점수 확인")
        print("6. 점수 기록 보기")
        print("7. 종료")

    def read_input(self, prompt: str) -> Optional[str]:
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

    def prompt_non_empty(self, prompt: str) -> Optional[str]:
        while self.running:
            value = self.read_input(prompt)
            if value is None:
                return None
            if value == "":
                print("빈 입력은 허용되지 않습니다. 다시 입력해주세요.")
                continue
            return value
        return None

    def prompt_int_in_range(self, prompt: str, minimum: int, maximum: int) -> Optional[int]:
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
        choice = self.prompt_int_in_range("메뉴 번호를 입력하세요: ", 1, 7)
        return choice if choice is not None else 7

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
            score_history = data.get("score_history", [])

            if not isinstance(quizzes_data, list):
                raise ValueError("quizzes 값이 목록이 아닙니다.")
            if best_score is not None and not isinstance(best_score, int):
                raise ValueError("best_score 값이 정수가 아닙니다.")
            if not isinstance(score_history, list):
                raise ValueError("score_history 값이 목록이 아닙니다.")

            self.quizzes = [Quiz.from_dict(item) for item in quizzes_data]
            self.best_score = best_score
            self.score_history = [self.normalize_history_entry(item) for item in score_history]
        except (OSError, KeyError, TypeError, ValueError) as error:
            print(f"state.json을 읽을 수 없어 기본 데이터로 복구합니다. ({error})")
            self.reset_default_state()
            self.save_state()
        except(json.JSONDecodeError):
            pass

        

    def normalize_history_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        played_at = entry.get("played_at")
        total_questions = entry.get("total_questions")
        score = entry.get("score")

        if not isinstance(played_at, str) or not played_at.strip():
            raise ValueError("played_at 값이 올바르지 않습니다.")
        if not isinstance(total_questions, int):
            raise ValueError("total_questions 값이 정수가 아닙니다.")
        if not isinstance(score, int):
            raise ValueError("score 값이 정수가 아닙니다.")

        return {
            "played_at": played_at,
            "total_questions": total_questions,
            "score": score,
        }

    def reset_default_state(self) -> None:
        self.quizzes = get_default_quizzes()
        self.best_score = None
        self.score_history = []

    def save_state(self) -> None:
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "score_history": self.score_history,
        }
        try:
            with self.state_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f"저장 중 오류가 발생했습니다: {error}")

    def prompt_quiz_count(self) -> Optional[int]:
        print(f"현재 등록된 퀴즈는 총 {len(self.quizzes)}문제입니다.")
        return self.prompt_int_in_range("몇 문제를 풀까요?: ", 1, len(self.quizzes))
 
    def prompt_answer(self, quiz: Quiz, hint_used: bool) -> Optional[int]:
        while self.running:
            if hint_used:
                prompt = "정답 번호를 입력하세요 (1~4): "
            else:
                prompt = "정답 번호를 입력하세요 (1~4, 힌트는 0): "

            raw_value = self.read_input(prompt)
            if raw_value is None:
                return None
            if raw_value == "":
                print("입력이 비어 있습니다. 다시 입력해주세요.")
                continue
            if raw_value == "0":
                if hint_used:
                    print("힌트는 이미 확인했습니다.")
                    continue
                print(f"힌트: {quiz.hint}")
                print("힌트를 사용하면 해당 문제에서 1점 차감됩니다.")
                return 0
            try:
                value = int(raw_value)
            except ValueError:
                print("숫자만 입력해주세요.")
                continue
            if not 1 <= value <= 4:
                print("1부터 4 사이의 숫자를 입력해주세요. 힌트는 0입니다.")
                continue
            return value
        return None

    def append_history(self, total_questions: int, score: int) -> None:
        self.score_history.append(
            {
                "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_questions": total_questions,
                "score": score,
            }
        )

    def play_quiz(self) -> None:
        print("\n[퀴즈 풀기]")
        if not self.quizzes:
            print("출제할 퀴즈가 없습니다.")
            return

        question_count = self.prompt_quiz_count()
        if question_count is None:
            return

        selected_quizzes = random.sample(self.quizzes, question_count)
        score = 0
        interrupted = False

        for index, quiz in enumerate(selected_quizzes, start=1):
            print(f"\n[{index}/{question_count}]")
            quiz.display()
            hint_used = False

            while self.running:
                answer = self.prompt_answer(quiz, hint_used)

                if answer is None:
                    interrupted = True
                    break

                if answer == 0:
                    hint_used = True
                    continue

                if quiz.is_correct(answer):
                    earned_score = 0 if hint_used else 1
                    score += earned_score
                    if hint_used:
                        print("정답입니다. 힌트 사용으로 이 문제 점수는 0점입니다.")
                    else:
                        print("정답입니다.")
                else:
                    print(f"오답입니다. 정답은 {quiz.answer}번입니다.")
                break

            if interrupted:
                break

        print(f"\n결과: {question_count}문제 중 총 {score}점")
        self.append_history(question_count, score)

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("최고 점수가 갱신되었습니다.")
        else:
            print(f"현재 최고 점수는 {self.best_score}점입니다.")

        self.save_state()

    def add_quiz(self) -> None:
        print("\n[퀴즈 추가]")

        question = self.prompt_non_empty("문제를 입력하세요: ")
        if question is None:
            return

        choices: List[str] = []
        for index in range(1, 5):
            choice = self.prompt_non_empty(f"{index}번 선택지를 입력하세요: ")
            if choice is None:
                return
            choices.append(choice)

        answer = self.prompt_int_in_range("정답 번호를 입력하세요 (1~4): ", 1, 4)
        if answer is None:
            return

        hint = self.prompt_non_empty("힌트를 입력하세요: ")
        if hint is None:
            return

        try:
            new_quiz = Quiz(question=question, choices=choices, answer=answer, hint=hint)
        except ValueError as error:
            print(f"퀴즈를 추가할 수 없습니다: {error}")
            return

        self.quizzes.append(new_quiz)
        self.save_state()
        print("새 퀴즈가 저장되었습니다.")

    def delete_quiz(self) -> None:
        print("\n[퀴즈 삭제]")
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        self.show_quizzes()
        quiz_number = self.prompt_int_in_range("삭제할 퀴즈 번호를 입력하세요: ", 1, len(self.quizzes))
        if quiz_number is None:
            return

        removed_quiz = self.quizzes.pop(quiz_number - 1)
        self.save_state()
        print(f"삭제되었습니다: {removed_quiz.question}")

    def show_quizzes(self) -> None:
        print("\n[퀴즈 목록 보기]")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{index}번 퀴즈]")
            quiz.display()
            print(f"힌트: {quiz.hint}")

    def show_best_score(self) -> None:
        print("\n[최고 점수 확인]")
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않아 최고 점수가 없습니다.")
            return
        print(f"현재 최고 점수: {self.best_score}")

    def show_score_history(self) -> None:
        print("\n[점수 기록 보기]")
        if not self.score_history:
            print("아직 저장된 게임 기록이 없습니다.")
            return

        for index, entry in enumerate(self.score_history, start=1):
            print(
                f"{index}. {entry['played_at']} | "
                f"{entry['total_questions']}문제 | {entry['score']}점"
            )

    def exit_game(self) -> None:
        print("\n게임을 종료합니다.")
        self.safe_shutdown()

    def safe_shutdown(self) -> None:
        state_file = "state.json"
        if os.path.exists(state_file):
            shutil.copy2(state_file, state_file + ".bak") 
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
                self.delete_quiz()
            elif choice == 4:
                self.show_quizzes()
            elif choice == 5:
                self.show_best_score()
            elif choice == 6:
                self.show_score_history()
            elif choice == 7:
                self.exit_game()


if __name__ == "__main__":
    QuizGame().run()
