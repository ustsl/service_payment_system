def model_to_dict(model_instance):
    """
    Функция для преобразования инстанса SQLAlchemy модели в словарь.
    """
    if isinstance(model_instance, dict):
        return model_instance

    return {
        column.name: getattr(model_instance, column.name)
        for column in model_instance.__table__.columns
    }
