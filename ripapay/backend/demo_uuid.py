from utils.uuid_generator import UUIDGenerator

# Create UUID generator instance
generator = UUIDGenerator()

# Generate sample UUIDs for different businesses
businesses = ["Acme Corp", "Tech Solutions", "Retail Store"]

print("Sample Business UUIDs:")
print("-" * 30)
for business in businesses:
	uuid = generator.generate_business_uuid(business)
	print(f"{business}: {uuid}")