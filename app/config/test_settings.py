from app.config import settings

print("=" * 60)
print("Application Settings")
print("=" * 60)

print(settings.app_name)
print(settings.app_version)
print(settings.database_url)
print(settings.environment)
print(settings.debug)

print("\nConfiguration Loaded Successfully")