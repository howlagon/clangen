from scripts.screens.StartScreen import *

class StartScreen(StartScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            screens = {
                self.mod_menu_button: "mod menu"
            }
            if event.ui_element in screens and not self.error_open:
                self.change_screen(screens[event.ui_element])

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
