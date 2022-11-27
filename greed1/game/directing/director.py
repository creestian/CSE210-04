from game.casting.artifact import Artifact
from game.shared.point import Point
from game.shared.color import Color
import random as r
# from game.casting.cast import Cast

WHITE = Color(255, 255, 255)

class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        # get direction to move from keyboard service
        player = cast.get_first_actor("player")
        velocity = self._keyboard_service.get_direction()
        player.set_velocity(velocity)  
        # player.set_velocity(Point(-15, 0))      
        # player actor = direction horizontal only

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        # create rocks, gems at top of screen (random x, set y)(random number of artifacts)
        gem = Artifact()
        gem.set_text("*")
        gem.set_points(1)
        gem.set_velocity(Point(0,5))
        gem.set_position(Point(r.randint(15, 885),15))
        green = Color(0, 255, 0)
        gem.set_color(green)

        rock = Artifact()
        rock.set_text("o")
        rock.set_points(-1)
        rock.set_velocity(Point(0,5))
        rock.set_position(Point(r.randint(15, 885),15))
        blue = Color(0,0,255)
        rock.set_color(blue)

        cast.add_actor("artifacts", gem)
        cast.add_actor("artifacts", rock)

        # move player, rocks, gems
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        # loop to move all actors
        player = cast.get_first_actor("player")
        player_x = player.get_position().get_x()
        player_y = player.get_position().get_y()
        score = cast.get_first_actor("score")
        for actor in cast.get_actors("artifacts"):
            actor.move_next(max_x, max_y)
            # check for collisions
            if actor.get_text() == "*":
                actor_x = actor.get_position().get_x()
                actor_y = actor.get_position().get_y()
                if ((player_x - 10 < actor_x < player_x + 10) and (player_y - 10 < actor_y < player_y + 10)):
                    score.add_points(1)
                if actor_y > max_y - 30 or((player_x - 10 < actor_x < player_x + 10) and (player_y - 10 < actor_y < player_y + 10)):
                    cast.remove_actor("artifacts", actor)
                    
            elif actor.get_text() == "o":
                actor_x = actor.get_position().get_x()
                actor_y = actor.get_position().get_y()
                if ((player_x - 10 < actor_x < player_x + 10) and (player_y - 10 < actor_y < player_y + 10)):
                    score.add_points(-1)
                if actor_y > max_y - 30 or ((player_x - 10 < actor_x < player_x + 10) and (player_y - 10 < actor_y < player_y + 10)):
                    cast.remove_actor("artifacts", actor)
                    
                    
            
        # move player
        player.move_next(max_x, max_y)

            
        # for actor1 in cast.get_all_actors():
        #     print(actor1.get_position())
        #     # actor1.move_next(max_x, max_y)
        #     x = (actor1.get_position().get_x() + actor1.get_velocity().get_x()) % max_x
        #     y = (actor1.get_position().get_y() + actor1.get_velocity().get_y()) % max_y
        #     actor1.set_position(Point(x, y))

        # check for collisions between player and artifact or player and gem
        # award points if needed(add points to score, negative for rocks, positive for gems)
        # remove artifact or gem if needed

        # artifacts = cast.get_actors("artifacts")
        # player = cast.get_first_actor("player")
        # score = cast.get_first_actor("score")

        # for artifact in artifacts:
        #     if player.get_position().equals(artifact.get_position()):
        #         points = artifact.get_points()
        #         score.add_points(points)
        #         cast.remove_actor("artifacts", artifact)
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        # artifacts = cast.get_actors("artifacts")
        player = cast.get_first_actor("player")
        score = cast.get_first_actor("score")
        score.set_text(f"SCORE: {score.get_points()}")
        for actor in cast.get_actors("artifacts"):
            self._video_service.draw_actor(actor)
        # score = cast.get_first_actor("score")
        # self._video_service.draw_actors(artifacts)
        self._video_service.draw_actor(player)
        self._video_service.draw_actor(score)
        # self._video_service.draw_actor(score)
        self._video_service.flush_buffer()