# KU Polls Class Diagram

```mermaid
classDiagram
    class User {
        +String username
        +String password
        +String email
        +Boolean is_active
        +DateTime date_joined
        +create_user()
        +authenticate()
    }

    class Question {
        +String question_text
        +DateTime pub_date
        +Boolean is_active
        +create_question()
        +get_active_questions()
    }

    class Choice {
        +String choice_text
        +Integer votes
        +ForeignKey question
        +add_vote()
        +get_vote_percentage()
    }

    class Vote {
        +ForeignKey user
        +ForeignKey choice
        +DateTime vote_date
        +cast_vote()
    }

    User "1" -- "0..*" Vote : casts
    Question "1" -- "0..*" Choice : has
    Choice "1" -- "0..*" Vote : receives
```

## Class Descriptions

### User
- Represents system users
- Handles authentication and authorization
- Manages user sessions

### Question
- Represents poll questions
- Manages question lifecycle
- Tracks publication dates

### Choice
- Represents poll options
- Tracks vote counts
- Calculates vote percentages

### Vote
- Records user votes
- Links users to choices
- Tracks voting timestamps

## Relationships
1. User to Vote: One-to-Many
   - A user can cast multiple votes
   - Each vote belongs to one user

2. Question to Choice: One-to-Many
   - A question can have multiple choices
   - Each choice belongs to one question

3. Choice to Vote: One-to-Many
   - A choice can receive multiple votes
   - Each vote is for one choice 