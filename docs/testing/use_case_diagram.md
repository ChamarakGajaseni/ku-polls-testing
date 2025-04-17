# KU Polls Use Case Diagram

```mermaid
graph TD
    subgraph "KU Polls System"
        UC1[Register User]
        UC2[Login]
        UC3[Create Poll]
        UC4[Edit Poll]
        UC5[Delete Poll]
        UC6[Vote on Poll]
        UC7[View Results]
        UC8[Export Results]
        UC9[Manage Profile]
    end

    subgraph "Actors"
        A1[Guest User]
        A2[Registered User]
        A3[Admin]
    end

    %% Guest User Relationships
    A1 --> UC1
    A1 --> UC2

    %% Registered User Relationships
    A2 --> UC3
    A2 --> UC4
    A2 --> UC5
    A2 --> UC6
    A2 --> UC7
    A2 --> UC8
    A2 --> UC9

    %% Admin Relationships
    A3 --> UC3
    A3 --> UC4
    A3 --> UC5
    A3 --> UC7
    A3 --> UC8
```

## Use Case Descriptions

### Guest User Use Cases
1. **Register User**
   - Actor: Guest User
   - Description: Create a new user account
   - Preconditions: None
   - Postconditions: New user account created

2. **Login**
   - Actor: Guest User
   - Description: Authenticate and access system
   - Preconditions: Valid user account
   - Postconditions: User session created

### Registered User Use Cases
3. **Create Poll**
   - Actor: Registered User
   - Description: Create a new poll with choices
   - Preconditions: User is logged in
   - Postconditions: New poll created

4. **Edit Poll**
   - Actor: Registered User
   - Description: Modify existing poll details
   - Preconditions: User owns the poll
   - Postconditions: Poll updated

5. **Delete Poll**
   - Actor: Registered User
   - Description: Remove a poll
   - Preconditions: User owns the poll
   - Postconditions: Poll deleted

6. **Vote on Poll**
   - Actor: Registered User
   - Description: Cast vote on active poll
   - Preconditions: User hasn't voted
   - Postconditions: Vote recorded

7. **View Results**
   - Actor: Registered User
   - Description: View poll results
   - Preconditions: Poll exists
   - Postconditions: Results displayed

8. **Export Results**
   - Actor: Registered User
   - Description: Download poll results
   - Preconditions: Poll has votes
   - Postconditions: Results exported

9. **Manage Profile**
   - Actor: Registered User
   - Description: Update user profile
   - Preconditions: User is logged in
   - Postconditions: Profile updated

### Admin Use Cases
- All poll management capabilities
- System-wide access
- User management
- Data export capabilities 