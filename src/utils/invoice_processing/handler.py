from .factory import (
    CreateQuickspeakRequest,
    CreateImvoRequest,
    factory,
)


def get_api_request_data_for_change_balance(
    service_name: str, acc_id: str, balance: float
):
    if service_name == "quickspeak":
        project = CreateQuickspeakRequest
    elif service_name == "imvo":
        project = CreateImvoRequest
    data = factory(project=project, acc_id=acc_id, balance=balance)
    return data
