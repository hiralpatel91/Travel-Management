from Travel import db


# metaclass for service registry that use in traveservice model
class ServiceMeta(type(db.Model)):
    _service_registry = []

    def __new__(cls, name, bases, attrs):
        # Create the class
        cls_instance = super().__new__(cls, name, bases, attrs)
        # Register the class type in the service registry
        cls._service_registry.append(cls_instance)
        return cls_instance

    @classmethod
    def get_registered_services(cls):
        return cls._service_registry