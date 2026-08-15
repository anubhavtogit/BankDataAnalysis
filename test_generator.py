from generator import (
    generate_master_data,
    save_master_data
)


print("Starting banking data generation...")


data = generate_master_data()


save_master_data(data)


print("Banking master data generation completed.")