# Create directories
mkdir -p finance_tracker/app/models
mkdir -p finance_tracker/app/routes
mkdir -p finance_tracker/app/services
mkdir -p finance_tracker/app/schemas
mkdir -p finance_tracker/app/utils
mkdir -p finance_tracker/config
mkdir -p finance_tracker/tests
mkdir -p finance_tracker/logs
mkdir -p finance_tracker/instance

# Create files
touch finance_tracker/app/__init__.py
touch finance_tracker/app/models/__init__.py
touch finance_tracker/app/models/user.py
touch finance_tracker/app/models/transaction.py
touch finance_tracker/app/models/budget.py
touch finance_tracker/app/models/savings_goal.py
touch finance_tracker/app/routes/__init__.py
touch finance_tracker/app/routes/auth.py
touch finance_tracker/app/routes/transaction.py
touch finance_tracker/app/routes/budget.py
touch finance_tracker/app/routes/analytics.py
touch finance_tracker/app/services/__init__.py
touch finance_tracker/app/services/analytics_service.py
touch finance_tracker/app/services/notification_service.py
touch finance_tracker/app/schemas/__init__.py
touch finance_tracker/app/schemas/user_schema.py
touch finance_tracker/app/schemas/transaction_schema.py
touch finance_tracker/app/schemas/budget_schema.py
touch finance_tracker/app/utils/__init__.py
touch finance_tracker/app/utils/decorators.py
touch finance_tracker/app/utils/error_handlers.py
touch finance_tracker/config/__init__.py
touch finance_tracker/config/config.py
touch finance_tracker/tests/__init__.py
touch finance_tracker/tests/test_models.py
touch finance_tracker/tests/test_routes.py
touch finance_tracker/tests/test_services.py
touch finance_tracker/run.py
touch finance_tracker/requirements.txt