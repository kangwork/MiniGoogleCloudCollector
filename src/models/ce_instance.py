from pydantic import BaseModel


class CEInstance(BaseModel):
    """
    Model for a Compute Engine vm instance
    """

    can_ip_forward: bool
    confidential_instance_config: str  # ConfidentialInstanceConfig
    cpu_platform: str
    creation_timestamp: str
    deletion_protection: bool
    description: str
    disks: str  # MutableSequence[AttachedDisk]
    display_device: str  # DisplayDevice
    fingerprint: str
    id: int
    key_revocation_action_type: str
    kind: str
    label_fingerprint: str
    labels: dict
    last_start_timestamp: str
    machine_type: str
    metadata: str  # Metadata
    name: str
    network_interfaces: str  # MutableSequence[NetworkInterface]
    reservation_affinity: str  # ReservationAffinity
    scheduling: str  # Scheduling
    self_link: str
    service_accounts: str  # MutableSequence[ServiceAccount]
    shielded_instance_config: str  # ShieldedInstanceConfig
    start_restricted: bool
    status: str
    tags: str  # Tags
    zone: str

    @classmethod
    def from_gcp_object(cls, obj: dict):
        return cls(
            can_ip_forward=obj.can_ip_forward,
            confidential_instance_config=repr(obj.confidential_instance_config),
            cpu_platform=obj.cpu_platform,
            creation_timestamp=obj.creation_timestamp,
            deletion_protection=obj.deletion_protection,
            description=obj.description,
            disks=repr(obj.disks),
            display_device=repr(obj.display_device),
            fingerprint=obj.fingerprint,
            id=obj.id,
            key_revocation_action_type=obj.key_revocation_action_type,
            kind=obj.kind,
            label_fingerprint=obj.label_fingerprint,
            labels=obj.labels,
            last_start_timestamp=obj.last_start_timestamp,
            machine_type=obj.machine_type,
            metadata=repr(obj.metadata),
            name=obj.name,
            network_interfaces=repr(obj.network_interfaces),
            reservation_affinity=repr(obj.reservation_affinity),
            scheduling=repr(obj.scheduling),
            self_link=obj.self_link,
            service_accounts=repr(obj.service_accounts),
            shielded_instance_config=repr(obj.shielded_instance_config),
            start_restricted=obj.start_restricted,
            status=obj.status,
            tags=repr(obj.tags),
            zone=obj.zone,
        )

    class Config:
        arbitrary_types_allowed = True
