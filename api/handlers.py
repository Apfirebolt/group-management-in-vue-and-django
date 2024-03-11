def create_supplier_handler(sender, supplier_instance, **kwargs):
    # Do something with the newly created supplier instance
    print(f"New supplier created! Name: {supplier_instance.name}")  # Example action