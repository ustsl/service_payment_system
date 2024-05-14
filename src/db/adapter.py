def model_to_dict(model_instance):
    """
    Функция для преобразования инстанса SQLAlchemy модели в словарь.
    """
    return {
        column.name: getattr(model_instance, column.name)
        for column in model_instance.__table__.columns
    }
