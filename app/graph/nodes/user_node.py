from app.graph.state.travel_state import TravelState


class UserNode:

    @staticmethod
    def initialize(state: TravelState):

        print("User Initialized")

        return state