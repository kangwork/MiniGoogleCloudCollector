from pydantic import BaseModel
from google.cloud.compute_v1.types import (
    ConfidentialInstanceConfig,
    DisplayDevice,
    Metadata,
    ReservationAffinity,
    Scheduling,
    ShieldedInstanceConfig,
    Tags,
    AttachedDisk,
    NetworkInterface,
    ServiceAccount,
)
from typing import MutableSequence


class CEInstance(BaseModel):
    """
    Model for a Compute Engine vm instance
    """

    can_ip_forward: bool
    confidential_instance_config: ConfidentialInstanceConfig
    cpu_platform: str
    creation_timestamp: str
    deletion_protection: bool
    description: str
    disks: MutableSequence[AttachedDisk]
    display_device: DisplayDevice
    fingerprint: str
    id: int
    key_revocation_action_type: str
    kind: str
    label_fingerprint: str
    labels: dict
    last_start_timestamp: str
    machine_type: str
    metadata: Metadata
    name: str
    network_interfaces: MutableSequence[NetworkInterface]
    reservation_affinity: ReservationAffinity
    scheduling: Scheduling
    self_link: str
    service_accounts: MutableSequence[ServiceAccount]
    shielded_instance_config: ShieldedInstanceConfig
    start_restricted: bool
    status: str
    tags: Tags
    zone: str

    @classmethod
    def from_gcp_object(cls, obj: dict):
        return cls(
            can_ip_forward=obj.can_ip_forward,
            confidential_instance_config=obj.confidential_instance_config,
            cpu_platform=obj.cpu_platform,
            creation_timestamp=obj.creation_timestamp,
            deletion_protection=obj.deletion_protection,
            description=obj.description,
            disks=obj.disks,
            display_device=obj.display_device,
            fingerprint=obj.fingerprint,
            id=obj.id,
            key_revocation_action_type=obj.key_revocation_action_type,
            kind=obj.kind,
            label_fingerprint=obj.label_fingerprint,
            labels=obj.labels,
            last_start_timestamp=obj.last_start_timestamp,
            machine_type=obj.machine_type,
            metadata=obj.metadata,
            name=obj.name,
            network_interfaces=obj.network_interfaces,
            reservation_affinity=obj.reservation_affinity,
            scheduling=obj.scheduling,
            self_link=obj.self_link,
            service_accounts=obj.service_accounts,
            shielded_instance_config=obj.shielded_instance_config,
            start_restricted=obj.start_restricted,
            status=obj.status,
            tags=obj.tags,
            zone=obj.zone,
        )

    def __str__(self):
        return f"Zone: {self.zone}, Name: {self.name}"

    class Config:
        arbitrary_types_allowed = True
