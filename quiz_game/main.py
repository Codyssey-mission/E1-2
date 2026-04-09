from quiz import Quiz, get_default_quizzes


class QuizGame:
    def __init__(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None
        self.running = True

    def show_menu(self):
        print("\n==== 수도 맞추기 퀴즈 게임 ====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 종료")

    def get_menu_choice(self):
        while True:
            try:
                user_input = input("메뉴 번호를 입력하세요: ").strip()

                if user_input == "":
                    print("입력이 비어 있습니다. 다시 입력해주세요.")
                    continue

                choice = int(user_input)

                if choice < 1 or choice > 5:
                    print("1부터 5 사이의 숫자를 입력해주세요.")
                    continue

                return choice

            except ValueError:
                print("숫자만 입력해주세요.")
            except KeyboardInterrupt:
                print("\n입력이 취소되었습니다. 프로그램을 종료합니다.")
                self.running = False
                return 5
            except EOFError:
                print("\n입력이 종료되었습니다. 프로그램을 종료합니다.")
                self.running = False
                return 5

    def play_quiz(self):
        print("\n[퀴즈 풀기]")
        print("아직 구현 전입니다.")

    def add_quiz(self):
        print("\n[퀴즈 추가]")
        print("아직 구현 전입니다.")

    def show_quizzes(self):
        print("\n[퀴즈 목록 보기]")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{index}번 퀴즈]")
            quiz.display()

    def show_best_score(self):
        print("\n[최고 점수 확인]")

        if self.best_score is None:
            print("아직 플레이한 기록이 없습니다.")
        else:
            print(f"현재 최고 점수: {self.best_score}")

    def exit_game(self):
        print("\n게임을 종료합니다.")
        self.running = False

    def run(self):
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
    game = QuizGame()
    game.run()