from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar

from agentcore.models import V1UserProfile
from devicebay import Device
from pydantic import BaseModel
from taskara import Task

from .skill import Skill

C = TypeVar("C", bound="BaseModel")
T = TypeVar("T", bound="TaskAgent")


class TaskAgent(Generic[C, T], ABC):
    """An agent that works on tasks"""

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    def learn_task(
        self,
        task: Task,
        skill: Skill,
        user: V1UserProfile,
    ):
        """Learn a task

        Args:
            skill (Skill): The skill
            user (V1UserProfile): The user
            task (Task): The task
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def solve_task(
        self,
        task: Task,
        device: Optional[Device] = None,
        max_steps: int = 30,
    ) -> Task:
        """Solve a task on a device

        Args:
            task (Task): The task
            device (Device, optional): Device to perform the task on. Default to None.
            max_steps (int, optional): Max steps allowed. Defaults to 30.

        Returns:
            Task: A task
        """
        pass

    @classmethod
    @abstractmethod
    def supported_devices(cls) -> List[Type[Device]]:
        """Devices this agent supports

        Returns:
            List[Type[Device]]: A list of supported devices
        """
        pass

    @classmethod
    def is_supported(cls, device: Device) -> bool:
        """Is the given device supported by this agent

        Args:
            device (Device): The device to check

        Returns:
            bool: Whether its supported
        """
        return type(device) in cls.supported_devices()

    @classmethod
    @abstractmethod
    def config_type(cls) -> Type[C]:
        """Type to configure the agent

        Returns:
            Type[C]: A configuration type
        """
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, config: C) -> T:
        """Create an agent from a config

        Args:
            config (C): Config to create the agent from

        Returns:
            T: The Agent
        """
        pass

    @classmethod
    @abstractmethod
    def default(cls) -> T:
        """Create a default agent with no params

        Returns:
            T: The Agent
        """
        pass

    @classmethod
    def init(cls) -> None:
        """Initialize the Agent type"""
        pass
