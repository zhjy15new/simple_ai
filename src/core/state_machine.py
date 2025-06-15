"""
This module implements the state machine for the camera capture process.
It defines the possible states, events, and transitions to manage the lifecycle
of connecting to a camera and capturing an image in a robust and predictable way.
"""

from enum import Enum, auto

class CaptureState(Enum):
    """Enumeration of possible states in the capture process."""
    DISCONNECTED = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    AUTHENTICATING = auto()
    AUTHENTICATED = auto()
    CAPTURING = auto()
    COMPLETED = auto()
    ERROR = auto()
    RETRYING = auto()

class CaptureEvent(Enum):
    """Enumeration of events that can trigger a state transition."""
    START_CONNECT = auto()
    CONNECT_SUCCESS = auto()
    CONNECT_FAILURE = auto()
    START_AUTH = auto()
    AUTH_SUCCESS = auto()
    AUTH_FAILURE = auto()
    START_CAPTURE = auto()
    CAPTURE_SUCCESS = auto()
    CAPTURE_FAILURE = auto()
    RETRY = auto()
    RESET = auto()

class CaptureStateMachine:
    """
    Manages the state of the camera capture lifecycle.
    
    This class holds the current state and defines the valid transitions
    between states based on events. It ensures that the capture process
    follows a logical and controlled flow.
    """

    def __init__(self, initial_state: CaptureState = CaptureState.DISCONNECTED):
        self.current_state = initial_state
        
        # Define the valid transitions in a dictionary for clarity and ease of management.
        # Format: {current_state: {event: next_state}}
        self.transitions = {
            CaptureState.DISCONNECTED: {
                CaptureEvent.START_CONNECT: CaptureState.CONNECTING
            },
            CaptureState.CONNECTING: {
                CaptureEvent.CONNECT_SUCCESS: CaptureState.CONNECTED,
                CaptureEvent.CONNECT_FAILURE: CaptureState.ERROR
            },
            CaptureState.CONNECTED: {
                CaptureEvent.START_AUTH: CaptureState.AUTHENTICATING,
                CaptureEvent.RESET: CaptureState.DISCONNECTED
            },
            CaptureState.AUTHENTICATING: {
                CaptureEvent.AUTH_SUCCESS: CaptureState.AUTHENTICATED,
                CaptureEvent.AUTH_FAILURE: CaptureState.ERROR
            },
            CaptureState.AUTHENTICATED: {
                CaptureEvent.START_CAPTURE: CaptureState.CAPTURING,
                CaptureEvent.RESET: CaptureState.DISCONNECTED
            },
            CaptureState.CAPTURING: {
                CaptureEvent.CAPTURE_SUCCESS: CaptureState.COMPLETED,
                CaptureEvent.CAPTURE_FAILURE: CaptureState.ERROR
            },
            CaptureState.COMPLETED: {
                CaptureEvent.RESET: CaptureState.DISCONNECTED
            },
            CaptureState.ERROR: {
                CaptureEvent.RETRY: CaptureState.RETRYING,
                CaptureEvent.RESET: CaptureState.DISCONNECTED
            },
            CaptureState.RETRYING: {
                CaptureEvent.START_CONNECT: CaptureState.CONNECTING,
                CaptureEvent.RESET: CaptureState.DISCONNECTED
            }
        }

    def transition(self, event: CaptureEvent) -> CaptureState:
        """

        Attempts to transition to a new state based on the given event.

        Args:
            event: The event that occurred.

        Returns:
            The new state after the transition.

        Raises:
            ValueError: If the transition is not valid for the current state.
        """
        if self.current_state in self.transitions and event in self.transitions[self.current_state]:
            next_state = self.transitions[self.current_state][event]
            # print(f"State transition: {self.current_state.name} -> {next_state.name} on event {event.name}")
            self.current_state = next_state
            return self.current_state
        
        raise ValueError(
            f"Invalid transition: Cannot handle event '{event.name}' in state '{self.current_state.name}'"
        )

    def is_terminal(self) -> bool:
        """Checks if the state machine is in a terminal state (COMPLETED or ERROR without retry)."""
        return self.current_state in [CaptureState.COMPLETED, CaptureState.ERROR] 