# Meal Tracker Application - Class Diagram

## Domain Model Overview

### User Class

- **Attributes**:
  - `id`: Unique identifier
  - `username`: User's unique username
  - `email`: User's email address
  - `password_hash`: Securely hashed password
- **Relationships**:
  - One-to-Many with Meals
  - One-to-Many with Allergies

### Meal Class

- **Attributes**:
  - `id`: Unique identifier
  - `name`: Meal name
  - `description`: Meal description
  - `ingredients`: List of ingredients
  - `allergy_risk`: Calculated allergy risk (0.0 - 0.3)
- **Relationships**:
  - Many-to-One with User
  - One-to-Many with Allergies

### Allergy Class

- **Attributes**:
  - `id`: Unique identifier
  - `name`: Allergy name
  - `severity`: Allergy severity level
- **Relationships**:
  - Many-to-One with User
  - Many-to-One with Meal

## Business Logic Relationships

1. **Allergy Risk Calculation**:
   - Each allergy added to a meal increases risk by 10%
   - Maximum risk capped at 30%
   - Automatically updated when allergies are added/removed

2. **User-Meal Ownership**:
   - Users can only modify their own meals
   - Allergies are tied to specific user-meal combinations

## Data Flow and Interactions

```
[User] 1 -----> * [Meal]
           owns
[User] 1 -----> * [Allergy]
           reports
[Meal] 1 -----> * [Allergy]
           has

Allergy Risk Calculation:
- Allergy Count → Risk Percentage
- 1 Allergy = 10% Risk
- 2 Allergies = 20% Risk
- 3 Allergies = 30% Risk (Max)
```

## Security Considerations

- Passwords are bcrypt-hashed
- JWT used for authentication
- User-specific data access
- Risk calculation prevents meal misuse

## Performance Optimizations

- Lazy loading of relationships
- Cascading delete for related entities
- Indexed database queries
- Efficient risk calculation mechanism
