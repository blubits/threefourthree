"""
Events passed between the view and controller in the game.

:Author:     Maded Batara III
:Version:    v20181126
"""

import events

class ViewEvents(events.Events):
    """
    Events that happen in the view and are listened to by the controller.

    Events:
        create: Raise when a game is created on the view, through a
            "Play Now" button, for example. The controller should
            make a new game appropriately.

            Messages:
                Should match the arguments of the Game class: see its
                    documentation.

        answer: Raise when the board is moved on the view. The controller
            should move the board accordingly, and emit any events if
            needed (e.g. the game is lost or won).

            Messages:
                direction (str): Direction to move the board towards,
                    either "up", "down", "left", or "right".

        keep_playing: Raise when the user indicates, through interaction
            with the view, that they want to keep playing the game even
            if a win condition has already been called. Only raise
            if the game has already been won, i.e. the controller
            has already sent a won() event.

        end: Raise when a game is ended, through user feedback on the view
            or otherwise. The controller should call game end and clean up.
    """
    __events__ = ('create', 'move', 'keep_playing', 'end')

class ControllerEvents(events.Events):
    """
    Events that happen in the controller and are listened to by the view.

    Events:
        won: Raise when a game is won, i.e. the win condition has already
            been achieved in the controller. The view should prompt
            the user accordingly; importantly, it must prompt the user
            if he wants to keep playing, and send the appropriate event.

        lost: Raise when a game is lost, i.e. the lose condition has already
            been achieved in the controller. The view should prompt the user
            accordingly.
    """
    __events__ = ('won', 'lost')
