import html
import json
import urllib.request as request

TOKEN_REQUEST_URL = "https://opentdb.com/api_token.php?command=request"
QUESTION_REQUEST_URL = "https://opentdb.com/api.php?amount=50&token="

question_bank = {}


def load_token():
    data = request.urlopen(TOKEN_REQUEST_URL).read()
    json_data = json.loads(data.decode("utf-8"))
    token = json_data.get("token")
    return token


def get_questions(token):
    data = request.urlopen(QUESTION_REQUEST_URL + token).read()
    json_data = json.loads(data.decode("utf-8"))

    if json_data.get("response_code") == 0:
        # Got more questions successfully
        questions = json_data.get("results")
        for question in questions:
            title = html.unescape(question.get("question"))
            answer = html.unescape(question.get("correct_answer"))

            question_bank[title] = answer

        return True
    elif json_data.get("response_code") == 4:
        # We've run out of questions
        return False
    else:
        raise RuntimeError("Fetching questions went wrong")


def save_questions():
    with open("questions.json", "w") as f:
        json.dump(question_bank, f)


if __name__ == "__main__":
    token = load_token()
    print("Got token: ", token)

    # Fetch questions until we run out
    while get_questions(token):
        print("Got more questions...")
        print(f"{len(question_bank)} questions so far")

    save_questions()
    print("Saved questions to questions.json!")
