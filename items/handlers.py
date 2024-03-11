from .models import Supplier  # Replace with your model name

def handle_supplier_creation(sender, supplier_instance, **kwargs):
    # Do something with the newly created supplier instance
    print(f"New supplier created! Name: {supplier_instance.name}")  # Example action