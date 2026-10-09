# DATABASE TABLES STRUCTURE

## Exercises

| Column | Type | Rules | Example | Explanation |
| --- | --- | --- | --- | --- |
| ID | Int | Unique | 123 | A single generated ID for each exercise. This distinguishes one exercise from another. |
| ELO | Int | Can change | 69 | ELO rating of this excersise. Increases when someone does it wrong, decrese when someone does it rigth |
| program | Bool | 0 or 1 | 0 | Defines whether the user needs to write a main function (1) or recreate a function (0). |
| prototype_function | String | Can be empty if program is 1 | "size_t ft_strlen(const char *s);" | The function prototype that the student must implement. Can be empty when the exercise requires writing a complete program. |
| topic | Subquery |  |  | A list of topics associated with the exercise. The abvailable topics will be definded by the 1v1 grid |
| description | String | No more than 500 characters | "Write a function reproducing the behavior of strlen" | Describes what the user needs to implement. |
| hints | String | Comma + space separated | "strings, char count, segmentation fault" | A list of hints to help the user solve the exercise. This will be for feeding the LLM ONLY, thats why we dont need a subquerry here. |
| forbidden_functions | Subquery |  |  | A list of functions that the user is not allowed to use. This is particularly important for the implementation of the tester. |
| pre_body | String | Can be empty, valid C code when provided | "int main(void) { int x = 5; printf(\"%d\\n\", x); return 0; }" | Initial code provided to the student when opening the exercise. Useful for debugging exercises or exercises where the student must complete or modify existing code. Good example is if the excersise is inside "Debug" topic |
| reference_solution | String | Valid C code | "size_t ft_strlen(const char *s) { size_t i = 0; while (s[i]) i++; return i; }" | A complete reference solution used to verify that the exercise and its tests work correctly before publishing. For exercises with a pre_body, this should contain the corrected or completed version of the initial code. |
| tests | Subquery |  |  | A list of tests used to validate the user's solution. |

### Topic subquery

| Column | Type | Rules | Example | Explanation |
| --- | --- | --- | --- | --- |
| ID | Int | Unique | 1 | A unique ID for each topic. |
| topic | String | Unique | "strings" | The name of the topic. |

### Forbidden functions subquery

| Column | Type | Rules | Example | Explanation |
| --- | --- | --- | --- | --- |
| ID | Int | Unique | 1 | A unique ID for each forbidden function. |
| function | String | Not empty | "strlen" | The name of a function that cannot be used in the exercise. |

### Tests subquery

| Column | Type | Rules | Example | Explanation |
| --- | --- | --- | --- | --- |
| ID | Int | Unique | 1 | A unique ID for each test. |
| compiler_code | String | Not empty | "gcc -Wall -Wextra -Werror main.c -o main" | The compiler command used to compile the student's solution. |
| test_code | String | Can be empty if program is 1. Otherwise, valid C code containing the student code placeholder. | "#include <stdio.h>\n// STUDENT_CODE_HERE\nint main(void) { printf(\"%zu\\n\", ft_strlen(\"Hello\")); return 0; }" | The test source code, including headers, a placeholder where the tester inserts the student's code, and a main function that executes the implementation. For program exercises, this can be empty because the student's code already contains the main function. |
| input | String | Can be empty | "" | Standard input provided to the compiled program during the test. |
| expected_output | String | Can be empty | "5" | The expected output used to verify whether the solution passes the test. |

## Users

| Column | Type | Rules | Example | Explanation |
| --- | --- | --- | --- | --- |
| id | Int | Unique | 123 | A unique generated ID for each user. |
| username | String | Unique, not empty | "john_doe" | The user's public username. |
| email | String | Unique, can be empty if GitHub login | "john@example.com" | The user's email address. Not required when authenticating through GitHub. |
| password_hash | String | Can be empty if GitHub login | "$2b$12$..." | The securely hashed password. Not required for GitHub authentication. |
| github_id | String | Unique, can be empty if email login | "12345678" | The user's GitHub account ID. Not required for email/password authentication. |
| friends | Subquery | Can be empty | Empty | A list of user IDs representing the user's friends. |
| elo | Int | Default 1000, minimum 0 | 1250 | The user's competitive rating, adjusted based on multiplayer game results. |
| total_score | Int | Default 0, minimum 0 | 15000 | The total score accumulated by the user across all games. |
| achievements | Subquery | List of booleans | Empty | A list of boolean values indicating which achievements the user has unlocked. |
| level_solo | Int | Default 1, minimum 1 | 12 | The highest solo level the user has reached. |

### Friends subquery

| Column | Type | Rules | Example | Explanation |
| --- | --- | --- | --- | --- |
| id | Int | Unique | 1 | A unique ID for each friendship relationship. |
| friend_id | Int | Must reference an existing user | 456 | The ID of a user in the current user's friends list. |

### Achievements subquery

| Column | Type | Rules | Example | Explanation |
| --- | --- | --- | --- | --- |
| id | Int | Unique | 1 | A unique ID for each achievement. |
| achievement_1 | Bool | 0 or 1, default 0 | 1 | Indicates whether the user has unlocked achievement 1. |
| achievement_2 | Bool | 0 or 1, default 0 | 0 | Indicates whether the user has unlocked achievement 2. |
| achievement_3 | Bool | 0 or 1, default 0 | 1 | Indicates whether the user has unlocked achievement 3. |
| ... | Bool | 0 or 1, default 0 | 0 | Additional achievements to be defined later. |

## Game

| Column | Type | Rules | Example | Explanation |
| --- | --- | --- | --- | --- |
| id | Int | Unique | 123 | A unique generated ID for each multiplayer game instance. |
| user1 | Subquery | Required | Empty | Stores the first player's performance and score in this game. |
| user2 | Subquery | Required | Empty | Stores the second player's performance and score in this game. |
| exercise_id | Int | Must reference an existing exercise | 42 | The exercise assigned to both players in this game instance. |

### Game user subquery

| Column | Type | Rules | Example | Explanation |
| --- | --- | --- | --- | --- |
| id | Int | Unique | 1 | A unique ID for the player's participation in this game. |
| user_id | Int | Must reference an existing user | 123 | The ID of the player participating in the game. |
| time | Int | Minimum 0, measured in milliseconds | 45000 | The time taken by the player to complete the exercise. |
| attempts | Int | Default 0, minimum 0 | 3 | The number of times the player submitted their code for testing, including the successful submission. |
| total_score | Int | Minimum 0 | 750 | The final score earned by this player in this game after applying penalties. |