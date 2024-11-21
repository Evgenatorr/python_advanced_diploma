def entity_to_dict(entity):
    """
    Локальная функция для преобразования данных из базы в нужный словарь
    """
    return {"id": entity.id, "name": entity.name}
