# Data Schema

- **User:** ID, Email, Role (RBAC).
- **Document:** ID, UserID, S3Key, Metadata.
- **Conversation:** ID, UserID, Title.
- **Message:** ID, ConversationID, Role, Content.