from pydantic import BaseModel


class CEInstance(BaseModel):
    """
    Model for a Compute Engine vm instance
    """

    can_ip_forward: bool
    confidential_instance_config: dict
    cpu_platform: str
    creation_timestamp: str
    deletion_protection: bool
    description: str
    disks: dict
    display_device: dict
    fingerprint: str
    id: int
    key_revocation_action_type: str
    kind: str
    label_fingerprint: str
    labels: dict
    last_start_timestamp: str
    machine_type: str
    metadata: dict
    name: str
    network_interfaces: dict
    reservation_affinity: dict
    scheduling: dict
    self_link: str
    service_accounts: dict
    shielded_instance_config: dict
    start_restricted: bool
    status: str
    tags: dict
    zone: str
