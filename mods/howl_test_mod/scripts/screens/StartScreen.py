from scripts.screens.StartScreen import *
import scripts.screens.StartScreen

class StartScreen(scripts.screens.StartScreen.StartScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def screen_switches(self):
        super().screen_switches()
        self.continue_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((270, 310), (200, 30))),
            "buttons.continue",
            image_dict=get_button_dict(ButtonStyles.MAINMENU, (200, 30)),
            object_id="@buttonstyles_mainmenu",
            manager=MANAGER,
        )