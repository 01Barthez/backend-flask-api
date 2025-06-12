# Meal Tracker - User Manual

## Introduction

### What is Meal Tracker?

A comprehensive application for tracking meals, managing allergies, and understanding potential health risks associated with your diet.

## Getting Started

### Account Creation

1. Navigate to `/auth/register`
2. Provide:
   - Unique Username
   - Valid Email
   - Strong Password

### Login Process

1. Go to `/auth/login`
2. Enter credentials
3. Receive JWT authentication token

## Meal Management

### Creating a Meal

- Endpoint: `/meals` (POST)
- Required Information:
  - Meal Name
  - Description (Optional)
  - Ingredients

### Viewing Meals

- List all meals: `/meals` (GET)
- View specific meal: `/meals/{meal_id}` (GET)

### Updating Meals

- Endpoint: `/meals/{meal_id}` (PUT)
- Modify meal details as needed

### Deleting Meals

- Endpoint: `/meals/{meal_id}` (DELETE)
- Permanently removes meal record

## Allergy Tracking

### Adding an Allergy

- Endpoint: `/allergies` (POST)
- Required Information:
  - Associated Meal ID
  - Allergy Name
  - Severity Level

### Allergy Risk Mechanism

- Each allergy increases meal risk by 10%
- Maximum risk: 30%
- Automatically calculated

### Advanced Allergy Insights

- View personal allergies: `/allergies`
- Identify high-risk meals: `/meals/high-risk`

## Security Features

### Authentication

- Token-based authentication
- Secure password storage
- Role-based access control

### Data Privacy

- Users can only access/modify their own data
- Strict input validation

## API Interaction

### Swagger Documentation

- Comprehensive API documentation
- Interactive endpoint testing
- Available at `/apidocs`

## Best Practices

### Meal Logging

- Be precise with ingredients
- Update allergies promptly
- Review meal risk periodically

### Allergy Management

- Document all known allergies
- Update severity levels
- Monitor meal risk trends

## Troubleshooting

### Common Issues

- Check network connection
- Verify authentication token
- Ensure data completeness

## Example Workflow

```
1. Register Account
2. Log In
3. Create Meal
   - Add ingredients
4. Record Allergies
   - Link to specific meals
5. Monitor Meal Risks
6. Make Informed Dietary Choices
```

## Privacy & Consent

- Your data is private
- No third-party sharing
- Secure, encrypted storage

## Support

### Contact Information

- Email: <support@mealtracker.com>
- Documentation: Available in `/docs`

## Version Information

- Current Version: 1.0.0
- Last Updated: 2025-06-11
