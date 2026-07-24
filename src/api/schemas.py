from pydantic import BaseModel


class MetricInput(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    disk_io: float
    network_in: float
    network_out: float
    response_time: float
    request_count: int
    error_rate: float
    active_users: int
    service_name: str          # changed from int
    region: str                # changed from int
    deployment_version: str    # changed from int
    day_of_week: str           # changed from int
    hour: int