# Data Model: Physical AI & Humanoid Robotics Textbook

## User Entity
- **id**: UUID (primary key)
- **email**: String (unique, required)
- **name**: String (required)
- **software_background**: String (enum: beginner, intermediate, advanced)
- **hardware_background**: String (enum: beginner, intermediate, advanced)
- **preferred_language**: String (default: "en", options: ["en", "ur"])
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated)
- **personalization_settings**: JSON (custom preferences)

**Validation Rules**:
- Email must be valid format
- Name must be 2-50 characters
- Background levels must be from enum
- Preferred language must be from supported list

## TextbookModule Entity
- **id**: UUID (primary key)
- **title**: String (required)
- **description**: Text
- **module_number**: Integer (required, unique)
- **weeks_duration**: Integer (required)
- **programming_language**: String (required)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated)

**Validation Rules**:
- Title must be 5-100 characters
- Module number must be unique
- Weeks duration must be 1-20
- Programming language must be from supported list

## Chapter Entity
- **id**: UUID (primary key)
- **title**: String (required)
- **content**: Text (required)
- **module_id**: UUID (foreign key to TextbookModule)
- **chapter_number**: Integer (required within module)
- **slug**: String (unique, auto-generated from title)
- **learning_objectives**: JSON (array of strings)
- **exercises**: JSON (exercise data)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated)

**Validation Rules**:
- Title must be 5-100 characters
- Content must not be empty
- Module_id must reference existing module
- Chapter number must be unique within module

## Exercise Entity
- **id**: UUID (primary key)
- **chapter_id**: UUID (foreign key to Chapter)
- **type**: String (enum: "coding", "mcq", "diagram", "essay")
- **question**: Text (required)
- **solution**: Text (required for coding/essay)
- **options**: JSON (for MCQ type)
- **difficulty**: String (enum: "beginner", "intermediate", "advanced")
- **created_at**: DateTime (auto-generated)

**Validation Rules**:
- Question must not be empty
- Solution required for coding/essay types
- Options required for MCQ type
- Difficulty must be from enum

## UserProgress Entity
- **id**: UUID (primary key)
- **user_id**: UUID (foreign key to User)
- **chapter_id**: UUID (foreign key to Chapter)
- **completed**: Boolean (default: false)
- **score**: Integer (0-100, nullable)
- **attempts**: Integer (default: 0)
- **completed_at**: DateTime (nullable)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated)

**Validation Rules**:
- User_id and chapter_id combination must be unique
- Score must be 0-100 if provided
- Attempts must be non-negative

## Translation Entity
- **id**: UUID (primary key)
- **original_content_id**: UUID (references either Chapter or Exercise)
- **content_type**: String (enum: "chapter", "exercise")
- **language_code**: String (required, e.g., "ur", "en")
- **translated_content**: Text (required)
- **approved**: Boolean (default: false)
- **created_at**: DateTime (auto-generated)

**Validation Rules**:
- Language code must be from supported list
- Content type must be from enum
- Translated content must not be empty

## State Transitions

### User Registration Flow
1. User initiates registration → User account created (pending)
2. User completes profile → User account active
3. User updates preferences → Personalization settings updated

### Content Progression
1. Chapter content loaded → User can interact
2. User completes exercises → Progress recorded
3. User marks complete → Progress updated to completed

### Translation Lifecycle
1. Translation request created → Awaiting translation
2. Translation completed → Awaiting approval
3. Translation approved → Available for users
4. Translation updated → Review cycle repeats