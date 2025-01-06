from scripts.screens.StartScreen import *

class StartScreen(StartScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def screen_switches(self):
        super().screen_switches()
        self.mod_menu_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((self.quit.relative_rect.left, self.quit.relative_rect.top), (200, 30))),
            "mod menu",
            image_dict=get_button_dict(ButtonStyles.MAINMENU, (200, 30)),
            object_id="@buttonstyles_mainmenu",
            manager=MANAGER,
            anchors={"top_target": self.quit},
        )
    
    def exit_screen(self):
        self.mod_menu_button.kill()
        return super().exit_screen()
