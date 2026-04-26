from api.models import Customer


class CustomerService:
    @staticmethod
    def get_or_create_customer(customer_data):
        psid = customer_data.get('psid')
        email = customer_data.get('email')

        if psid:
            return CustomerService._get_or_update_customer('psid', psid, customer_data)

        if email:
            return CustomerService._get_or_update_customer('email', email, customer_data)

        return Customer.objects.create(**customer_data)

    @staticmethod
    def _get_or_update_customer(field, value, customer_data):
        customer, created = Customer.objects.get_or_create(
            **{field: value},
            defaults=customer_data,
        )
        if not created:
            for attr, val in customer_data.items():
                setattr(customer, attr, val)
            customer.save()
        return customer
